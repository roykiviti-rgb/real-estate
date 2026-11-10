# -*- coding: utf-8 -*-
"""fcf_lib — shared helpers for the financing-cash-flow breakdown (generic, reusable for all companies).

Never writes to source PDFs: documents are opened read-only and only rendered.
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import statistics  # noqa: E402

import pymupdf  # noqa: E402

# ----------------------------------------------------------------------------- paths
WORK = os.path.dirname(os.path.abspath(__file__))
GOAL_DIR = os.path.dirname(WORK)
WORKSPACE = os.path.dirname(os.path.dirname(GOAL_DIR))
DATA_DIR = os.path.join(WORK, "data")
OVERRIDES_DIR = os.path.join(WORK, "overrides")
VERIFY_DIR = os.path.join(WORK, "verify")
ROLES_PATH = os.path.join(WORK, "roles.json")
# Scratch space OUTSIDE the WORKSPACE. Layout (parallel-safe):
#   %TEMP%\fcf_run\<issuer>\...        everything produced for one company (review files, renders, tmp outputs)
#   %TEMP%\fcf_run\_runs\<tag>_<pid>\  per-invocation results of multi-company commands (checks, validate, ...)
TEMP_BASE = os.path.join(os.environ.get("TEMP") or os.environ.get("TMP") or os.path.expanduser("~"), "fcf_run")
MASTER_NAME = "סיכום פירוט תזרים מימון 2026 - כל החברות.xlsx"


def temp_dir(*parts):
    """Create and return a scratch folder under %TEMP%\\fcf_run (e.g. temp_dir('1618') or temp_dir('1618', 'review'))."""
    p = os.path.join(TEMP_BASE, *[str(x) for x in parts])
    os.makedirs(p, exist_ok=True)
    return p


def run_dir(tag):
    """Per-invocation scratch folder for multi-company commands: %TEMP%\\fcf_run\\_runs\\<tag>_<yyyymmdd-hhmmss>_<pid>."""
    import time
    return temp_dir("_runs", f"{tag}_{time.strftime('%Y%m%d-%H%M%S')}_{os.getpid()}")

# ----------------------------------------------------------------------------- labels (exact, from goal.md R3/R5/R6)
ITEMS = [
    (1, "הנפקת מניות, בניכוי עלויות הנפקה"),
    (2, "מימוש אופציות / כתבי אופציה"),
    (3, 'הנפקת אגרות חוב (כולל אג"ח להמרה)'),
    (4, "קבלת הלוואות לזמן ארוך"),
    (5, "אשראי לזמן קצר מתאגידים בנקאיים, נטו"),
    (6, "השקעת בעלי זכויות שאינן מקנות שליטה בחברה בת"),
    (7, "פירעון הלוואות לזמן ארוך"),
    (8, "פירעון אגרות חוב"),
    (9, "רכישה עצמית של מניות"),
    (10, "פירעון קרן התחייבויות בגין חכירה"),
    (11, "דיבידנד ששולם לבעלי המניות (*)"),
    (12, "דיבידנד ששולם לבעלי זכויות שאינן מקנות שליטה"),
    (13, "ריבית ששולמה (*)"),
    (14, "רכישת זכויות נוספות בחברה בת ללא שינוי בשליטה"),
]
ITEM_LABEL = dict(ITEMS)
OTHER_LABEL = "אחר"
TOTAL_LABEL = "סך תזרים מזומנים מפעילות מימון"
GROUP_IN = "התקבלויות (+)"
GROUP_OUT = "תשלומים (\u2212)"
CHECK_LABEL = 'בדיקה: סכום הסעיפים פחות הסה"כ המדווח'
INFO_INT_LABEL = "(*) ריבית ששולמה שסווגה מחוץ לפעילות מימון (לידיעה בלבד)"
INFO_DIV_LABEL = "(*) דיבידנד ששולם שסווג מחוץ לפעילות מימון (לידיעה בלבד)"
NOT_SEPARATE_NOTE = "לא מוצג בנפרד בדוח תזרים המזומנים"
SUBTOTAL_TAG = "סיכום ביניים \u2013 לא נכלל"
OUTSIDE_TAG = "לידיעה \u2013 מחוץ לפעילות מימון"
MISSING_Q1_TEXT = "דוח Q1 2026 אינו קיים בתיקייה"
ROLE_MAIN = "מקור הנתונים \u2013 דוח רבעוני"
SECTION_OPERATING = "פעילות שוטפת"
SECTION_INVESTING = "פעילות השקעה"
# canonical sections of the (*) lines (Phase C alignment E, conventions §1)
SECTION_APPX_OPERATING = "גילוי בנספח לדוח תזרימי המזומנים \u2013 נכלל בפעילות שוטפת"
SECTION_APPX_INVESTING = "גילוי בנספח לדוח תזרימי המזומנים \u2013 נכלל בפעילות השקעה"
SECTION_APPX_UNSTATED = "גילוי בנספח לדוח תזרימי המזומנים \u2013 הסעיף לא צוין (לא בפעילות מימון)"
STAR_SECTIONS = (SECTION_OPERATING, SECTION_INVESTING, SECTION_APPX_OPERATING, SECTION_APPX_INVESTING,
                 SECTION_APPX_UNSTATED)
# the extractor's generic label of a (*) line found in an appendix (= fcf_extract.APPENDIX_SECTION); finalize maps it
# to SECTION_APPX_UNSTATED unless outside_sections states the section
SECTION_APPX_AUTO = "נספח לדוח תזרים המזומנים (מחוץ לפעילות מימון)"


STAR_SIGN_REMARK = {   # orchestrator decision D3 (iteration 2, M5): remark on a (*) line recorded with the payment sign
    "interest": "מודפס ללא סוגריים (חיובי) ונרשם כאן בסימן תשלום (שלילי) כדי ששורת (*) הריבית תציג את סך הריבית "
                "ששולמה מחוץ לפעילות המימון (ראו 'הסבר' – (*) סימן)",
    "dividend": "מודפס ללא סוגריים (חיובי) ונרשם כאן בסימן תשלום (שלילי) כדי ששורת (*) הדיבידנד תציג את סך הדיבידנד "
                "ששולם מחוץ לפעילות המימון (ראו 'הסבר' – (*) סימן)",
}


def star_mapping_note(o):
    """Mapping-sheet note of a (*) line: where the report classifies / discloses it; for a line whose printed positive
    amount is recorded with the payment sign (override flag "sign_flipped", decision D3) the sign remark is appended."""
    note = f"מסווג בדוח ב{o['section']}" if o["section"] in (SECTION_OPERATING, SECTION_INVESTING) else o["section"]
    if o.get("sign_flipped"):
        note += "; " + STAR_SIGN_REMARK.get(o.get("info"), STAR_SIGN_REMARK["interest"])
    return note


CF_NAME_CONS = "הדוח המאוחד על תזרימי המזומנים"
CF_NAME_SOLE = "הדוח על תזרימי המזומנים (החברה אינה מציגה דוחות מאוחדים)"


def cf_statement_name(d):
    """How the statement used as the data source is named in captions/notes: the consolidated statement, or – for a
    company that presents no consolidated statements (override "consolidated": false, goal R1.2) – its statement of
    cash flows, saying so (iteration 2, M10)."""
    return CF_NAME_CONS if d.get("consolidated", True) else CF_NAME_SOLE

HEB_MONTHS = {
    "ינואר": 1, "פברואר": 2, "מרס": 3, "מרץ": 3, "אפריל": 4, "מאי": 5, "יוני": 6,
    "יולי": 7, "אוגוסט": 8, "ספטמבר": 9, "אוקטובר": 10, "נובמבר": 11, "דצמבר": 12,
}
MONTH_WORDS = {"שלושה": 3, "שלושת": 3, "שישה": 6, "ששת": 6, "תשעה": 9, "תשעת": 9, "שנים עשר": 12}

HEADER_KEYWORDS = ["חודשים", "החודשים", "שהסתיימו", "שהסתיימה", "ביום", "מבוקר", "לשנה", "בדצמבר",
                   "במרס", "במרץ", "ביוני", "בספטמבר", "לתקופה", "באור", "ביאור", "מוצג מחדש", "מתוקן"]
DASHES = set("-\u2013\u2014\u2212")
NUM_TOKEN_RE = re.compile(r"^[\(\)\-\u2013\u2014\u2212\d,\.\*]+$")
HEB_RE = re.compile(r"[\u0590-\u05FF]")
LATIN_RE = re.compile(r"[A-Za-z]")


def check_labels_against_goal():
    """Return list of label strings not found verbatim in goal.md (should be empty)."""
    txt = open(os.path.join(GOAL_DIR, "goal.md"), encoding="utf-8").read()
    labels = [lab for _, lab in ITEMS] + [OTHER_LABEL, TOTAL_LABEL, GROUP_IN, GROUP_OUT, CHECK_LABEL,
                                          INFO_INT_LABEL, INFO_DIV_LABEL, NOT_SEPARATE_NOTE, SUBTOTAL_TAG,
                                          OUTSIDE_TAG, MISSING_Q1_TEXT, ROLE_MAIN, SECTION_OPERATING,
                                          SECTION_INVESTING]
    return [lab for lab in labels if lab not in txt]


# ----------------------------------------------------------------------------- small utils
def restore_quotes(name):
    """Folder/file names replaced '"' by '_' (e.g. 'בע_מ' -> 'בע"מ', 'נדל_ן' -> 'נדל"ן')."""
    return re.sub(r"(?<=[\u05D0-\u05EA])_(?=[\u05D0-\u05EA])", '"', name)


def page_range_text(pages):
    """[55,56,57] -> '55–57'; [56] -> '56'; [55,57] -> '55, 57'."""
    pages = sorted(set(pages))
    if not pages:
        return ""
    out, start, prev = [], pages[0], pages[0]
    for p in pages[1:] + [None]:
        if p is not None and p == prev + 1:
            prev = p
            continue
        out.append(f"{start}\u2013{prev}" if prev != start else f"{start}")
        if p is not None:
            start = prev = p
    return ", ".join(out)


def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def temp_path(name, issuer=None):
    """Unique scratch path outside the WORKSPACE (for writing outputs before moving them in place).
    Per-issuer sub-folder + pid in the name, so that parallel runs never share a file."""
    d = temp_dir(str(issuer) if issuer else "_misc")
    return os.path.join(d, f"tmp_{os.getpid()}_{name}")


def move_into_place(tmp, dst):
    try:
        os.replace(tmp, dst)
    except OSError:
        import shutil
        shutil.copyfile(tmp, dst)
        os.remove(tmp)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


_ROLES = None


def load_roles():
    """work/roles.json (shared, read-only for batch builders): {'sources': {'<issuer>_<Q>': rel}, 'files': {rel: {...}}}."""
    global _ROLES
    if _ROLES is None:
        _ROLES = load_json(ROLES_PATH)
    return _ROLES


def source_rel(issuer, q):
    """Relative path (from WORKSPACE) of the data-source PDF of issuer x quarter, per roles.json."""
    return load_roles()["sources"].get(f"{issuer}_{q}")


def company_folder(issuer):
    hits = [d for d in os.listdir(WORKSPACE)
            if os.path.isdir(os.path.join(WORKSPACE, d)) and d.split(" - ")[0].strip() == str(issuer)]
    if len(hits) != 1:
        raise SystemExit(f"company folder for {issuer}: {hits}")
    return hits[0]


def baseline_files():
    """{relative_path: (bytes, sha256)} of the pre-existing files (the source PDFs)."""
    import csv
    out = {}
    with open(os.path.join(GOAL_DIR, "baseline_files_sha256.csv"), encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            out[row["relative_path"]] = (int(row["bytes"]), row["sha256"])
    return out


# ----------------------------------------------------------------------------- words & lines
class Word:
    __slots__ = ("text", "x0", "y0", "x1", "y1", "size", "font")

    def __init__(self, text, x0, y0, x1, y1, size, font):
        self.text, self.x0, self.y0, self.x1, self.y1 = text, x0, y0, x1, y1
        self.size, self.font = size, font

    @property
    def xc(self):
        return (self.x0 + self.x1) / 2

    @property
    def yc(self):
        return (self.y0 + self.y1) / 2

    @property
    def h(self):
        return self.y1 - self.y0

    def is_num(self):
        t = self.text
        if not NUM_TOKEN_RE.match(t):
            return False
        return any(c.isdigit() for c in t) or all(c in DASHES for c in t) or all(c in "()" for c in t)

    def __repr__(self):
        return f"W({self.text!r} {self.x0:.1f}-{self.x1:.1f} y{self.y0:.1f}-{self.y1:.1f})"


NUN_GLYPHS = "\u00f0\u00aa\uf8ff"


def fix_glyph_text(t):
    """Repair known font-encoding defects of the text layer (generic, all reports): fonts whose
    ToUnicode map lacks the letter nun emit a substitute character instead of 'נ':
      'ð' (U+00F0 = cp1255 byte 0xF0 'נ' decoded as cp1252) – 1083 Q2, 1680 Q2, 1703 Q2, 1928, 200, 2441,
          2486, 2488, 2559, 373, 584, ...;
      'ª' (U+00AA) – 2567 Q2;  '\uf8ff' (private use) – 573 Q1, 1484, 715, 2418 (cover pages).
    Only applied inside words that contain Hebrew letters (or consist of substitutes only)."""
    if any(c in t for c in NUN_GLYPHS) and (HEB_RE.search(t) or set(t) <= set(NUN_GLYPHS) | {'"', "'"}):
        for c in NUN_GLYPHS:
            t = t.replace(c, "\u05e0")
    return t


def visual_rtl_order(chars):
    """Logical order of a Hebrew word from the glyph positions (right to left), keeping runs of digits /
    Latin letters left-to-right. Used for words of the defective fonts (see fix_glyph_text) whose text
    stream puts the 'ð' (nun) glyph out of order (e.g. 'נהפקת' instead of 'הנפקת')."""
    srt = sorted(chars, key=lambda c: -(c["bbox"][0] + c["bbox"][2]))
    out, i = [], 0
    while i < len(srt):
        if re.match(r"[0-9A-Za-z.,%]", srt[i]["c"]):
            j = i
            while j + 1 < len(srt) and re.match(r"[0-9A-Za-z.,%]", srt[j + 1]["c"]):
                j += 1
            out.extend(reversed(srt[i:j + 1]))
            i = j + 1
        else:
            out.append(srt[i])
            i += 1
    return out


def page_words(page):
    """Words rebuilt from rawdict chars (stream order). Splits on whitespace and on gaps, so that
    tokens like ')(' whose two chars sit far apart become two words. Horizontal text only."""
    raw = page.get_text("rawdict", flags=pymupdf.TEXTFLAGS_RAWDICT & ~pymupdf.TEXT_PRESERVE_IMAGES)
    words = []
    for b in raw["blocks"]:
        if b.get("type", 0) != 0:
            continue
        for ln in b["lines"]:
            dx, dy = ln["dir"]
            if abs(dy) > 0.05 or dx < 0:
                continue  # rotated/vertical text is ignored
            for s in ln["spans"]:
                cur = []

                def flush():
                    if cur:
                        x0 = min(c["bbox"][0] for c in cur)
                        x1 = max(c["bbox"][2] for c in cur)
                        y0 = min(c["bbox"][1] for c in cur)
                        y1 = max(c["bbox"][3] for c in cur)
                        chars = cur
                        if any(c["c"] in NUN_GLYPHS for c in cur):
                            chars = visual_rtl_order(cur)
                        words.append(Word(fix_glyph_text("".join(c["c"] for c in chars)), x0, y0, x1, y1,
                                          s["size"], s["font"]))
                        cur.clear()

                for c in s["chars"]:
                    ch = c["c"]
                    if ch.isspace() or ch == "\u00a0":
                        flush()
                        continue
                    if cur:
                        p = cur[-1]
                        gap = max(c["bbox"][0] - p["bbox"][2], p["bbox"][0] - c["bbox"][2])
                        if gap > max(1.2, 0.2 * s["size"]):
                            flush()
                    cur.append(c)
                flush()
    return words


class Line:
    def __init__(self, words):
        self.words = sorted(words, key=lambda w: -w.x1)
        self.label_words = []
        self.groups = []      # value groups: list of (x0, x1, text)
        self.values = {}      # col index -> (raw text, parsed value)

    @property
    def y0(self):
        return min(w.y0 for w in self.words)

    @property
    def y1(self):
        return max(w.y1 for w in self.words)

    @property
    def yc(self):
        return statistics.median([w.yc for w in self.words])

    def text_all(self):
        return join_rtl(self.words)


def group_lines(words):
    """Group words into visual lines by vertical-centre proximity (robust to baseline jitter)."""
    words = sorted(words, key=lambda w: (w.yc, -w.x1))
    lines = []
    for w in words:
        best = None
        for ln in lines[-4:]:
            hmax = max(w.h, statistics.median([x.h for x in ln]))
            if abs(statistics.median([x.yc for x in ln]) - w.yc) <= 0.45 * hmax:
                best = ln
        if best is not None:
            best.append(w)
        else:
            lines.append([w])
    return [Line(ws) for ws in lines]


def join_rtl(words):
    """Join words of one visual line in logical (RTL) order. Adjacent words (no visual gap) are
    concatenated without a space (e.g. 'נדל' + '"' + 'ן'); runs of LTR words keep their LTR order."""
    ws = sorted(words, key=lambda w: -w.x1)
    # reverse runs of consecutive LTR-only words (Latin/digits) so that 'PDF 56' keeps logical order
    out, i = [], 0
    while i < len(ws):
        if not HEB_RE.search(ws[i].text) and (LATIN_RE.search(ws[i].text) or any(c.isdigit() for c in ws[i].text)):
            j = i
            while j + 1 < len(ws) and not HEB_RE.search(ws[j + 1].text) and (
                    LATIN_RE.search(ws[j + 1].text) or any(c.isdigit() for c in ws[j + 1].text)):
                j += 1
            out.extend(reversed(ws[i:j + 1]))
            i = j + 1
        else:
            out.append(ws[i])
            i += 1
    text = ""
    prev = None
    for w in out:
        if prev is None:
            text = w.text
        else:
            gap = min(abs(prev.x0 - w.x1), abs(w.x0 - prev.x1))
            text += ("" if gap < 1.0 else " ") + w.text
        prev = w
    return normalize_label(text)


def fix_mirrored_parens(t):
    """Some PDFs store the parentheses of RTL text mirrored and without the surrounding spaces:
    'הנפקת אגרות חוב)בניכוי הוצאות הנפקה(' -> 'הנפקת אגרות חוב (בניכוי הוצאות הנפקה)'. Applied only to Hebrew
    text whose first parenthesis is ')' and whose parentheses balance."""
    if not re.search(r"[\u05D0-\u05EA]", t) or "(" not in t or ")" not in t:
        return t
    first = min(i for i in (t.find("("), t.find(")")) if i >= 0)
    if t[first] != ")" or t.count("(") != t.count(")"):
        return t
    t = t.translate(str.maketrans("()", ")("))
    t = re.sub(r"(?<=[^\s(])\(", " (", t)          # space before '(' (the text layer dropped it)
    t = re.sub(r"\)(?=[^\s),.;:])", ") ", t)        # space after ')'
    return t


def normalize_label(t):
    t = t.replace("\u00a0", " ")
    t = re.sub(r"\s+", " ", t).strip()
    t = fix_mirrored_parens(t)
    t = re.sub(r"\(\s+", "(", t)
    t = re.sub(r"\s+\)", ")", t)
    t = re.sub(r"\s+,", ",", t)
    return t


# ----------------------------------------------------------------------------- numbers
def display_raw(raw):
    """Normalise a raw value string for display: ')241,336(' -> '(241,336)'."""
    if raw is None:
        return None
    s = raw.replace(" ", "")
    if "(" in s or ")" in s:
        return "(" + s.replace("(", "").replace(")", "") + ")"
    return s


def parse_amount(raw):
    """'(485,475)' -> -485475 ; '1,161,665' -> 1161665 ; '-' -> 0 ; '(5)' -> -5. Returns (value, flags)."""
    s = raw.replace(" ", "")
    flags = []
    if "*" in s:
        flags.append("asterisk")
        s = s.replace("*", "")
    if s and all(c in DASHES for c in s):
        return 0, flags
    neg = "(" in s or ")" in s
    body = s.replace("(", "").replace(")", "")
    if body and body[0] in DASHES and any(c.isdigit() for c in body):
        neg = True
        body = body[1:]
    body = body.replace(",", "")
    if not re.fullmatch(r"\d+(\.\d+)?", body):
        raise ValueError(f"cannot parse amount {raw!r}")
    v = float(body) if "." in body else int(body)
    return (-v if neg else v), flags


def build_groups(num_words, max_gap=1.6):
    """Merge horizontally adjacent numeric tokens of one line into value groups (paren-only groups
    that are not attached to a number are dropped)."""
    ws = sorted(num_words, key=lambda w: w.x0)
    groups = []
    for w in ws:
        if groups and w.x0 - groups[-1][1] <= max_gap:
            g = groups[-1]
            groups[-1] = (g[0], max(g[1], w.x1), g[2] + [w])
        else:
            groups.append((w.x0, w.x1, [w]))
    out = []
    for g in groups:
        text = "".join(x.text for x in sorted(g[2], key=lambda x: x.x0))
        if any(c.isdigit() for c in text) or any(c in DASHES for c in text):
            out.append((g[0], g[1], text))
    return out


def is_year(text):
    return bool(re.fullmatch(r"20\d\d", text))


# ----------------------------------------------------------------------------- statement parsing
HEADER_TOKENS = {"חודשים", "החודשים", "שהסתיימו", "שהסתיימה", "ביום", "מבוקר", "מבוקרים", "לשנה", "בדצמבר",
                 "במרס", "במרץ", "ביוני", "בספטמבר", "לתקופה", "באור", "ביאור", "חודשים)", "(מבוקר)"}


def is_header_line(line):
    toks = {w.text.strip(":,.()") for w in line.words}
    if toks & {t.strip("()") for t in HEADER_TOKENS}:
        return True
    t = line.text_all()
    return "מוצג מחדש" in t or "הוצג מחדש" in t


def cluster_spans(intervals, min_count):
    """Union overlapping intervals; return spans [(x0, x1, count)] with count >= min_count."""
    iv = sorted(intervals)
    spans = []
    for a, b in iv:
        if spans and a <= spans[-1][1] + 0.5:
            s = spans[-1]
            spans[-1] = [s[0], max(s[1], b), s[2] + 1]
        else:
            spans.append([a, b, 1])
    return [tuple(s) for s in spans if s[2] >= min_count]


def analyse_page(page, spans_hint=None):
    """Parse one statement page: columns (value spans), header text per column, body lines with
    label + values. spans_hint: column spans from another page of the same statement, used when
    this page has too few numeric rows to detect its own columns."""
    words = page_words(page)
    lines = group_lines(words)
    # numeric groups per line
    for ln in lines:
        ln.groups = build_groups([w for w in ln.words if w.is_num()])
    header_idx = set(i for i, ln in enumerate(lines) if is_header_line(ln))
    # first body line = first line below the last header line within the top 40% of the page
    top_limit = page.rect.height * 0.4
    last_hdr = max([i for i in header_idx if lines[i].yc < top_limit], default=-1)
    printed_page = None
    for ln in lines:
        if ln.yc > page.rect.height * 0.9 and len(ln.words) == 1 and re.fullmatch(r"\d{1,3}", ln.words[0].text):
            printed_page = int(ln.words[0].text)
    body = [ln for i, ln in enumerate(lines) if i > last_hdr and ln.yc < page.rect.height * 0.95]
    # drop page-number-only lines (single small integer, no label text)
    body = [ln for ln in body if not (len(ln.words) == 1 and re.fullmatch(r"\d{1,3}", ln.words[0].text))]
    intervals = []
    n_numeric_lines = 0
    for ln in body:
        gs = [g for g in ln.groups if not is_year(g[2])]
        if gs:
            n_numeric_lines += 1
        intervals += [(g[0], g[1]) for g in gs]
    spans = cluster_spans(intervals, max(3, int(0.25 * n_numeric_lines)))
    if spans_hint and len(spans) < len(spans_hint):
        spans = [tuple(s) for s in spans_hint]
    # header text per span (Voronoi by span centre)
    centres = [(s[0] + s[1]) / 2 for s in spans]
    order = sorted(range(len(spans)), key=lambda i: centres[i])
    bounds = {}
    for k, i in enumerate(order):
        left = (centres[order[k - 1]] + centres[i]) / 2 if k > 0 else None
        right = (centres[order[k + 1]] + centres[i]) / 2 if k + 1 < len(order) else None
        half = None
        if left is None and right is not None:
            half = right - centres[i]
            left = centres[i] - half
        if right is None and left is not None:
            half = centres[i] - left
            right = centres[i] + half
        if left is None and right is None:
            left, right = spans[i][0] - 40, spans[i][1] + 40
        bounds[i] = (left, right)
    hdr_lines = [ln for i, ln in enumerate(lines) if i <= last_hdr]
    col_headers = {i: [] for i in range(len(spans))}
    for ln in hdr_lines:
        per = {i: [] for i in range(len(spans))}
        for w in ln.words:
            for i, (a, b) in bounds.items():
                if a <= w.xc < b:
                    per[i].append(w)
        for i, ws in per.items():
            if ws:
                col_headers[i].append(join_rtl(ws))
    label_right_limit = max([s[1] for s in spans], default=0)
    # body lines: label words = words right of the rightmost value span (RTL layout)
    for ln in body:
        ln.label_words = [w for w in ln.words if w.x0 > label_right_limit + 2]
        ln.values = {}
        for g in ln.groups:
            gx = (g[0] + g[1]) / 2
            hit = [i for i, s in enumerate(spans) if g[0] <= s[1] + 2 and g[1] >= s[0] - 2]
            if not hit:
                continue
            i = min(hit, key=lambda k: abs(centres[k] - gx))
            if i in ln.values:
                ln.values[i] = (ln.values[i][0] + " " + g[2], None)
            else:
                ln.values[i] = (g[2], None)
        for i, (raw, _) in list(ln.values.items()):
            ln.values[i] = (raw, parse_amount(raw)[0])
    return {
        "spans": spans, "centres": centres, "bounds": bounds, "col_headers": col_headers,
        "hdr_lines": hdr_lines, "body": body, "lines": lines, "label_right_limit": label_right_limit,
        "printed_page": printed_page,
    }


def merge_wrapped(body, label_left_limit, pitch=None):
    """Merge wrapped labels: a text-only line immediately followed (within ~1.3 line pitch) by a
    line with values, when the text-only line is 'full width' and is not a heading."""
    rows = [ln for ln in body if ln.label_words or ln.values]
    if pitch is None:
        ys = [r.yc for r in rows]
        diffs = sorted(b - a for a, b in zip(ys, ys[1:]) if b - a > 4)
        pitch = statistics.median(diffs) if diffs else 12.0
    out = []
    i = 0
    while i < len(rows):
        r = rows[i]
        lab = join_rtl(r.label_words)
        if (not r.values and i + 1 < len(rows) and rows[i + 1].values and rows[i + 1].label_words
                and rows[i + 1].yc - r.yc <= 1.35 * pitch and not lab.endswith(":")
                and not is_section_heading(lab)
                and min(w.x0 for w in r.label_words) <= label_left_limit + 60):
            nxt = rows[i + 1]
            out.append({"label": normalize_label(lab + " " + join_rtl(nxt.label_words)),
                        "y0": r.y0, "y1": nxt.y1, "values": nxt.values, "lines": [r, nxt]})
            i += 2
            continue
        out.append({"label": lab, "y0": r.y0, "y1": r.y1, "values": r.values, "lines": [r]})
        i += 1
    return out, pitch


SECTION_RE = {
    "operating": re.compile(r"(?:פעילות|פעילויות)\)?\s+שוטפת"),
    "investing": re.compile(r"(?:פעילות|פעילויות)\)?\s+השקעה"),
    "financing": re.compile(r"(?:פעילות|פעילויות)\)?\s+מימון"),
}


def is_section_heading(label):
    t = label.replace(":", "").strip()
    return bool(re.match(r"^(?:תזרימי|תזרים)\s+(?:ה)?מזומנים\s+(?:מ|ל|ב)?(?:פעילות|פעילויות)", t))


def section_of_label(label):
    for k, rx in SECTION_RE.items():
        if rx.search(label):
            return k
    return None


# ----------------------------------------------------------------------------- headers -> periods
def parse_period_header(text, report_q, default_year=None):
    """Parse a column header text into months / end date / audit / restated."""
    t = text.replace("\u2013", "-").replace("\u05be", "-")
    months = None
    m = re.search(r"(\d+)\s*-?\s*(?:ה)?חודשים", t)
    if m:
        months = int(m.group(1))
    else:
        for w, n in MONTH_WORDS.items():
            if w in t:
                months = n
                break
    if months is None and re.search(r"(?:^|\s|ל)שנה(?:\s|$)", t):
        months = 12
    day = mon = year = None
    m = re.search(r"(\d{1,2})[./](\d{1,2})[./](20\d\d)", t)
    if m:
        day, mon, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        md = re.search(r"(\d{1,2})\s+ב?(" + "|".join(HEB_MONTHS) + r")", t)
        if md:
            day, mon = int(md.group(1)), HEB_MONTHS[md.group(2)]
        else:
            mm = re.search(r"ב(" + "|".join(HEB_MONTHS) + r")", t)
            if mm:
                mon = HEB_MONTHS[mm.group(1)]
        ys = re.findall(r"20\d\d", t)
        if ys:
            year = int(ys[-1])
    if year is None:
        year = default_year
    if months == 12 and mon is None:
        day, mon = 31, 12
    if mon is None and months in (3, 6, 9):
        mon = {"Q1": 3, "Q2": 6, "Q3": 9}.get(report_q)
    if day is None and mon is not None:
        day = {3: 31, 6: 30, 9: 30, 12: 31}.get(mon)
    restated = bool(re.search(r"מוצג מחדש|מתוקן|הוצג מחדש|הותאם", t))
    audit = "בלתי מבוקר" if "בלתי מבוקר" in t else ("מבוקר" if "מבוקר" in t else "")
    return {"months": months, "end": (f"{year:04d}-{mon:02d}-{day:02d}" if (year and mon and day) else None),
            "restated": restated, "audit": audit}


HEB_MONTH_NAMES = {1: "ינואר", 2: "פברואר", 3: "מרץ", 4: "אפריל", 5: "מאי", 6: "יוני", 7: "יולי", 8: "אוגוסט",
                   9: "ספטמבר", 10: "אוקטובר", 11: "נובמבר", 12: "דצמבר"}


def month_range(months, end_iso):
    """'(אפריל–יוני)' for a 3-month period ending 30.06 (goal amendment 1, T2)."""
    m_end = int(end_iso.split("-")[1])
    m_start = (m_end - months) % 12 + 1
    return f"({HEB_MONTH_NAMES[m_start]}\u2013{HEB_MONTH_NAMES[m_end]})"


def is_quarter_column(col, columns):
    """T2: a 3-month column that is NOT the year-to-date period = the same report presents a longer
    period ending on the same date (e.g. the 3-month columns of a Q2 report next to the 6-month ones)."""
    return col.get("months") == 3 and any((c.get("months") or 0) > 3 and c.get("end") == col.get("end")
                                          for c in columns)


def period_label(months, end_iso, restated=False, quarter_range=False):
    y, m, d = end_iso.split("-")
    date = f"{d}.{m}.{y}"
    lab = f"שנה שהסתיימה ב-{date}" if months == 12 else f"{months} חודשים שהסתיימו ב-{date}"
    if quarter_range:
        lab += " " + month_range(months, end_iso)
    return lab + (" (מוצג מחדש)" if restated else "")


# ----------------------------------------------------------------------------- units / currency
UNIT_PATTERNS = [
    (r'(?:ב)?אלפי[\s()]*(?:ש["\u05f4\u201d]?\s?ח|₪)', 'ש"ח', "אלפים"),
    (r'(?:ב)?מי?ליוני[\s()]*(?:ש["\u05f4\u201d]?\s?ח|₪)', 'ש"ח', "מיליונים"),
    (r'(?:ב)?אלפי\s+דולר(?:\s+ארה["\u05f4]?ב)?(?:\s+אמריקאי)?', 'דולר ארה"ב', "אלפים"),
    (r'(?:ב)?מי?ליוני\s+דולר(?:\s+ארה["\u05f4]?ב)?', 'דולר ארה"ב', "מיליונים"),
    (r"(?:ב)?אלפי\s+אירו", "אירו", "אלפים"),
    (r"(?:ב)?מי?ליוני\s+אירו", "אירו", "מיליונים"),
    (r"(?:ב)?אלפי\s+זלוטי", "זלוטי פולני", "אלפים"),
    (r"(?:ב)?אלפי\s+דולר\s+קנדי", "דולר קנדי", "אלפים"),
    (r"(?:ב)?אלפי\s+ליש[\"\u05f4]?ט", "ליש\"ט", "אלפים"),
]


def detect_units(text):
    found = []
    for rx, cur, unit in UNIT_PATTERNS:
        for m in re.finditer(rx, text):
            found.append((m.start(), m.group(0), cur, unit))
    if not found:
        return None
    # prefer the most specific (longest) match at the earliest position
    found.sort(key=lambda f: (f[0], -len(f[1])))
    _, raw, cur, unit = found[0]
    if cur == 'דולר ארה"ב' and "קנדי" in text[found[0][0]:found[0][0] + 30]:
        cur = "דולר קנדי"
    return {"units_text": raw.strip(), "currency": cur, "units": unit}


# ----------------------------------------------------------------------------- classification (suggestion only)
def suggest_item(label):
    """Keyword-based suggestion of the item for an original financing line. Returns (item, note).
    item: int 1..14, 'other', 'net_loans' (4/7 by sign), 'net_bonds' (3/8 by sign)."""
    t = label.replace("פירעון", "פרעון").replace("״", '"')
    nci = ("שאינן מקנות שליטה" in t) or ("מיעוט" in t)
    if "ריבית" in t and ("ששולמה" in t or "ששולמו" in t or "תשלום" in t or "שולמה" in t):
        return 13, ""
    if ("דיבידנד" in t or "חלוקה" in t or "חלוקת" in t or "משיכות" in t) and nci:
        return 12, ""
    if "דיבידנד" in t or "חלוקת רווחים" in t:
        return 11, ""
    if nci and re.search(r"רכישה|רכישת|רכישות", t):
        return 14, ""
    if nci:
        return 6, ""
    if "אופציות" in t or "כתבי אופציה" in t:
        return 2, ""
    if "מניות אוצר" in t or "רכישה עצמית" in t or re.search(r"רכישת מניות(?! ב)", t):
        return 9, ""
    if "חכירה" in t or "חכירות" in t:
        return 10, ""
    bonds = ("אגרות חוב" in t or 'אג"ח' in t or "אגרות-חוב" in t or 'נע"מ' in t or "ניירות ערך מסחריים" in t)
    if bonds:
        rec = re.search(r"הנפקת|הנפקה|תמורה|גיוס|קבלת", t)
        rep = re.search(r"פרעון|רכישה|רכישת|פדיון", t)
        if rec and rep:
            return "net_bonds", "שורה נטו – סיווג לפי סימן"
        if rep:
            return 8, ""
        return 3, ""
    if "הנפקת מניות" in t or "הנפקת הון" in t or "הנפקה של מניות" in t:
        return 1, ""
    if "לזמן קצר" in t or "אשראי" in t:
        return 5, ""
    if "הלוואות" in t or "הלוואה" in t:
        rec = re.search(r"קבלת|התקבלו|נטילת|תמורה", t)
        rep = re.search(r"פרעון|החזר", t)
        if rec and rep:
            return "net_loans", "שורה נטו – סיווג לפי סימן"
        if rep:
            return 7, ""
        if rec:
            return 4, ""
        if "נטו" in t:
            return 5, "הלוואות נטו ללא ציון תקופה – סעיף 5"
    return "other", "לבדיקה ידנית"
