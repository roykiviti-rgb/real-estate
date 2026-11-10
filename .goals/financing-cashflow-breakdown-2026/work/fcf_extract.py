# -*- coding: utf-8 -*-
"""fcf_extract — generic extraction engine for the consolidated statement of cash flows.

Steps (all read-only on the source PDF):
  1. scan every page: rebuild words/lines from the text layer (fcf_lib.page_words / group_lines),
     detect the page title (top of page), statement-type flags (solo / board / notes / TOC /
     consolidated), cash-flow section headings and section totals;
  2. find the consolidated cash-flow statement = the first complete statement block (operating +
     financing structure, enough numeric rows) that is not solo (38D) / board / notes; investee
     statements come later in the file and are therefore never chosen first;
  3. analyse every statement page: value columns (x-spans of numeric groups), layout (RTL Hebrew /
     LTR English), header phrases -> per-column header text -> months / end date / audit / restated,
     body rows (label + one value per column, wrapped labels merged), units/currency;
  4. cut the financing section (heading .. reported total), suggest an item per line, find the (*)
     lines (interest / dividends paid) in the operating and investing sections;
  5. return a dict (schema used by finalize_report / build_company / fcf_render) + flags for triage.
"""
import sys

sys.dont_write_bytecode = True

import os  # noqa: E402
import re  # noqa: E402
import statistics  # noqa: E402

import pymupdf  # noqa: E402

import fcf_lib as L  # noqa: E402


# ----------------------------------------------------------------------------- text helpers
def compact(t):
    """Remove whitespace (and stray colons) and normalise quote characters for keyword matching."""
    t = t.replace("״", '"').replace("”", '"').replace("“", '"').replace("׳", "'").replace("’", "'")
    return re.sub(r"[\s:]+", "", t)


SEC_RX = {
    "operating": re.compile(r"(?:פ?עילות|פ?עילויות)[()]*ה?שוטפת|operatingactivities", re.I),
    "investing": re.compile(r"(?:פ?עילות|פ?עילויות)[()]*ה?השקעה|investingactivities", re.I),
    "financing": re.compile(r"(?:פ?עילות|פ?עילויות)[()]*ה?מימון|financingactivities", re.I),
}
CF_TITLE_RX = re.compile(r"תזרימי(?:ה)?מזומנים|תזרים(?:ה)?מזומנים|cashflows?|statementsofcash", re.I)
SOLO_RX = re.compile(r"המיוחסים?לחברה|המיוחסיםלחברה|מידעכספינפרד|נתוניםכספייםמתוך|38ד|נפרדים|הנפרד|"
                     r"נתוניםעלתזרימי|נתוניםכספייםעלתזרימי|separatefinancial|parentcompany", re.I)
# phrases that mark a separate-company (38D) page anywhere on the page, typically in the footer
# ('המידע הנוסף המצורף מהווה חלק בלתי נפרד מהדוחות הכספיים הנפרדים'); 'חלק בלתי נפרד' alone does not match
SOLO_PAGE_RX = re.compile(r"מידעכספינפרד|המידעהכספיהנפרד|המידעהכספיהבינייםהנפרד|הדוחותהכספייםהנפרדים|"
                          r"מהדוחותהכספייםהנפרדים|דוחותכספייםנפרדים|הנתוניםהכספייםהנפרדים|נתוניםכספייםנפרדים|"
                          r"המיוחסיםלחברהכחברהאם|תקנה38ד|separatefinancial(?:information|statements|data)", re.I)
BOARD_RX = re.compile(r"דירקטוריון|directors", re.I)
NOTES_RX = re.compile(r"באורים|ביאורים|באור\d{1,2}[\-–]?[א-ת]|ביאור\d{1,2}[\-–]?[א-ת]|notesto", re.I)
TOC_RX = re.compile(r"תוכןעניינים|תוכןהעניינים|tableofcontents", re.I)
CONS_RX = re.compile(r"מאוחד|consolidated", re.I)
NONCASH_RX = re.compile(r"שלאבמזומן|שלאכרוכותבמזומנים|שלאכרוכהבמזומן|מהותיותשלא|non-?cash|נספח", re.I)
TOTAL_WORD_RX = re.compile(r"נטו|סה\"כ|סה\"כ|סך|מזומנים|net|total", re.I)
CASH_END_RX = re.compile(r"(?:יתרת)?מזומניםושוויי?מזומניםל(?:סוף|תום)|cashandcashequivalents.{0,12}end", re.I)
INTEGRAL_RX = re.compile(r"(?:הבאורים|הביאורים)(?:ה)?מצורפים|מהוויםחלקבלתינפרד|מהווהחלקבלתינפרד|integralpart", re.I)
HEADER_WORDS_RX = re.compile(r"חודשים|החודשים|שהסתיימו|שהסתיימה|לשנה|לתקופה|מבוקר|ended|months|year|unaudited|audited",
                             re.I)
HDR_LIKE_RX = re.compile(r"20\d\d|חודשים|חודשי|שהסתיימ|שנסתיימ|לשנה|לשנת|שנה|לתקופה|לתקופות|ביום|ליום|מבוקר|אלפי|מיליוני|"
                         r"באור|ביאור|מוצג|מחדש|שלושה|שלושת|ששה|שישה|ששת|שישת|תשעה|תשעת|"
                         r"ינואר|פברואר|מרס|מרץ|אפריל|מאי|יוני|יולי|אוגוסט|ספטמבר|אוקטובר|נובמבר|דצמבר|"
                         r"ended|months|year|audited|thousands|millions|restated|note|^\(?\*?\)?$|^\d{1,2}[-–/]\d", re.I)
DATE_TOKEN_RX = re.compile(r"^\d{1,2}[./]\d{1,2}[./]\d{2,4}$|^\d+(?:\.\d+){2,}$|^\d{1,3}-\d{1,3}$")
LETTER_RX = re.compile(r"[A-Za-z\u05D0-\u05EA]")
MONTH_WORD_RX = re.compile(r"^(?:ב|ל|מ)?(?:ינואר|פברואר|מרץ|מרס|אפריל|מאי|יוני|יולי|אוגוסט|ספטמבר|אוקטובר|נובמבר|"
                           r"דצמבר)$|^(?:january|february|march|april|may|june|july|august|september|october|"
                           r"november|december)$|^(?:ביום|ליום)$", re.I)
NOTE_HDR_RX = re.compile(r"באור|ביאור|סעיף|^note$|^notes$", re.I)


def is_value_token(w):
    """A word that can be (part of) an amount: digits with , . ( ) - or a dash meaning zero, or a lone
    parenthesis / thousands separator that belongs to a neighbouring number (some PDFs place '164', ','
    and '896' of '164,896' in separate text spans)."""
    t = w.text
    if not L.NUM_TOKEN_RE.match(t):
        return False
    if DATE_TOKEN_RX.match(t.strip("()")):
        return False
    return any(c.isdigit() for c in t) or all(c in L.DASHES for c in t) or all(c in "()" for c in t) or t in (",", ".")


def label_hyphen(w, letters):
    """A dash (or a lone ',' / '.') that touches a word with letters on the same line belongs to the label
    text ('... ואחרים -', 'ואחרים,'), not to an amount."""
    if not w.text or not (all(c in L.DASHES for c in w.text) or w.text in (",", ".")):
        return False
    lim = max(3.5, 0.45 * max(w.y1 - w.y0, 1.0)) if w.text not in (",", ".") else 1.5
    return any(min(abs(w.x0 - lw.x1), abs(lw.x0 - w.x1)) <= lim for lw in letters)


def value_groups(line):
    """Numeric value groups of a line (years / dates excluded). Letter-spaced single digits ('2 0 2 5')
    are first joined into one token. A dash that touches a word of the label ('... ואחרים -' wrapped onto
    'זמן ארוך') is a hyphen of the label, not a zero value; a day number next to a month word
    ('ביום 31 במרץ') is part of a date."""
    letters = [w for w in line.words if LETTER_RX.search(w.text)]
    months = [w for w in letters if MONTH_WORD_RX.match(w.text.strip(",.()"))]

    def date_day(w):
        if not re.fullmatch(r"\d{1,2}[,.]?", w.text) or not months:
            return False
        lim = max(6.0, 0.9 * max(w.y1 - w.y0, 1.0))
        return any(min(abs(w.x0 - mw.x1), abs(mw.x0 - w.x1)) <= lim for mw in months)

    toks = sorted([w for w in line.words if is_value_token(w) and not label_hyphen(w, letters)
                   and not date_day(w)], key=lambda w: w.x0)
    merged, single = [], []
    for w in toks:
        if (merged and single[-1] and len(w.text) == 1 and w.text.isdigit() and len(merged[-1].text) < 4
                and w.x0 - merged[-1].x1 < max(2.6, 0.38 * w.h)):
            p = merged[-1]
            merged[-1] = L.Word(p.text + w.text, p.x0, min(p.y0, w.y0), w.x1, max(p.y1, w.y1), w.size, w.font)
            continue
        merged.append(w)
        single.append(len(w.text) == 1 and w.text.isdigit())
    gs = L.build_groups(merged)
    out = []
    for g in gs:
        t = g[2]
        core = t.strip("()*")
        if re.fullmatch(r"(?:19|20)\d\d", core) or DATE_TOKEN_RX.match(core):
            continue
        out.append(g)
    return out


# ----------------------------------------------------------------------------- page scan
class PageScan:
    def __init__(self, page, pno):
        self.pno = pno
        self.page = page
        self.H, self.W = page.rect.height, page.rect.width
        self.words = L.page_words(page)
        self.lines = L.group_lines(self.words)
        for ln in self.lines:
            ln.vgroups = value_groups(ln)
        self.texts = [ln.text_all() for ln in self.lines]
        self.ctexts = [compact(t) for t in self.texts]
        numeric = [i for i, ln in enumerate(self.lines) if len(ln.vgroups) >= 1 and ln.yc < self.H * 0.93]
        self.n_numeric = len(numeric)
        # the title block ends at the first line that carries real amounts (thousands separator / parentheses)
        first_num = min([self.lines[i].yc for i in numeric
                         if len(self.lines[i].vgroups) >= 2 and any(re.search(r"\d,\d{3}|\(\d", g[2])
                                                                     for g in self.lines[i].vgroups)],
                        default=self.H)
        top = [i for i, ln in enumerate(self.lines) if ln.yc < min(self.H * 0.33, first_num)]
        self.title = " | ".join(self.texts[i] for i in top)
        tc = compact(self.title)
        self.ctitle = tc
        self.cf_title = bool(CF_TITLE_RX.search(tc))
        self.solo = bool(SOLO_RX.search(tc))
        self.board = bool(BOARD_RX.search(tc))
        self.notes = bool(NOTES_RX.search(tc))
        self.toc = bool(TOC_RX.search(compact(" ".join(self.texts[:40]))))
        self.cons = bool(CONS_RX.search(tc))
        self.heads = {k: [] for k in SEC_RX}
        self.totals = {k: [] for k in SEC_RX}
        n = len(self.lines)
        for i, ct in enumerate(self.ctexts):
            ln = self.lines[i]
            # a heading / total label may wrap over two lines ('תזרימי מזומנים מפעילות' + 'השקעה')
            joined = ct
            vline = ln
            if not ln.vgroups and i + 1 < n and self.lines[i + 1].yc - ln.yc < 2.2 * max(ln.y1 - ln.y0, 6):
                joined = ct + self.ctexts[i + 1]
                vline = self.lines[i + 1]
            for k, rx in SEC_RX.items():
                hit = rx.search(ct) or (joined is not ct and rx.search(joined) and not rx.search(self.ctexts[i + 1]))
                if hit:
                    src = vline if (joined is not ct and not rx.search(ct)) else ln
                    if src.vgroups:
                        dashes_only = all(all(c in L.DASHES for c in g[2]) for g in src.vgroups)
                        if re.search(r"נטו|net|סה\"כ|סך", joined, re.I) or (TOTAL_WORD_RX.search(joined)
                                                                            and not dashes_only):
                            self.totals[k].append(i)
                        else:
                            self.heads[k].append(i)      # heading row with dashes (empty section)
                    else:
                        self.heads[k].append(i)
        self.cash_end = any(CASH_END_RX.search(ct) for ct in self.ctexts)
        # statement pages carry 'the accompanying notes are an integral part ...' and a formal title
        allc = "".join(self.ctexts)
        self.integral = bool(INTEGRAL_RX.search(allc))
        if not self.solo and not self.cons and SOLO_PAGE_RX.search(allc):
            self.solo = True     # separate-company (38D) statement recognised by its footer / body phrases
        self.formal_title = bool(re.search(r"על(?:ה)?תזרימי|statementsofcashflows|statementofcashflows", tc, re.I))
        self.n_chars = sum(len(w.text) for w in self.words)

    def summary(self):
        return {"p": self.pno, "cf_title": self.cf_title, "solo": self.solo, "board": self.board, "notes": self.notes,
                "toc": self.toc, "cons": self.cons, "numeric": self.n_numeric,
                "heads": {k: len(v) for k, v in self.heads.items() if v},
                "totals": {k: len(v) for k, v in self.totals.items() if v}, "title": self.title[:150]}


GENERIC_NAME_TOKENS = {"קבוצת", "בעמ", "חברה", "החברה", "לימיטד", "בערבון", "מוגבל", "אחזקות", "השקעות", "ופיתוח",
                       "נדלן", "בניה", "ובניה", "ובנין", "לבנין", "יזמות", "הנדסה", "גרופ", "ושות"}


def name_tokens(folder):
    name = folder.split(" - ", 1)[1] if " - " in folder else folder
    toks = re.split(r"[\s\-,().']+", name.replace("_", "").replace('"', ""))
    toks = [t for t in toks if len(t) >= 3 and not t.isdigit()]
    specific = [t for t in toks if t not in GENERIC_NAME_TOKENS]
    return specific or toks


def find_statement(scans, folder=None):
    """Return (block info, candidate blocks) of the consolidated cash-flow statement, or (None, cands)."""
    ntoks = name_tokens(folder) if folder else []
    blocks, cur = [], []
    for s in scans:
        has_sec = any(s.heads[k] or s.totals[k] for k in SEC_RX)
        excluded = s.board or (s.toc and s.n_numeric < 15)
        if s.notes and not (has_sec and (s.cf_title or s.n_numeric >= 15)):
            excluded = True      # a notes page joins only if it really carries cash-flow sections
        member = not excluded and ((s.cf_title and (s.n_numeric >= 5 or has_sec)) or (cur and has_sec))
        if cur and not excluded and s.cf_title and s.pno == cur[-1].pno + 1:
            member = True        # continuation page of the statement (e.g. non-cash appendix)
        if member and cur and (s.pno != cur[-1].pno + 1 or s.solo != cur[-1].solo or s.notes != cur[-1].notes):
            blocks.append(cur)
            cur = []
        if member:
            cur.append(s)
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    cands = []
    for b in blocks:
        info = {
            "pages": [s.pno for s in b],
            "solo": any(s.solo for s in b), "board": any(s.board for s in b), "notes": any(s.notes for s in b),
            "cons": any(s.cons for s in b),
            "op": any(s.heads["operating"] or s.totals["operating"] for s in b),
            "inv": any(s.heads["investing"] or s.totals["investing"] for s in b),
            "fin_head": sum(len(s.heads["financing"]) for s in b),
            "fin_total": sum(len(s.totals["financing"]) for s in b),
            "cash_end": any(s.cash_end for s in b),
            "integral": any(s.integral for s in b),
            "formal": any(s.formal_title for s in b),
            "numeric": sum(s.n_numeric for s in b),
        }
        if ntoks:
            info["name"] = round(max(sum(1 for t in ntoks if t in s.ctitle.replace('"', "")) / len(ntoks) for s in b), 2)
        else:
            info["name"] = 0.0
        info["complete"] = bool((info["fin_total"] or info["fin_head"]) and (info["op"] or info["inv"])
                                and info["numeric"] >= 18)
        info["strong"] = bool((info["fin_total"] or info["fin_head"]) and info["op"] and info["inv"]
                              and (info["numeric"] >= 25 or info["cash_end"]))
        info["score"] = (3 * bool(info["fin_total"]) + 2 * bool(info["fin_head"]) + 2 * info["op"] + 2 * info["inv"]
                         + 2 * info["cash_end"] + info["cons"] + 4 * info["integral"] + 2 * info["formal"]
                         + 3 * info["name"] + min(info["numeric"], 60) / 20.0)
        cands.append(info)
    ok = [c for c in cands if c["complete"] and not c["solo"] and not c["board"]]
    pick = None
    for pool in ([c for c in ok if c["strong"] and not c["notes"]],
                 [c for c in ok if c["strong"]]):
        if pool:
            # a block titled 'מאוחד/consolidated' beats untitled ones (separate-company data, investees)
            sub = [c for c in pool if c["cons"]] or pool
            best = max(c["score"] for c in sub)
            pick = [c for c in sub if c["score"] >= best - 0.5][0]     # best score; ties -> first in the file
            pick["first_strong"] = pick is pool[0]
            break
    if pick is None and ok:
        pick = max(ok, key=lambda c: c["score"])
        pick["first_strong"] = False
    return pick, cands


# ----------------------------------------------------------------------------- page analysis
def cluster_spans(intervals, min_count):
    iv = sorted(intervals)
    spans = []
    for a, b in iv:
        if spans and a <= spans[-1][1] + 0.5:
            s = spans[-1]
            spans[-1] = [s[0], max(s[1], b), s[2] + 1]
        else:
            spans.append([a, b, 1])
    return [s for s in spans if s[2] >= min_count]


class PageAnalysis:
    pass


def label_side(lines, spans):
    """'rtl' when the row labels are right of the value columns (Hebrew), 'ltr' when left (English)."""
    if not spans:
        return "rtl"
    xr = max(s[1] for s in spans)
    xl = min(s[0] for s in spans)
    right = left = 0
    for ln in lines:
        if not ln.vgroups:
            continue
        for w in ln.words:
            if is_value_token(w):
                continue
            if w.x0 > xr + 2:
                right += len(w.text)
            elif w.x1 < xl - 2:
                left += len(w.text)
    return "ltr" if left > right * 1.5 else "rtl"


def analyse(scan, spans_hint=None):
    """Columns, header text per column, body rows of one statement page."""
    a = PageAnalysis()
    a.scan = scan
    lines = scan.lines
    H, W = scan.H, scan.W
    a.H, a.W = H, W
    # footer / printed page number
    a.printed_page = None
    foot = []
    for i, ln in enumerate(lines):
        if ln.yc > H * 0.88:
            t = ln.text_all().replace(" ", "")
            m = re.fullmatch(r"[-–]?(\d{1,3})[-–]?", t)
            if m:
                a.printed_page = int(m.group(1))
                foot.append(i)
    # value spans from lines below the title area
    cand = [ln for i, ln in enumerate(lines) if i not in foot and ln.vgroups]
    intervals = [(g[0], g[1]) for ln in cand for g in ln.vgroups]
    n_num = len(cand)
    spans = cluster_spans(intervals, max(3, int(0.25 * n_num)))
    if spans_hint and len(spans) < len(spans_hint):
        spans = [list(s) for s in spans_hint]
    spans = [list(s[:2]) + [s[2] if len(s) > 2 else 0] for s in spans]
    a.layout = label_side(cand, spans)
    # drop a note-reference column (sparse small integers next to the labels) or a line-numbering column
    # (small integers increasing down the page, e.g. a PDF made from a text processor with line numbers)
    a.ignored_spans = []
    if len(spans) >= 2:
        side = max(spans, key=lambda s: s[0]) if a.layout == "rtl" else min(spans, key=lambda s: s[0])
        hits = [(ln.yc, g[2]) for ln in cand for g in ln.vgroups if g[0] <= side[1] + 1 and g[1] >= side[0] - 1]
        vals = [v for _, v in hits]
        small = all(re.fullmatch(r"\d{1,2}[א-ת]?|[\d.]{1,5}", v.strip("()")) for v in vals) if vals else False
        ints = [int(v) for v in vals if re.fullmatch(r"\d{1,3}", v)]
        numbering = len(ints) >= 5 and len(ints) == len(vals) and all(b > c for c, b in zip(ints, ints[1:]))
        if vals and ((small and len(vals) < 0.4 * n_num and side[1] - side[0] < 25) or numbering):
            spans.remove(side)
            a.ignored_spans.append(side)
    a.note_span = a.ignored_spans[0] if a.ignored_spans else None
    spans.sort(key=lambda s: s[0])
    a.spans = [(s[0], s[1]) for s in spans]
    a.centres = [(s[0] + s[1]) / 2 for s in a.spans]
    pitch = statistics.median([b - c for c, b in zip(a.centres, a.centres[1:])]) if len(a.centres) > 1 else 60.0
    a.col_pitch = pitch
    xr = max([s[1] for s in a.spans], default=W * 0.5)
    xl = min([s[0] for s in a.spans], default=W * 0.5)
    if a.note_span:
        if a.layout == "rtl":
            xr = max(xr, a.note_span[1])
        else:
            xl = min(xl, a.note_span[0])
    a.values_x = (xl, xr)

    def numlike(w):
        return is_value_token(w) and not all(c in "()" for c in w.text)

    def label_words(ln):
        # a word with letters that extends beyond the value area belongs to the label even if it starts
        # inside it (the value area can be widened by an appendix block printed lower on the page);
        # a hyphen touching a label word stays in the label
        lets = [w for w in ln.words if LETTER_RX.search(w.text)]
        if a.layout == "rtl":
            return [w for w in ln.words if label_hyphen(w, lets) or (
                (w.x0 > xr + 2 or (LETTER_RX.search(w.text) and w.x1 > xr + 8))
                and not (numlike(w) and w.x0 < xr + 40))]
        return [w for w in ln.words if label_hyphen(w, lets) or (
            (w.x1 < xl - 2 or (LETTER_RX.search(w.text) and w.x0 < xl - 8))
            and not (numlike(w) and w.x1 > xl - 40))]

    # first body line: a section heading, or a line with a value in a column and a real label
    body_start = None
    for i, ln in enumerate(lines):
        if i in foot:
            continue
        ct = scan.ctexts[i]
        lw = label_words(ln)
        lab = compact(L.join_rtl(lw)) if lw else ""
        is_head = any(rx.search(ct) for rx in SEC_RX.values()) and (not ln.vgroups or i in scan.heads.get("financing", []))
        hdrish = bool(HEADER_WORDS_RX.search(ct)) and not any(rx.search(ct) for rx in SEC_RX.values())
        in_cols = [g for g in ln.vgroups if _span_of(g, a.spans) is not None]
        big = [g for g in in_cols if re.search(r"\d,\d|\(\d|\d\)|\d{3}", g[2])]
        amountish = bool(big) or (len({_span_of(g, a.spans) for g in in_cols}) >= 2
                                  and not HDR_LIKE_RX.search(ct))
        hdrish = hdrish and not big
        has_val = bool(in_cols) and amountish
        real_label = len(re.sub(r"[^א-תA-Za-z]", "", lab)) >= 3 and not NOTE_HDR_RX.search(lab) and \
            not re.search(r"אלפי|מיליוני|thousands|millions", lab, re.I)
        if is_head or (has_val and real_label and not hdrish):
            body_start = i
            break
    if body_start is None:
        body_start = len(lines)
    a.body_start = body_start
    above = [ln for i, ln in enumerate(lines[:body_start])]
    # header lines = the contiguous block of header-like lines directly above the body (column titles,
    # years, audit status, units); everything above it is the title block (company, statement name)
    hdr, title = [], []
    k = len(above) - 1
    gap_used = False
    while k >= 0:
        ln = above[k]
        over = [w for w in ln.words if w.x1 > xl - 6 and w.x0 < xr + 6]
        ct = compact(ln.text_all())
        hdr_like = bool(over) and bool(HDR_LIKE_RX.search(ct))
        if hdr_like:
            hdr.insert(0, ln)
        elif over and not gap_used and k > 0 and hdr and len(ln.words) <= 3:
            hdr.insert(0, ln)        # one short stray line inside the header block (e.g. a lone word)
            gap_used = True
        elif hdr or not over:
            if hdr:
                break
        k -= 1
    title = above[:k + 1] if hdr else above
    hdr_y0 = min([ln.y0 for ln in hdr], default=None)
    a.hdr_lines = hdr
    a.title_lines = title
    a.above_lines = above
    # per-column header text from phrases
    a.col_headers = column_headers(hdr, a.spans, a.centres, pitch, a.layout, xl, xr)
    # body rows
    rows = []
    for i, ln in enumerate(lines[body_start:], start=body_start):
        if i in foot:
            continue
        lw = label_words(ln)
        vals = {}
        unparsed = []
        for g in ln.vgroups:
            k = _span_of(g, a.spans)
            if k is None:
                if any(g[0] <= s[1] + 1 and g[1] >= s[0] - 1 for s in a.ignored_spans):
                    continue
                gx = (g[0] + g[1]) / 2
                if (a.layout == "rtl" and gx > xr + 2) or (a.layout == "ltr" and gx < xl - 2):
                    continue          # part of the label (e.g. a dash or a number inside the text)
                unparsed.append(g[2])
                continue
            raw = g[2] if k not in vals else vals[k][0] + " " + g[2]
            vals[k] = (raw, None)
        stars = set()
        for k, (raw, _) in list(vals.items()):
            v, fl = parse_amount(raw)
            vals[k] = (raw, v)
            if v is None:
                unparsed.append(raw)
            if "asterisk" in fl:
                stars.add(k)
        rows.append({"line": ln, "label_words": lw, "label": L.join_rtl(lw) if lw else "", "vals": vals,
                     "unparsed": unparsed, "y0": ln.y0, "y1": ln.y1, "yc": ln.yc, "stars": stars,
                     "x0": min(w.x0 for w in ln.words), "x1": max(w.x1 for w in ln.words),
                     "ct": scan.ctexts[i], "idx": i})
    a.rows = rows
    lab_x = [w.x1 for r in rows for w in r["label_words"]] if a.layout == "rtl" else \
        [w.x0 for r in rows for w in r["label_words"]]
    a.label_edge = (max(lab_x, default=W) if a.layout == "rtl" else min(lab_x, default=0))
    inner = sorted((min(w.x0 for w in r["label_words"]) if a.layout == "rtl" else -max(w.x1 for w in r["label_words"]))
                   for r in rows if len(r["label_words"]) >= 3)
    if inner:
        v = inner[min(len(inner) - 1, len(inner) // 5)]      # 20th percentile: robust to stray words
        a.label_inner = v if a.layout == "rtl" else -v
    else:
        a.label_inner = None
    body_words = [w for r in rows for w in r["line"].words]
    hw = [w for ln in a.title_lines + hdr for w in ln.words]
    a.content_x = [min([w.x0 for w in body_words + hw], default=0), max([w.x1 for w in body_words + hw], default=W)]
    a.header_x = [min([w.x0 for w in hw], default=0), max([w.x1 for w in hw], default=W)]
    a.title_y = [min([ln.y0 for ln in a.title_lines], default=(hdr_y0 or 0)),
                 max([ln.y1 for ln in a.title_lines], default=(hdr_y0 or 0))]
    a.header_y = [hdr_y0 if hdr_y0 is not None else (rows[0]["y0"] if rows else 0),
                  max([ln.y1 for ln in hdr], default=(rows[0]["y0"] if rows else 0))]
    a.title_text = " | ".join(ln.text_all() for ln in a.title_lines)
    a.above_text = " | ".join(ln.text_all() for ln in above)
    ys = [r["yc"] for r in rows if r["vals"]]
    diffs = sorted(b - c for c, b in zip(ys, ys[1:]) if b - c > 4)
    a.pitch = statistics.median(diffs) if diffs else 12.0
    return a


def _span_of(g, spans):
    gx = (g[0] + g[1]) / 2
    hit = [k for k, s in enumerate(spans) if g[0] <= s[1] + 2 and g[1] >= s[0] - 2]
    if not hit:
        return None
    return min(hit, key=lambda k: abs((spans[k][0] + spans[k][1]) / 2 - gx))


def parse_amount(raw):
    """Like fcf_lib.parse_amount but never raises: returns (value or None, flags). Footnote markers
    such as '(*', '*)', ')*', '*(' or '(*)' are removed together with the ONE parenthesis that touches the
    star, before the sign is decided ('3,643)*' = +3,643 with a footnote; '(2,563))*' = -2,563)."""
    s = raw.replace(" ", "")
    flags = []
    if "*" in s:
        flags.append("asterisk")
        s = re.sub(r"\(\*+\)", "", s)
        s = re.sub(r"\)\*+|\*+\)|\(\*+|\*+\(", "", s, count=1)
        s = s.replace("*", "")
    if not s:
        return None, flags + ["empty"]
    if all(c in L.DASHES for c in s):
        return 0, flags
    neg = "(" in s or ")" in s
    body = s.replace("(", "").replace(")", "")
    if body and all(c in L.DASHES for c in body):
        return 0, flags
    if body and body[0] in L.DASHES and any(c.isdigit() for c in body):
        neg = True
        body = body[1:]
    elif body and body[-1] in L.DASHES and any(c.isdigit() for c in body):
        neg = True          # '17,553-' = visual-order rendering of '-17,553'
        body = body[:-1]
        flags.append("trailing-minus")
    body = body.replace(",", "")
    if not re.fullmatch(r"\d+(\.\d+)?", body):
        return None, flags + ["unparsed"]
    v = float(body) if "." in body else int(body)
    return (-v if neg else v), flags


PHRASE_START_RX = re.compile(r"^(?:ל-?)?(?:3|6|9|12)(?:-ל)?$|^(?:לתקופה|לתקופות|לשנה|שנה|לשלושה|לשישה|לששה|לתשעה|לשנת|"
                             r"three|six|nine|year|for)$", re.I)


def column_headers(hdr_lines, spans, centres, pitch, layout, xl, xr):
    """Assign header phrases to columns. Each header line is split into phrases at gaps wider than a
    normal word space and at the start of a new group header ('6 החודשים', 'לתקופה', 'לשנה' ...); a
    phrase applies to every column whose centre lies under it, and a phrase centred BETWEEN two columns
    (a group header such as 'לשלושה חודשים שהסתיימו ביום 31 במרס') applies to both."""
    out = {k: [] for k in range(len(spans))}
    if not spans:
        return out
    tol = max(3.0, 0.12 * pitch)
    for ln in sorted(hdr_lines, key=lambda x: x.yc):
        ws = sorted([w for w in ln.words if w.x1 > xl - 8 and w.x0 < xr + 8], key=lambda w: w.x0)
        if not ws:
            continue
        hgt = statistics.median([w.h for w in ws])
        thr = max(3.2, 0.5 * hgt)
        phrases, cur = [], [ws[0]]
        for w in ws[1:]:
            prev = cur[-1]
            start_split = (layout == "rtl" and PHRASE_START_RX.match(prev.text)
                           and not re.fullmatch(r"ל-?|-?ל|-|ל\u05be", w.text) and w.x0 - prev.x1 > 1.0) or \
                          (layout == "ltr" and PHRASE_START_RX.match(w.text))
            if w.x0 - prev.x1 > thr or start_split:
                phrases.append(cur)
                cur = [w]
            else:
                cur.append(w)
        phrases.append(cur)
        for ph in phrases:
            x0, x1 = min(w.x0 for w in ph), max(w.x1 for w in ph)
            xc = (x0 + x1) / 2
            ks = [k for k, c in enumerate(centres) if x0 - tol <= c <= x1 + tol]
            if not ks:
                order = sorted(range(len(centres)), key=lambda k: abs(centres[k] - xc))
                k1 = order[0]
                d1 = abs(centres[k1] - xc)
                if len(order) > 1:
                    k2 = order[1]
                    d2 = abs(centres[k2] - xc)
                    between = min(centres[k1], centres[k2]) < xc < max(centres[k1], centres[k2])
                    if between and abs(k1 - k2) == 1 and d1 > 0.28 * pitch and d2 > 0.28 * pitch:
                        ks = [k1, k2]
                if not ks and d1 <= 0.75 * pitch:
                    ks = [k1]
            txt = L.join_rtl(ph)
            if len(ks) >= 3 and len(centres) >= 3 and not re.search(r"מבוקר|audited", compact(txt), re.I):
                continue          # a statement-level line over all columns ('לתקופות של 6 ו-3 החודשים ...')
            for k in ks:
                out[k].append(txt)
    return {k: " ".join(v) for k, v in out.items()}


# ----------------------------------------------------------------------------- periods
EN_MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                           "september", "october", "november", "december"], start=1)}


def parse_period_header(text, report_q):
    """Months / period end / audit status / restated flag from a column's header text. Works on the
    compacted text (spaces removed), so that '2 0 2 6', 'ל ש נ ה' or '3-ל החודשים' are understood."""
    t = text.replace("\u2013", "-").replace("\u05be", "-").replace("(המשך)", "")
    c = compact(t)
    cl = c.lower()
    months, amb = None, False
    found = []
    m = re.search(r"(?:(?<!\d)|(?<=20\d\d))(3|6|9|12)-?ל?ה?חודשים", c) or re.search(r"ל-?(3|6|9|12)ה?חודשים", c)
    if m:
        found.append(int(m.group(1)))
    for w, n in (("שלושה", 3), ("שלושת", 3), ("שישה", 6), ("ששה", 6), ("ששת", 6), ("שישת", 6), ("תשעה", 9),
                 ("תשעת", 9)):
        if w in c:
            found.append(n)
    for w, n in (("three", 3), ("3months", 3), ("six", 6), ("6months", 6), ("nine", 9), ("9months", 9)):
        if w in cl:
            found.append(n)
    m2 = re.search(r"(?<!\d)(\d{1,2})-(\d{1,2})/(20\d\d)", c)       # '1-6/2026', '4-6/2026'
    if m2:
        found.append(int(m2.group(2)) - int(m2.group(1)) + 1)
    if found:
        months = found[0]
        amb = len(set(found)) > 1
    elif re.search(r"שנה|לשנת|שנתי|year|12חודשים", c, re.I):
        months = 12
    day = mon = year = None
    m = re.search(r"(?<!\d)(\d{1,2})[./](\d{1,2})[./](20\d\d)", c)
    if m:
        day, mon, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        md = re.search(r"(?<!\d)(\d{1,2}),?ב?(" + "|".join(L.HEB_MONTHS) + r")", c)
        if md:
            day, mon = int(md.group(1)), L.HEB_MONTHS[md.group(2)]
        else:
            mm = re.search(r"ב(" + "|".join(L.HEB_MONTHS) + r")", c)
            if mm:
                mon = L.HEB_MONTHS[mm.group(1)]
            me = re.search(r"(" + "|".join(EN_MONTHS) + r")(\d{1,2})?", cl)
            if me:
                mon = EN_MONTHS[me.group(1)]
                if me.group(2):
                    day = int(me.group(2))
        ys = re.findall(r"20\d\d", c)
        if ys:
            year = int(ys[-1])
            if len(set(ys)) > 1:
                amb = True
        if m2 and mon is None:
            mon, year = int(m2.group(2)), int(m2.group(3))
    if months == 12 and mon is None:
        day, mon = 31, 12
    if mon is None and months in (3, 6, 9):
        mon = {"Q1": 3, "Q2": 6, "Q3": 9}.get(report_q)
    if day is None and mon is not None:
        day = {3: 31, 6: 30, 9: 30, 12: 31}.get(mon)
    restated = bool(re.search(r"מוצגמחדש|הוצגמחדש|מוצגיםמחדש|מתוקן|מותאם|restated|asadjusted", c, re.I))
    audit = "בלתי מבוקר" if re.search(r"בלתימבוקר|unaudited", c, re.I) else (
        "מבוקר" if re.search(r"מבוקר|audited", c, re.I) else "")
    end = f"{year:04d}-{mon:02d}-{day:02d}" if (year and mon and day) else None
    return {"months": months, "end": end, "restated": restated, "audit": audit, "ambiguous": amb, "_year": year}


def infer_missing_periods(parsed, q, flags):
    """Fill gaps in the parsed column headers (flagged for review):
    - a column without months/end takes them from its pair partner (the adjacent column with the same
      kind of header but the other year, e.g. '2025' next to 'לשלושה חודשים ... 2026');
    - a year missing in a 12-month column = 2025 (the last annual period of a 2026 interim report);
    - months missing but end month known (interim) = months since the start of the calendar year."""
    out = [dict(p) for p in parsed]
    n = len(out)
    known = {(p.get("months"), p.get("end")) for p in parsed if p.get("months") and p.get("end")}
    for k, p in enumerate(out):
        if k > 0 and out[k - 1].get("months") and out[k - 1].get("end"):
            known.add((out[k - 1]["months"], out[k - 1]["end"]))     # period inferred for the previous column
        if p.get("months") and p.get("end"):
            continue
        txt_year = p.get("_year")
        partner = None
        # pair partner: an adjacent interim column; prefer the neighbour that does not produce a period that
        # already exists (c1/c2 = 6 months 2026/2025, c3 = '30 ביוני 2026' -> partner c4 = 3 months, not c2)
        cands = []
        for j in (k - 1, k + 1):
            if 0 <= j < n and out[j].get("months") and out[j].get("end") and out[j]["months"] != 12:
                pp = out[j]          # includes periods inferred earlier in this pass
                if p.get("end") is not None and p["end"][5:] != pp["end"][5:]:
                    continue
                if p.get("end"):
                    res_end = p["end"]
                else:
                    py = int(pp["end"][:4])
                    yr = txt_year or (py - 1 if k > j else py + 1)
                    res_end = f"{yr:04d}{pp['end'][4:]}"
                cands.append(((pp["months"], res_end) in known, (j, pp), res_end))
        if cands:
            cands.sort(key=lambda c: c[0])          # non-duplicating partner first (stable: left neighbour first)
            partner = cands[0][1]
        if not p.get("months") and partner:
            j, pp = partner
            p["months"] = pp["months"]
            if not p.get("end"):
                p["end"] = cands[0][2]
            known.add((p["months"], p["end"]))
            flags.append(f"עמודה c{k + 1}: חודשים/תאריך הוסקו מהעמודה הסמוכה – לאמת")
            continue
        if p.get("months") == 12 and not p.get("end"):
            p["end"] = "2025-12-31"
            flags.append(f"עמודה c{k + 1}: שנה לא זוהתה בכותרת – הונח 2025 – לאמת")
            continue
        if p.get("months") and not p.get("end"):
            qend = {"Q1": "03-31", "Q2": "06-30"}.get(q, "06-30")
            nb = [(j, out[j]) for j in (k - 1, k + 1) if 0 <= j < n and out[j].get("end")
                  and out[j].get("months") == p["months"]]
            if nb:
                j0, pp = nb[0]
                py = int(pp["end"][:4])
                yr = txt_year or (py - 1 if k > j0 else py + 1)
                p["end"] = f"{yr:04d}{pp['end'][4:]}"
            elif txt_year:
                p["end"] = f"{txt_year:04d}-{qend}"
            if p.get("end"):
                flags.append(f"עמודה c{k + 1}: תאריך סוף התקופה הוסק ({p['end']}) – לאמת")
                continue
        if not p.get("months") and p.get("end") and p["end"][5:] in ("03-31", "06-30", "09-30"):
            p["months"] = int(p["end"][5:7])
            flags.append(f"עמודה c{k + 1}: מספר החודשים לא צוין בכותרת – הונח {p['months']} (מתחילת השנה) – לאמת")
            continue
        if not p.get("months") and p.get("end") and p["end"][5:] == "12-31":
            p["months"] = 12
            flags.append(f"עמודה c{k + 1}: תקופה שמסתיימת ב-31.12 ללא ציון אורך – הונחה שנה – לאמת")
            continue
        if not p.get("months") and not p.get("end") and txt_year:
            mm = {"Q1": 3, "Q2": 6}.get(q, 3)
            p["months"], p["end"] = mm, f"{txt_year:04d}-{mm:02d}-{30 if mm == 6 else 31}"
            flags.append(f"עמודה c{k + 1}: לא זוהו חודשים/תאריך – הונח {mm} חודשים עד {p['end']} – לאמת")
    return out


# ----------------------------------------------------------------------------- units
EN_UNITS = [
    (r"(?:u\.?s\.?\s*)?dollars?\s+in\s+thousands|usd\s+in\s+thousands|in\s+thousands\s+of\s+(?:u\.?s\.?\s*)?dollars|"
     r"thousands\s+of\s+(?:u\.?s\.?\s*)?dollars|\$\s*in\s+thousands", 'דולר ארה"ב', "אלפים"),
    (r"(?:u\.?s\.?\s*)?dollars?\s+in\s+millions|in\s+millions\s+of\s+(?:u\.?s\.?\s*)?dollars", 'דולר ארה"ב', "מיליונים"),
    (r"eur(?:o)?\s+in\s+thousands|in\s+thousands\s+of\s+eur(?:o)?|eur\s*'?000|€\s*in\s+thousands", "אירו", "אלפים"),
    (r"pln\s+in\s+thousands|in\s+thousands\s+of\s+pln", "זלוטי פולני", "אלפים"),
    (r"(?:canadian\s+dollars|cad)\s+in\s+thousands|in\s+thousands\s+of\s+(?:canadian\s+dollars|cad)", "דולר קנדי", "אלפים"),
    (r"nis\s+in\s+thousands|in\s+thousands\s+of\s+nis", 'ש"ח', "אלפים"),
]


def detect_units(text):
    u = L.detect_units(text.replace("״", '"').replace("”", '"'))
    if u:
        return u
    tl = text.lower()
    for rx, cur, unit in EN_UNITS:
        m = re.search(rx, tl)
        if m:
            return {"units_text": text[m.start():m.end()], "currency": cur, "units": unit}
    return None


# ----------------------------------------------------------------------------- rows
def _label_edges(r, layout):
    """(outer, inner) x of a row's label: for RTL outer = right edge (start of text), inner = left end."""
    ws = r["label_words"]
    if not ws:
        return None, None
    if layout == "rtl":
        return max(w.x1 for w in ws), min(w.x0 for w in ws)
    return min(w.x0 for w in ws), max(w.x1 for w in ws)


def merge_rows(a):
    """Rows of one page -> logical rows (wrapped labels merged):
    0. a value row WITHOUT label text takes the text-only line(s) directly above and/or below it that are
       closer than ~0.9 line pitch (labels printed on two lines with the amounts centred between them);
    1. two text-only lines that together form a section heading ('תזרימי מזומנים מפעילות' + 'השקעה');
    2. 'before': a text-only line followed (within ~1.4 pitch) by a value line is merged into it when the
       text line runs (almost) up to the label column's inner edge (it wrapped because it was long), or the
       value line is indented, or the combined text is a section total;
    3. 'after': a long value line followed by an indented text-only continuation (not itself followed by a
       value line) gets that text appended."""
    rr = [dict(r) for r in a.rows if r["label"] or r["vals"]]
    pitch = a.pitch
    lay = a.layout
    inner_lim = a.label_inner
    lab_width = abs((a.label_edge or 0) - (inner_lim if inner_lim is not None else 0)) or 200.0

    def combine(parts, how):
        base = [p for p in parts if p["vals"]]
        base = base[0] if base else parts[-1]
        lw = [w for p in parts for w in p["label_words"]]
        return dict(base, label=L.normalize_label(" ".join(p["label"] for p in parts if p["label"])),
                    y0=min(p["y0"] for p in parts), y1=max(p["y1"] for p in parts),
                    x0=min(p["x0"] for p in parts), x1=max(p["x1"] for p in parts),
                    label_words=lw, wrapped=how, nlines=len(parts))

    def text_only(r):
        return not r["vals"] and bool(r["label"])

    def plain(r):
        return text_only(r) and not r["label"].endswith(":") and not is_heading_text(r)

    # pass 0: value rows without a label
    out0, i = [], 0
    while i < len(rr):
        r = rr[i]
        if r["vals"] and not r["label"]:
            parts = []
            below_ok = (i + 1 < len(rr) and plain(rr[i + 1]) and rr[i + 1]["yc"] - r["yc"] <= 0.9 * pitch)
            if out0 and text_only(out0[-1]) and not out0[-1]["label"].endswith(":"):
                gap = r["yc"] - out0[-1]["yc"]
                total_lab = bool(re.search(r"נטו|סה\"כ|סך|net|total", compact(out0[-1]["label"]), re.I))
                if (plain(out0[-1]) and gap <= 0.9 * pitch) or \
                        ((plain(out0[-1]) or total_lab) and not below_ok and gap <= 1.3 * pitch):
                    parts.append(out0.pop())
            parts.append(r)
            if below_ok:
                parts.append(rr[i + 1])
                i += 1
            out0.append(combine(parts, "centred") if len(parts) > 1 else dict(r, wrapped="", nlines=1))
            i += 1
            continue
        out0.append(dict(r, wrapped=r.get("wrapped", ""), nlines=r.get("nlines", 1)))
        i += 1
    rr = out0

    def indented(child, parent):
        co, _ = _label_edges(child, lay)
        po, _ = _label_edges(parent, lay)
        if co is None or po is None:
            return False
        return (po - co) >= 3.5 if lay == "rtl" else (co - po) >= 3.5

    def long_line(r):
        _, inner = _label_edges(r, lay)
        if inner is None or inner_lim is None:
            return False
        dist = (inner - inner_lim) if lay == "rtl" else (inner_lim - inner)
        return dist <= max(25.0, 0.22 * lab_width)

    def is_total_text(t):
        ct = compact(t)
        return any(rx.search(ct) for rx in SEC_RX.values()) and bool(TOTAL_WORD_RX.search(ct))

    out = []
    i = 0
    while i < len(rr):
        r = rr[i]
        lab = r["label"]
        nxt = rr[i + 1] if i + 1 < len(rr) else None
        # 1. heading wrapped over two text-only lines
        if nxt is not None and text_only(r) and text_only(nxt) and nxt["yc"] - r["yc"] <= 1.4 * pitch:
            cj = compact(lab + " " + nxt["label"])
            if any(rx.search(cj) for rx in SEC_RX.values()) and not any(rx.search(compact(lab)) for rx in SEC_RX.values()) \
                    and not any(rx.search(compact(nxt["label"])) for rx in SEC_RX.values()):
                out.append(combine([r, nxt], "heading"))
                i += 2
                continue
        # 2. 'before'
        if (nxt is not None and plain(r) and nxt["vals"] and nxt["label"] and nxt["yc"] - r["yc"] <= 1.4 * pitch
                and not is_heading_text(nxt)
                and (long_line(r) or indented(nxt, r) or (is_total_text(lab + " " + nxt["label"])
                                                           and not is_total_text(nxt["label"])))):
            out.append(combine([r, nxt], "before"))
            i += 2
            continue
        # 3. 'after'
        if (nxt is not None and r["vals"] and plain(nxt) and nxt["yc"] - r["yc"] <= 1.15 * pitch
                and indented(nxt, r) and long_line(r)
                and not (i + 2 < len(rr) and rr[i + 2]["vals"] and rr[i + 2]["yc"] - nxt["yc"] <= 1.4 * pitch)):
            out.append(combine([r, nxt], "after"))
            i += 2
            continue
        out.append(r)
        i += 1
    return out


def is_heading_text(r):
    ct = compact(r["label"])
    if r["vals"] and not all(v == 0 for _, v in r["vals"].values()):
        return False
    if re.search(r"נטו|net|סה\"כ|סך|total", ct, re.I):
        return False          # a section total (possibly with dashes only, or with its amounts on the next line)
    if any(rx.search(ct) for rx in SEC_RX.values()) and re.search(r"תזרימי|תזרים|מזומנים|cashflow|^פעילו|^מפעילו",
                                                                  ct, re.I):
        return True
    return bool(NONCASH_RX.search(ct)) and not r["vals"]


# ----------------------------------------------------------------------------- items (suggestion)
def suggest_item(label):
    """Suggestion only (the Phase B review decides). Returns (item, note)."""
    t = label.replace("פירעון", "פרעון").replace("״", '"').replace("”", '"')
    tl = t.lower()
    if re.search(r"[a-z]", tl) and not re.search(r"[א-ת]", t):
        return suggest_item_en(tl)
    nci = bool(re.search(r"שאינן מקנות שליטה|שאינה מקנה שליטה|מיעוט|שאינן מקנות|זשמ\"ש|זשמ\"ש|זכויות שאינן", t))
    if re.search(r"ריבית|ריביות", t) and re.search(r"ששולמה|ששולמו|שולמה|תשלום|תשלומי", t) and "שהתקבל" not in t:
        return 13, ""
    if re.search(r"דיבידנד|חלוקת רווחים|חלוקה|חלוקות|משיכות", t) and nci:
        return 12, ""
    if re.search(r"דיבידנד|חלוקת רווחים|חלוקה לבעלי|חלוקות לבעלי|חלוקה לשותפים|חלוקות לשותפים|"
                 r"חלוקות? (?:ה)?בעלים|משיכות (?:ה)?שותפים", t):
        return 11, ""
    if nci and re.search(r"רכישה|רכישת|רכישות", t):
        return 14, ""
    if nci:
        return 6, ""
    if re.search(r"(?:הקצאת|הנפקת|הנפקה של) מניות (?:ב|של )?(?:ה)?(?:חברת|חברה|חברות) (?:ה)?(?:בת|בנות)", t):
        return 6, "הנפקת/הקצאת מניות בחברה בת למשקיעים חיצוניים – סעיף 6 (לבדיקה)"
    if re.search(r"אופציות|אופציה|כתבי אופציה|כ\"א", t):
        return 2, ""
    if re.search(r"מניות אוצר|מניות באוצר|מניות רדומות|רכישה עצמית|רכישת מניות החברה|רכישת מניות(?! ב)", t):
        return 9, ""
    if "חכירה" in t or "חכירות" in t:
        return 10, ""
    bonds = re.search(r"אגרות חוב|אג\"ח|אגרות-חוב|נע\"מ|ניירות ערך מסחריים|אגרת חוב", t)
    if bonds:
        rec = re.search(r"הנפקת|הנפקה|תמורה|גיוס|קבלת|הרחבת", t)
        rep = re.search(r"פרעון|רכישה|רכישת|פדיון|פירעונות|פרעונות", t)
        if rec and rep:
            return "net_bonds", "שורה נטו – סיווג לפי סימן"
        if rep:
            return 8, ""
        return 3, ""
    if re.search(r"הנפקת מניות|הנפקת הון|הנפקות הון|הנפקה של מניות|הנפקה ראשונה של מניות|הנפקת יחידות|הון מניות|"
                 r"תקבולים על חשבון מניות", t):
        return 1, ""
    if re.search(r"הנפקת חבילה|הנפקת חבילות", t):
        return 1, "הנפקת חבילה (מניות + ניירות נלווים) – סעיף 1 אם התמורה לא פוצלה בדוח (לבדיקה)"
    if re.search(r"השקע(?:ת|ות) (?:ה)?בעלים|הון (?:ה)?שותפים|הפקדות (?:ה)?שותפים|השקעות? (?:ה)?שותפים|"
                 r"הזרמת הון|הזרמות הון|השקעות? הון", t):
        return 1, "השקעת בעלים/שותפים בהון – סעיף 1 (לבדיקה)"
    long_term = bool(re.search(r"ל?זמן ארוך", t))
    if re.search(r"ל?זמן קצר", t) or ("אשראי" in t and not long_term):
        return 5, ""
    if re.search(r"הלוואה|הלוואות|הלוואת|התחייבות|התחייבויות|אשראי|מימון", t):
        rec = re.search(r"קבלת|קבלה|התקבלו|נטילת|תמורה|שהתקבלו|גיוס|תקבול", t)
        rep = re.search(r"פרעון|החזר|פרעונות", t)
        if rec and rep:
            if long_term:
                return "net_loans", "שורה נטו – סיווג לפי סימן"
            return 5, "שורה נטו (קבלה/פירעון) ללא ציון תקופה – סעיף 5 לפי כלל המיפוי (לבדיקה)"
        if rep:
            return 7, ""
        if rec:
            return 4, ""
        if "נטו" in t or re.search(r"שינוי|קיטון|גידול|עלי(?:י)?ה|ירידה", t):
            if long_term:
                return "net_loans", "שינוי נטו בהלוואות לזמן ארוך – סיווג לפי סימן (לבדיקה)"
            return 5, "הלוואות נטו / שינוי בהלוואות ללא ציון תקופה – סעיף 5 (לבדיקה)"
    return "other", "לבדיקה ידנית"


def suggest_item_en(t):
    if "interest" in t and "paid" in t:
        return 13, ""
    if ("dividend" in t or "distribution" in t) and ("non-controlling" in t or "noncontrolling" in t or "minority" in t):
        return 12, ""
    if "dividend" in t or "distribution" in t:
        return 11, ""
    if "non-controlling" in t or "noncontrolling" in t or "minority" in t:
        return (14, "") if ("acquisition" in t or "purchase" in t) else (6, "")
    if "option" in t or "warrant" in t:
        return 2, ""
    if "treasury" in t or "buyback" in t or "repurchase of shares" in t:
        return 9, ""
    if "lease" in t:
        return 10, ""
    if "bond" in t or "debenture" in t or "notes" in t:
        if "issu" in t or "proceeds" in t:
            return 3, ""
        return 8, ""
    if "issuance of shares" in t or "share capital" in t or "issue of shares" in t or "units" in t:
        return 1, ""
    if "short-term" in t or "short term" in t or "credit" in t:
        return 5, ""
    if "loan" in t or "borrowing" in t:
        if ("receipt" in t or "proceeds" in t) and "repayment" in t:
            return "net_loans", "net line – by sign"
        if "repayment" in t or "repaid" in t:
            return 7, ""
        if "receipt" in t or "proceeds" in t or "received" in t:
            return 4, ""
    return "other", "לבדיקה ידנית"


INT_PAID_RX = re.compile(r"ריבית.*(?:ששולמה|ששולמו|שולמה|תשלומי)|(?:ששולמה|ששולמו).*ריבית|interestpaid|paidinterest", re.I)
DIV_PAID_RX = re.compile(r"(?:דיבידנד|חלוק).*(?:ששולם|ששולמו|שולם|שולמו|לבעלי)|dividendspaid|dividendpaid|paiddividend",
                         re.I)
RECEIVED_RX = re.compile(r"שהתקבל|התקבלו|received", re.I)
CAP_INT_RX = re.compile(r"עלויותאשראישהוונו|ריביתשהוונה|ריביתשהוונו|capitalizedinterest|borrowingcostscapitalized", re.I)
APPENDIX_SECTION = "נספח לדוח תזרים המזומנים (מחוץ לפעילות מימון)"


def malformed_number(s):
    """True for a printed amount whose thousands grouping is irregular ('280,68', '7,985965', '1,23,456'),
    which usually means a digit is missing / duplicated in the source or the text layer."""
    core = re.sub(r"[()\s*\-–−]", "", str(s))
    if not core or not any(c.isdigit() for c in core) or "," not in core:
        return False
    core = core.split(".")[0]
    return not re.fullmatch(r"\d{1,3}(?:,\d{3})+", core)


# ----------------------------------------------------------------------------- main extraction
def extract(path, issuer, q, folder, fname, pages=None, fin_pages_force=None):
    doc = pymupdf.open(path)
    flags, log = [], []
    scans = [PageScan(doc[i], i + 1) for i in range(doc.page_count)]
    pick, cands = find_statement(scans, folder)
    log.append("statement blocks: " + "; ".join(
        f"{c['pages']} cons={c['cons']} solo={c['solo']} board={c['board']} notes={c['notes']} op={c['op']} "
        f"inv={c['inv']} finH={c['fin_head']} finT={c['fin_total']} cashEnd={c['cash_end']} num={c['numeric']} "
        f"complete={c['complete']} strong={c['strong']} score={c['score']:.1f}"
        for c in cands))
    if pages is None:
        if not pick:
            return {"error": "no consolidated cash-flow statement found", "log": log, "scans": [s.summary() for s in scans]}
        pages = pick["pages"]
        if not pick["cons"]:
            flags.append("כותרת הדוח אינה כוללת 'מאוחד' – לוודא שזה הדוח המאוחד (או חברה ללא חברות בנות)")
        if pick["notes"]:
            flags.append("כותרת העמוד (כותרת רצה) מציינת 'באורים' – לוודא שזה הדוח המאוחד על תזרימי המזומנים")
        if not pick["strong"]:
            flags.append("מבנה הדוח לא זוהה במלואו (שוטפת/השקעה/מימון) – לוודא את עמודי הדוח")
        if not pick.get("first_strong", True):
            first = [c for c in cands if c["strong"] and not c["solo"] and not c["board"]]
            flags.append(f"נבחר הדוח בעמודים {pick['pages']} ולא דוח קודם בקובץ "
                         f"({first[0]['pages'] if first else '-'}) – לוודא שזה הדוח המאוחד של החברה")
    other = [c for c in cands if c.get("complete") and c["pages"] != pages]
    solo_pages = [p for c in cands if c["solo"] for p in c["pages"]]
    board_pages = [p for c in cands if c["board"] for p in c["pages"]]
    # analyse pages (span hint = page with most columns)
    an = {}
    for p in pages:
        an[p] = analyse(scans[p - 1])
    best = max(pages, key=lambda p: (len(an[p].spans), an[p].scan.n_numeric))
    for p in pages:
        if len(an[p].spans) < len(an[best].spans):
            an[p] = analyse(scans[p - 1], spans_hint=[list(s) + [0] for s in an[best].spans])
    # logical rows per page with sections
    rows_all = []
    section = None
    for p in pages:
        a = an[p]
        order = sorted(range(len(a.spans)), key=lambda k: -a.centres[k]) if a.layout == "rtl" else \
            list(range(len(a.spans)))
        a.order = order
        for r in merge_rows(a):
            ct = compact(r["label"])
            lab = r["label"]
            nz = [v for _, v in r["vals"].values() if v is not None]
            if is_heading_text(r) and not (r["vals"] and any(nz)):
                sec = None
                for k, rx in SEC_RX.items():
                    if rx.search(ct):
                        sec = k
                if sec is None and NONCASH_RX.search(ct):
                    sec = "noncash"
                section = sec or section
                kind = "heading"
                # a heading row that carries dash values = the section total when the section is empty
                if r["vals"] and sec == "financing":
                    kind = "heading_total"
            elif not r["vals"] and NONCASH_RX.search(ct):
                section = "noncash"
                kind = "heading"
            elif r["vals"] and any(rx.search(ct) for rx in SEC_RX.values()) and TOTAL_WORD_RX.search(ct):
                kind = "section_total"
            elif r["vals"]:
                kind = "line"
            else:
                kind = "text"
            vals = [None] * len(a.spans)
            raws = [None] * len(a.spans)
            for k, (raw, v) in r["vals"].items():
                j = order.index(k)
                vals[j], raws[j] = v, L.display_raw(raw)
            sec_tot = None
            if kind == "section_total":
                for k, rx in SEC_RX.items():
                    if rx.search(ct):
                        sec_tot = k
            rows_all.append({"page": p, "label": lab, "kind": kind, "section": section, "sec_total": sec_tot,
                             "bbox": [round(min(r["x0"], a.content_x[0]) if a.layout == "ltr" else r["x0"], 2),
                                      round(r["y0"], 2), round(r["x1"], 2), round(r["y1"], 2)],
                             "values": vals, "raw": raws, "unparsed": r["unparsed"], "wrapped": r["wrapped"],
                             "stars": sorted(order.index(k) for k in r.get("stars", ()) if k in order)})
            if kind == "section_total" and sec_tot == "financing":
                section = "post"
    # ---------------- financing section
    fin, in_fin, fin_heading = [], False, None
    for idx, r in enumerate(rows_all):
        if r["kind"] in ("heading", "heading_total") and r["section"] == "financing" and fin_heading is None:
            fin_heading = r
            in_fin = True
            if r["kind"] == "heading_total":
                fin.append(dict(r, kind="section_total"))
                break
            continue
        if in_fin:
            if r["kind"] == "heading" and r["section"] != "financing":
                break
            fin.append(r)
            if r["kind"] == "section_total" and r["sec_total"] == "financing":
                break
    if fin_heading is None:
        # no heading: lines after the investing total up to the financing total
        tot_i = [i for i, r in enumerate(rows_all) if r["kind"] == "section_total" and r["sec_total"] == "financing"]
        inv_i = [i for i, r in enumerate(rows_all) if r["kind"] == "section_total" and r["sec_total"] == "investing"]
        if tot_i:
            start = (inv_i[0] + 1) if inv_i and inv_i[0] < tot_i[0] else tot_i[0]
            fin = rows_all[start:tot_i[0] + 1]
            fin_heading = dict(rows_all[start], label=rows_all[start]["label"])
            flags.append("לא נמצאה כותרת 'פעילות מימון' – הסעיף נקבע מסוף פעילות ההשקעה ועד הסה\"כ")
        else:
            return {"error": "financing section not found", "log": log, "pages": pages,
                    "rows": [{k: r[k] for k in ("page", "label", "kind", "section", "values")} for r in rows_all]}
    totals = [r for r in fin if r["kind"] == "section_total"]
    if not totals:
        flags.append("לא נמצאה שורת סה\"כ של פעילות המימון")
    # ---------------- columns (header text of the financing page, else of the statement's first page)
    fp = fin_heading["page"] if fin_heading else fin[0]["page"]
    hp = fp
    pinfo = an[fp]
    hdr_texts = [pinfo.col_headers.get(k, "") for k in pinfo.order]
    parsed = [parse_period_header(h, q) for h in hdr_texts]
    if not all(x["months"] and x["end"] for x in parsed) or not hdr_texts:
        for p in pages:
            a = an[p]
            if len(a.spans) != len(pinfo.spans):
                continue
            ht = [a.col_headers.get(k, "") for k in a.order]
            ps = [parse_period_header(h, q) for h in ht]
            if all(x["months"] and x["end"] for x in ps):
                hp, hdr_texts, parsed = p, ht, ps
                break
    ncol = len(pinfo.spans)
    parsed = infer_missing_periods(parsed, q, flags)
    columns = []
    for k in range(ncol):
        per = parsed[k] if k < len(parsed) else {"months": None, "end": None, "restated": False, "audit": "",
                                                 "ambiguous": False}
        amb = per.pop("ambiguous", False)
        per.pop("_year", None)
        lab = period_label(per["months"], per["end"], per["restated"]) if per["months"] and per["end"] else None
        columns.append({"key": f"c{k + 1}", "header_text": hdr_texts[k] if k < len(hdr_texts) else "", **per,
                        "label": lab})
        if not lab:
            flags.append(f"עמודה c{k + 1}: לא זוהו חודשים/תאריך מכותרת העמודה ('{hdr_texts[k] if k < len(hdr_texts) else ''}')")
        elif amb:
            flags.append(f"עמודה c{k + 1}: כותרת עמודה דו-משמעית ('{hdr_texts[k]}') – לאמת חודשים/תאריך")
    ends = [(c["months"], c["end"]) for c in columns]
    if len(set(ends)) != len(ends):
        flags.append("שתי עמודות עם אותה תקופה – לבדוק את כותרות העמודות")
    exp_end = "2026-03-31" if q == "Q1" else "2026-06-30"
    if not any(c["end"] == exp_end for c in columns):
        flags.append(f"אין עמודה שמסתיימת ב-{exp_end}")
    odd = [c["key"] for c in columns if c["end"] and c["end"][5:] not in ("03-31", "06-30", "09-30", "12-31")]
    if odd:
        flags.append(f"תאריך סוף תקופה חריג בעמודות {odd} – לאמת מול הדוח")
    # ---------------- units
    units = None
    for p in [hp] + pages:
        units = detect_units(an[p].above_text)
        if units:
            break
    if not units:
        for p in pages:
            units = detect_units(" | ".join(scans[p - 1].texts))
            if units:
                break
    if not units:
        p0 = pages[0]
        for p in range(p0 - 1, max(0, p0 - 6), -1):
            units = detect_units(" | ".join(scans[p - 1].texts))
            if units:
                flags.append(f"יחידות זוהו מעמוד {p} (לפני הדוח) – לאמת")
                break
    if not units:
        flags.append("יחידות/מטבע לא זוהו")
    # ---------------- outside (*) lines
    outside = []
    not_paid = re.compile(r"טרם|לשלם|שהוכרז|הוכרז|שלאשולמ|payable|declared", re.I)

    def paid_context(i):
        """The nearest heading/text row above (within 6 rows) that says 'paid' or 'received' decides
        ('מזומנים ששולמו במשך התקופה עבור: ריבית' vs 'מזומנים שהתקבלו ...: ריבית')."""
        for x in reversed(rows_all[max(0, i - 6):i]):
            if x["kind"] not in ("text", "heading"):
                continue
            cx = compact(x["label"])
            if re.search(r"שהתקבלו|התקבלו|received", cx, re.I):
                return False
            if re.search(r"ששולמו|שולמו|paid", cx, re.I):
                return True
        return False

    for i, r in enumerate(rows_all):
        if r in fin or r["kind"] != "line" or r["section"] not in ("operating", "investing"):
            continue
        ct = compact(r["label"])
        if not_paid.search(ct):
            continue                  # 'דיבידנד שהוכרז וטרם שולם', 'ריבית לשלם' – not a payment
        is_int = bool(INT_PAID_RX.search(ct)) and not RECEIVED_RX.search(ct)
        if not is_int and re.match(r"^(?:ריבית|interest)", ct, re.I) and paid_context(i) \
                and not RECEIVED_RX.search(ct):
            is_int = True
            flags.append(f"(*) ריבית בשורה '{r['label']}' זוהתה לפי כותרת 'ששולמו' – לאמת")
        if not is_int and CAP_INT_RX.search(ct):
            is_int = True
            flags.append(f"(*) ריבית שהוונה '{r['label']}' – לאמת שמדובר בריבית ששולמה")
        is_div = bool(DIV_PAID_RX.search(ct)) and not RECEIVED_RX.search(ct)
        if not is_div and re.match(r"^(?:דיבידנד|dividend)", ct, re.I) and paid_context(i) \
                and not RECEIVED_RX.search(ct):
            is_div = True
        if is_int or is_div:
            outside.append({"info": "interest" if is_int else "dividend",
                            "section": {"operating": L.SECTION_OPERATING, "investing": L.SECTION_INVESTING}[r["section"]],
                            "page": r["page"], "text": r["label"], "values": r["values"], "raw": r["raw"],
                            "bbox": r["bbox"]})
    # interest / dividends paid disclosed only in an appendix of the statement ('נספח – ריבית ומסים במזומן'):
    # candidates when neither the financing section nor the operating/investing sections show such a line
    fin_items = {suggest_item(r["label"])[0] for r in fin if r["kind"] == "line"}
    for kind, its, rx in (("interest", {13}, INT_PAID_RX), ("dividend", {11, 12}, DIV_PAID_RX)):
        if fin_items & its or any(o["info"] == kind for o in outside):
            continue
        word = r"^(?:ריבית|interest)" if kind == "interest" else r"^(?:דיבידנד|dividend)"
        for i, r in enumerate(rows_all):
            if r in fin or r["kind"] != "line" or r["section"] not in ("post", "noncash"):
                continue
            ct = compact(r["label"])
            paid = rx.search(ct) or (re.match(word, ct, re.I) and paid_context(i))
            if paid and not RECEIVED_RX.search(ct) and not not_paid.search(ct) and any(v for v in r["values"] if v):
                outside.append({"info": kind, "section": APPENDIX_SECTION, "page": r["page"], "text": r["label"],
                                "values": r["values"], "raw": r["raw"], "bbox": r["bbox"]})
                flags.append(f"(*) {'ריבית' if kind == 'interest' else 'דיבידנד'} ששולמ/ה מגולה רק בנספח לדוח "
                             f"('{r['label']}', עמ' {r['page']}) – לאמת שאינה בפעילות המימון ולקבוע את הערת הסעיף")
                break
    # ---------------- lines out
    lines_out = []
    for n, r in enumerate(fin, start=1):
        lfl = []
        if r["kind"] == "section_total":
            item, note = "total", ""
        elif r["kind"] == "line" and re.match(r'^(?:סה"כ|סה״כ|סך הכל|סך הכול|total)', r["label"], re.I):
            item, note = "subtotal", ""
        elif r["kind"] == "line":
            item, note = suggest_item(r["label"])
        else:
            item, note = "text", "שורת טקסט ללא ערכים"
        vals = list(r["values"])
        if r["kind"] in ("line", "section_total") and any(v is None for v in vals):
            if all(v is None for v in vals):
                lfl.append("אין ערכים")
            else:
                lfl.append("תא ריק – נרשם 0 (לאמת)")
                vals = [0 if v is None else v for v in vals]
        if r["unparsed"]:
            lfl.append(f"ערכים שלא פוענחו: {r['unparsed']}")
        if r["wrapped"]:
            lfl.append(f"תווית בשתי שורות ({r['wrapped']})")
        if r.get("stars"):
            lfl.append("ערך מסומן בכוכבית (הערת שוליים) בעמודות " + ", ".join(f"c{k + 1}" for k in r["stars"]))
        bad_fmt = [f"c{k + 1} '{s}'" for k, s in enumerate(r.get("raw") or []) if s and malformed_number(s)]
        if bad_fmt:
            lfl.append("מספר בפורמט חריג (קבוצת ספרות שאינה בת 3 – ספרה חסרה/עודפת בדוח?) – לבדוק: " + ", ".join(bad_fmt))
        if isinstance(item, int):
            if item in (1, 2, 3, 4, 6) and any((v or 0) < 0 for v in vals):
                lfl.append("סימן שלילי בשורת תקבול – לבדוק סיווג (שורה נטו?)")
            if item in (7, 8, 9, 10, 11, 12, 13, 14) and any((v or 0) > 0 for v in vals):
                lfl.append("סימן חיובי בשורת תשלום – לבדוק סיווג (שורה נטו?)")
        lines_out.append({"n": n, "page": r["page"], "text": r["label"], "item": item, "note": note,
                          "values": vals, "raw": r["raw"], "bbox": r["bbox"], "flags": lfl})
    fin_pages = sorted(set(r["page"] for r in fin) | {fin_heading["page"]})
    # vertical limits around the financing rows per page (for crops)
    fin_limits = {}
    fin_ids = {id(r) for r in fin} | {id(fin_heading)}
    for p in fin_pages:
        prow = [r for r in rows_all if r["page"] == p]
        idx = [i for i, r in enumerate(prow) if id(r) in fin_ids or (r is fin_heading)]
        if not idx:
            continue
        top = prow[idx[0] - 1]["bbox"][3] if idx[0] > 0 else an[p].header_y[1]
        bot = prow[idx[-1] + 1]["bbox"][1] if idx[-1] + 1 < len(prow) else an[p].H * 0.95
        fin_limits[str(p)] = [top, bot]
    context_sections = {}
    for r in rows_all:
        if r["kind"] in ("line", "section_total", "heading") and r["section"] in ("operating", "investing", "noncash"):
            nm = {"operating": L.SECTION_OPERATING, "investing": L.SECTION_INVESTING,
                  "noncash": "פעילויות שלא במזומן"}[r["section"]]
            lst = context_sections.setdefault(str(r["page"]), [])
            if nm not in lst:
                lst.append(nm)
    page_info = {}
    for p in pages:
        a = an[p]
        page_info[str(p)] = {
            "ncol": len(a.spans), "layout": a.layout,
            "spans": [list(a.spans[k]) for k in a.order],
            "headers": [a.col_headers.get(k, "") for k in a.order],
            "title_text": a.title_text, "title_y": a.title_y, "header_y": a.header_y, "header_x": a.header_x,
            "content_x": a.content_x, "printed_page": a.printed_page,
            "first_body_y0": min([r["y0"] for r in a.rows], default=None),
            "label_right_limit": a.values_x[1], "label_right_edge": a.label_edge, "pitch": a.pitch,
            "page_rect": [a.W, a.H],
        }
    # sanity flags
    tot = [ln for ln in lines_out if ln["item"] == "total"]
    if len(tot) == 1:
        for k in range(ncol):
            s = sum((ln["values"][k] or 0) for ln in lines_out if ln["item"] not in ("total", "subtotal", "text"))
            t = tot[0]["values"][k]
            if t is not None and abs(s - t) > 1e-6:
                flags.append(f"C1 אוטומטי: עמודה c{k + 1} סכום השורות {s} ≠ סה\"כ {t}")
    if any(ln["item"] == "other" for ln in lines_out):
        flags.append("יש שורות ללא הצעת סיווג ('אחר'/לבדיקה)")
    if any(ln["item"] == "subtotal" for ln in lines_out):
        flags.append("יש סיכומי ביניים בסעיף המימון")
    alltxt = "".join(compact(" ".join(scans[p - 1].texts)) for p in pages)
    if re.search(r"הוצגמחדש|מוצגמחדש|מוצגיםמחדש|הוצגומחדש|restated", alltxt, re.I):
        flags.append("בעמודי הדוח מופיע 'הוצג מחדש' – לבדוק אם עמודות/ערכים מוצגים מחדש (סימון מוצג מחדש)")
    if len(other):
        flags.append("דוחות נוספים בקובץ (סולו/מוחזקות וכד') בעמודים: " + "; ".join(str(c["pages"]) for c in other))
    layouts = sorted({an[p].layout for p in pages})
    out = {
        "issuer": str(issuer), "company_folder": folder, "company_name": L.restore_quotes(folder.split(" - ", 1)[1]),
        "quarter": q, "report_label": f"{q} 2026",
        "report_id": re.search(r"_(\d+)(?:-\d+)?\.pdf$", fname).group(1),
        "source_file": fname, "page_count": doc.page_count,
        "cf_pages": pages, "fin_pages": fin_pages, "header_page": hp,
        "fin_heading": {"page": fin_heading["page"], "text": fin_heading["label"], "bbox": fin_heading["bbox"]},
        "units": units, "columns": columns, "lines": lines_out,
        "outside": outside,
        "page_info": page_info,
        "fin_limits": fin_limits,
        "context_sections": context_sections,
        "other_cf_pages": {"solo": solo_pages, "board": board_pages},
        "layout": layouts[0] if len(layouts) == 1 else "mixed",
        "flags": flags,
        "all_rows": [{k: r[k] for k in ("page", "label", "kind", "section", "values", "bbox")} for r in rows_all],
        "log": log,
    }
    doc.close()
    return out


def period_label(months, end_iso, restated=False):
    return L.period_label(months, end_iso, restated)
