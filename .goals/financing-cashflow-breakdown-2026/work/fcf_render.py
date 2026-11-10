# -*- coding: utf-8 -*-
"""fcf_render — build the per-company screenshots PDF from final report data (data/<issuer>_<Q>.json).

Images are rendered from the source PDFs (opened read-only); highlights are drawn on the rendered
raster images only. Captions are Hebrew (python-bidi visual reordering + PyMuPDF TextWriter).
"""
import sys

sys.dont_write_bytecode = True
import io  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402

import pymupdf  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

try:  # pure-python implementation applies bracket mirroring
    from bidi.algorithm import get_display as _gd
except Exception:  # pragma: no cover
    from bidi import get_display as _gd0

    def _gd(t, base_dir=None):
        return _gd0(t, base_dir=base_dir).translate(str.maketrans("()[]", ")(]["))

import fcf_lib as L  # noqa: E402

FONT_REG = r"C:\Windows\Fonts\arial.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
DPI_PAGE = 150
DPI_CTX = 120
DPI_ZOOM = 220
ORANGE = (230, 120, 0)
YELLOW = (255, 230, 0)
BLUE = (30, 90, 220)
RED = (210, 30, 30)
A4 = (595.0, 842.0)
DRAFT_TEXT = "טיוטה – חילוץ אוטומטי שטרם אומת ויזואלית; אין להשתמש בנתונים לפני אימות"


# ----------------------------------------------------------------------------- text helpers
class Writer:
    def __init__(self):
        self.reg = pymupdf.Font(fontfile=FONT_REG)
        self.bold = pymupdf.Font(fontfile=FONT_BOLD)

    def width(self, text, size, bold=False):
        return (self.bold if bold else self.reg).text_length(text, fontsize=size)

    def wrap(self, text, size, bold, max_width):
        font = self.bold if bold else self.reg
        lines, cur = [], ""
        for w in text.split(" "):
            trial = (cur + " " + w).strip()
            if not cur or font.text_length(trial, fontsize=size) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def rtl(self, page, x_right, y, text, size=9.0, bold=False, max_width=None, color=(0, 0, 0), lead=1.35):
        """Write RTL text right-aligned at x_right, wrapping to max_width. Returns next y."""
        font = self.bold if bold else self.reg
        max_width = max_width or (x_right - 20)
        lines = self.wrap(text, size, bold, max_width)
        tw = pymupdf.TextWriter(page.rect, color=color)
        for ln in lines:
            vis = _gd(ln, base_dir="R")
            tw.append((x_right - font.text_length(vis, fontsize=size), y), vis, font=font, fontsize=size)
            y += size * lead
        tw.write_text(page)
        return y

    def label_and_ltr(self, page, x_right, y, label, ltr_text, size=9.0, color=(0, 0, 0)):
        """'label:' (RTL, at the right) followed (to its left) by an LTR string such as a file name.
        An LRM is inserted after each Hebrew run that is followed by '_'+digit/Latin so that the
        file name reads left-to-right in its logical order (e.g. 1618_<hebrew>_2026_Q1_...)."""
        tw = pymupdf.TextWriter(page.rect, color=color)
        v1 = _gd(label, base_dir="R")
        w1 = self.reg.text_length(v1, fontsize=size)
        tw.append((x_right - w1, y), v1, font=self.reg, fontsize=size)
        t = re.sub(r"([\u05D0-\u05EA])(?=[_\-. ][0-9A-Za-z])", "\\1\u200e", ltr_text)
        v2 = _gd(t, base_dir="L").replace("\u200e", "").replace("\u200f", "")
        w2 = self.bold.text_length(v2, fontsize=size)
        tw.append((x_right - w1 - 5 - w2, y), v2, font=self.bold, fontsize=size)
        tw.write_text(page)
        return y + size * 1.35


# ----------------------------------------------------------------------------- image helpers
def render(page, clip, dpi):
    pix = page.get_pixmap(dpi=dpi, clip=clip, alpha=False)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def to_px(rect, clip, dpi):
    s = dpi / 72.0
    return [(rect[0] - clip.x0) * s, (rect[1] - clip.y0) * s, (rect[2] - clip.x0) * s, (rect[3] - clip.y0) * s]


def overlay(img, boxes):
    """boxes: list of (px_rect, outline_rgb, width_px, fill_rgba or None)."""
    base = img.convert("RGBA")
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for r, outline, width, fill in boxes:
        if fill:
            d.rectangle(r, fill=fill)
    base = Image.alpha_composite(base, ov)
    d2 = ImageDraw.Draw(base)
    for r, outline, width, fill in boxes:
        if outline:
            d2.rectangle(r, outline=outline + (255,), width=width)
    return base.convert("RGB")


def separator(width, height=34):
    img = Image.new("RGB", (width, height), (255, 255, 255))
    d = ImageDraw.Draw(img)
    y = height // 2
    x = 10
    while x < width - 10:
        d.line([(x, y), (min(x + 14, width - 10), y)], fill=(120, 120, 120), width=3)
        x += 26
    return img


def stack(images, sep=True):
    w = max(i.width for i in images)
    parts = []
    for k, im in enumerate(images):
        if k and sep:
            parts.append(separator(w))
        parts.append(im)
    h = sum(p.height for p in parts)
    out = Image.new("RGB", (w, h), (255, 255, 255))
    y = 0
    for p in parts:
        out.paste(p, (w - p.width, y))  # right-aligned (RTL documents)
        y += p.height
    return out


def png_bytes(img, jpeg=False):
    buf = io.BytesIO()
    if jpeg:
        img.save(buf, "JPEG", quality=88, optimize=True)
    else:
        img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


# ----------------------------------------------------------------------------- geometry from data
# All boxes come from d["geometry"] (computed by finalize_report.py: from the auto extraction with the
# pilot's formulas, or from the manual "boxes" of the override file). PDF points, origin top-left.
def geo(d, p):
    return d["geometry"].get(str(p)) or {}


def fin_segments(d):
    """[(page, y0, y1)] of the financing section per page (padded, limited by the neighbouring rows)."""
    segs = []
    for p in d["fin_pages"]:
        g = geo(d, p)
        if g.get("fin_y"):
            segs.append((p, g["fin_y"][0], g["fin_y"][1]))
    if not segs:
        raise SystemExit(f"{d['issuer']} {d['quarter']}: no financing-section geometry – add 'boxes' to the override")
    return segs


def page_x_range(d, pages, pad=6.0, fallback=False):
    xs0, xs1, wmax = [], [], 0
    for p in pages:
        g = geo(d, p)
        if not g.get("content_x"):
            continue
        xs0.append(g["content_x"][0])
        xs1.append(g["content_x"][1])
        wmax = (g.get("page_rect") or [595.0, 842.0])[0]
    if not xs0:
        if fallback:
            w = (geo(d, pages[0]).get("page_rect") or [595.0, 842.0])[0]
            return 20.0, w - 20.0
        raise SystemExit(f"{d['issuer']} {d['quarter']}: no horizontal geometry for pages {pages} – add 'boxes'")
    return max(0.0, min(xs0) - pad), min(wmax, max(xs1) + pad)


# ----------------------------------------------------------------------------- header composition (Phase C: S3/S4)
# Every zoom crop and every red (*) crop must show the period headers (column titles) and the units/currency line.
# The geometry gives a header strip per page; when the text inside it lacks the periods or the units, the crop is
# composed: (a) a column-header block printed on the same page above the (*) line (appendix tables repeat it),
# (b) a units line printed on the same page, (c) the header strip / units line of another page of the statement.
YEAR_RX = re.compile(r"20[12]\d")
UNITS_WORD_RX = re.compile(r"אלפי|מיליוני|מליוני|אלפים|thousands|millions", re.I)
HDR_WORD_RX = re.compile(r"חודשים|החודשים|שהסתיימו|שהסתיימה|שנסתיימה|לשנה|ל ש נ ה|ביום|לתקופה|בדצמבר|במרס|במרץ|ביוני|"
                         r"מבוקר|אלפי|מיליוני|ליום|\d{1,2}[./]\d{1,2}[./]20\d\d")
AMOUNT_RX = re.compile(r"\d,\d{3}|\(\d|\d\)|\d{5,}")


class PageText:
    """Read-only text access to the source PDF pages (words with coordinates), cached per page."""

    def __init__(self, doc):
        self.doc = doc
        self._lines = {}

    def lines(self, p):
        if p not in self._lines:
            ws = L.page_words(self.doc[p - 1])
            self._lines[p] = [(ln.y0, ln.y1, ln.words) for ln in sorted(L.group_lines(ws), key=lambda l: l.y0)]
        return self._lines[p]

    def text(self, p, rect):
        out = []
        for y0, y1, ws in self.lines(p):
            sel = [w for w in ws if rect.x0 <= w.xc <= rect.x1 and rect.y0 <= w.yc <= rect.y1]
            if sel:
                out.append(L.join_rtl(sel))
        return " | ".join(out)

    def band_lines(self, p, y_lo, y_hi, x0, x1):
        """[(y0, y1, text)] of the lines whose centre lies in (y_lo, y_hi) (words inside x0..x1 only)."""
        out = []
        for y0, y1, ws in self.lines(p):
            sel = [w for w in ws if x0 <= w.xc <= x1]
            if sel and y_lo < (y0 + y1) / 2 < y_hi:
                out.append((min(w.y0 for w in sel), max(w.y1 for w in sel), L.join_rtl(sel)))
        return out


# ----------------------------------------------------------------------------- edge snapping (iteration 2, S7b/S7d)
# A crop or frame edge that crosses a text row shows a sliver of that row (half-cut glyphs) or draws the frame over it.
# Every crop edge is therefore moved off any text row it crosses (or touches with its glyphs): the row stays inside the
# region when its centre lies inside, otherwise it is left out, and the edge is placed on the least-inked pixel row
# between that row and its neighbour. A header top edge that runs through a logo/icon is moved above it. An edge that
# crosses nothing is left exactly where it was. Zoom and (*) crops get their frames in a white margin (framed());
# frames drawn on full pages are placed on the row gaps (row_gap_ys / clear_band).
INK_LEVEL = 150


def ink_profile(page, x0, x1, y0, y1, dpi=DPI_ZOOM):
    """Number of dark pixels per pixel row of the band (x0..x1, y0..y1) rendered at dpi."""
    import numpy as np
    pix = page.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1), alpha=False, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width]
    return (a < INK_LEVEL).sum(axis=1)


RULE_RUN_PT = 13.0      # a horizontal dark run at least this long is a printed rule (underline), not a glyph


def glyph_profile(page, x0, x1, y0, y1, dpi=DPI_ZOOM):
    """Like ink_profile, but counting only dark pixels in horizontal runs shorter than RULE_RUN_PT (glyph ink; printed
    rules and underlines are not counted)."""
    import numpy as np
    pix = page.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1), alpha=False, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width] < INK_LEVEL
    long_px = max(2, int(round(RULE_RUN_PT * dpi / 72.0)))
    out = []
    for row in a:
        if not row.any():
            out.append(0)
            continue
        r = np.concatenate(([0], row.astype(np.int8), [0]))
        dr = np.diff(r)
        starts, ends = np.where(dr == 1)[0], np.where(dr == -1)[0]
        lens = ends - starts
        out.append(int(lens[lens < long_px].sum()))
    return np.array(out)


def quiet_row(page, x0, x1, lo, hi, dpi=DPI_ZOOM):
    """y (PDF points) of the least-inked pixel row between lo and hi; ties -> the row nearest the middle."""
    if hi - lo < 0.6:
        return (lo + hi) / 2
    prof = ink_profile(page, x0, x1, lo, hi, dpi)
    n = len(prof)
    if not n:
        return (lo + hi) / 2
    mid = (n - 1) / 2
    best = min(range(n), key=lambda i: (int(prof[i]), abs(i - mid)))
    return lo + (best + 0.5) * (hi - lo) / n


def ink_cut(page, x0, x1, y, dpi=DPI_ZOOM):
    """True when the pixel rows at y carry clearly more ink than the quietest pixel row within ±12 pt, i.e. y runs
    through glyphs or a graphic (vertical table rules alone do not count)."""
    lo, hi = max(0.0, y - 12), min(page.rect.height, y + 12)
    if hi - lo < 2:
        return False
    prof = ink_profile(page, x0, x1, lo, hi, dpi)
    n = len(prof)
    if n < 3:
        return False
    e = int(round((y - lo) * n / (hi - lo)))
    e = min(max(e, 1), n - 1)
    return min(int(prof[e - 1]), int(prof[e])) > int(prof.min()) + 2


def graphic_top(pt, p, y, x0, x1, reach=25.0, dpi=DPI_ZOOM):
    """A top edge that runs through a graphic (logo, icon; not a text row) is moved off it: up to the first quiet pixel
    row above it, so the graphic is shown whole – unless the graphic is also cut by the crop's left/right edge; then it
    is left out if possible: the edge moves down to a quiet pixel row below it with no text row in between, or to an
    almost blank pixel row between the edge and the top of the first text row. Otherwise y is returned unchanged."""
    import numpy as np
    page = pt.doc[p - 1]
    if not ink_cut(page, x0, x1, y, dpi):
        return y
    lo, hi = max(0.0, y - reach), min(page.rect.height, y + reach)
    if hi - lo < 4:
        return y
    pix = page.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, lo, x1, hi), alpha=False, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width] < INK_LEVEL
    prof = a.sum(axis=1)
    n = len(prof)
    s = n / (hi - lo)
    base = int(prof.min())
    e = min(int(round((y - lo) * s)), n - 1)
    min_run = max(2, int(round(2.5 * s)))      # a logo may consist of parts with small gaps between them

    def walk(step):
        """First quiet pixel row next to the graphic in direction step (a quiet run of min_run rows), or None."""
        i, run = e, 0
        while 0 <= i < n:
            if int(prof[i]) <= base + 1:
                run += 1
                if run >= min_run:
                    return i - step * (min_run - 1)
            else:
                run = 0
            i += step
        return None

    up, down = walk(-1), walk(+1)
    up_ok, down_ok = up is not None, down is not None
    band = a[(up if up_ok else max(0, e - 2)):(down + 1 if down_ok else e + 3)]
    side_cut = bool(band[:, :2].any() or band[:, -2:].any())
    if side_cut:
        # leave the graphic out: a quiet pixel row below it with no text row in between, or else the least-inked pixel
        # row between the edge and the top of the first text row below it, if (almost) blank
        if down_ok:
            y_down = lo + (down + 0.5) / s
            lost = [r for r in pt.band_lines(p, y - 1, y_down + 1, x0, x1) if y < (r[0] + r[1]) / 2 < y_down]
            if not lost:
                return y_down
        below = [r for r in pt.band_lines(p, y - 1, hi, x0, x1) if (r[0] + r[1]) / 2 > y]
        stop = min([r[0] + 0.25 * (r[1] - r[0]) for r in below] + [hi])
        i_stop = min(n - 1, int((stop - lo) * s))
        if i_stop > e:
            cand = min(range(e, i_stop + 1), key=lambda i: (int(prof[i]), i))
            if int(prof[cand]) <= base + 4:
                return lo + (cand + 0.5) / s
    if up_ok:
        return lo + (up + 0.5) / s
    return y


def side_graphic(pt, p, r, depth=20.0, min_rows=6, dpi=DPI_ZOOM):
    """True when a graphic (not text) at the top of crop r touches its left or right edge over at least min_rows pixel
    rows (a logo cut by the crop's side)."""
    import numpy as np
    page = pt.doc[p - 1]
    ya, yb = r.y0, min(r.y1, r.y0 + depth)
    if yb - ya < 2:
        return False
    pix = page.get_pixmap(dpi=dpi, clip=pymupdf.Rect(r.x0, ya, r.x1, yb), alpha=False, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width] < INK_LEVEL
    for edge, cols in ((r.x0, a[:, :2]), (r.x1, a[:, -2:])):
        if int(cols.any(axis=1).sum()) >= min_rows:
            words = [w for _, _, ws in pt.lines(p) for w in ws if w.x0 < edge < w.x1 and w.y1 > ya and w.y0 < yb]
            if not words:
                return True
    return False


def widen_for_graphic(pt, p, r, reach=90.0, gap=3.0, dpi=DPI_ZOOM):
    """Crop r widened so that a graphic (logo) touching its left/right edge near the top is taken in whole (its parts
    up to gap pt apart; at most reach pt wider on each side, otherwise r is returned unchanged). The parts of the zoom
    are stacked right-aligned at one scale, so a wider header part keeps the columns aligned."""
    import numpy as np
    page = pt.doc[p - 1]
    W = page.rect.width
    xa, xb = max(0.0, r.x0 - reach), min(W, r.x1 + reach)
    ya, yb = max(0.0, r.y0 - 25), min(r.y1, r.y0 + 30)
    pix = page.get_pixmap(dpi=dpi, clip=pymupdf.Rect(xa, ya, xb, yb), alpha=False, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width] < INK_LEVEL
    col = a.any(axis=0)
    n = len(col)
    s = n / (xb - xa)
    g = max(2, int(round(gap * s)))

    def ext(i, step):
        j, last, run = i, None, 0
        while 0 <= j < n:
            if col[j]:
                last, run = j, 0
            else:
                run += 1
                if run >= g:
                    break
            j += step
        return last if 0 <= j < n else None

    nx0, nx1 = r.x0, r.x1
    i0, i1 = int((r.x0 - xa) * s), min(n - 1, int((r.x1 - xa) * s))
    if col[max(0, i0 - 1):i0 + 2].any():
        last = ext(i0, -1)
        if last is None:
            return r
        nx0 = xa + last / s - 2
    if col[max(0, i1 - 1):i1 + 2].any():
        last = ext(i1, +1)
        if last is None:
            return r
        nx1 = xa + (last + 1) / s + 2
    return pymupdf.Rect(max(0.0, nx0), r.y0, min(W, nx1), r.y1)


def snap_header_rect(pt, p, r, protect=None):
    """Header part / header frame r snapped (snap_rect with graphics_top); a logo that is still cut by the crop's side
    after that is taken in whole by widening the crop (widen_for_graphic) and snapping again."""
    s = snap_rect(pt, p, r, protect=protect, graphics_top=True)
    if side_graphic(pt, p, s):
        w = widen_for_graphic(pt, p, r)
        if w != r:
            s = snap_rect(pt, p, w, protect=protect, graphics_top=True)
    return s


def snap_edge(pt, p, y, x0, x1, side, keep=None, protect=None, graphics=False):
    """New y of a horizontal edge on page p (x-range x0..x1). side='top': the region lies below y; 'bottom': above.
    keep: a y that must stay inside the region. protect(text): rows that must stay inside the region.
    graphics (top edges only): an edge through a logo/icon (no text row) is moved off it (see graphic_top)."""
    page = pt.doc[p - 1]
    if y <= 0.5 or y >= page.rect.height - 0.5:
        return y
    rows = sorted(pt.band_lines(p, y - 60, y + 60, x0, x1))
    cut = [r for r in rows if r[0] + 0.6 < y < r[1] - 0.6]
    if not cut:
        # an edge within 1 pt of a row's box that still touches its glyphs counts as cutting it
        near = [r for r in rows if r[0] - 1.0 <= y <= r[1] + 1.0]
        if near and ink_cut(page, x0, x1, y):
            cut = near
    if not cut:
        if graphics and side == "top":
            return graphic_top(pt, p, y, x0, x1)
        return y
    r = min(cut, key=lambda q: abs((q[0] + q[1]) / 2 - y))
    i = rows.index(r)
    c = (r[0] + r[1]) / 2
    inside = (c <= y) if side == "bottom" else (c >= y)
    if not inside and protect and protect(r[2]):
        inside = True

    def gap(a, b):          # quiet row between row a (above) and row b (below); None = page margin
        ca = (a[0] + a[1]) / 2 + 0.25 * (a[1] - a[0]) if a else (b[0] - 8)
        cb = (b[0] + b[1]) / 2 - 0.25 * (b[1] - b[0]) if b else (a[1] + 8)
        lo, hi = min(ca, cb), max(ca, cb)
        return quiet_row(page, x0, x1, max(0.0, lo), min(page.rect.height, hi))

    prev_r = rows[i - 1] if i > 0 else None
    next_r = rows[i + 1] if i + 1 < len(rows) else None
    if side == "bottom":
        new = gap(r, next_r) if inside else gap(prev_r, r)
    else:
        new = gap(prev_r, r) if inside else gap(r, next_r)
    if keep is not None and ((side == "bottom" and new < keep) or (side == "top" and new > keep)):
        return y
    return new


def snap_rect(pt, p, r, protect=None, keep=None, graphics_top=False):
    """pymupdf.Rect r on page p with its top and bottom edges snapped (keep = (y_top_max, y_bottom_min) or None).
    graphics_top: the top edge is also moved off a logo/icon (header parts and frames)."""
    k0, k1 = keep if keep else (None, None)
    y0 = snap_edge(pt, p, r.y0, r.x0, r.x1, "top", keep=k0, protect=protect, graphics=graphics_top)
    y1 = snap_edge(pt, p, r.y1, r.x0, r.x1, "bottom", keep=k1, protect=protect)
    if y1 - y0 < 2:
        return r
    return pymupdf.Rect(r.x0, y0, r.x1, y1)


def box_off_crossing_rows(pt, p, r, reach=40.0):
    """The vertical edges of a frame drawn on a full page must not run through text. A text row inside box r whose words
    cross the box's left or right edge is left below the box when it is the box's bottom row (e.g. a section heading
    printed on the units line): the bottom moves up to the row gap above it. In any other row the box is widened to
    take in the crossing words (up to reach pt)."""
    page = pt.doc[p - 1]
    for _ in range(6):
        rows = [(y0, y1, ws) for y0, y1, ws in pt.lines(p)
                if r.y0 + 0.5 < (y0 + y1) / 2 < r.y1 - 0.5]
        if not rows:
            return r
        hit = None
        for y0, y1, ws in rows:
            cw = [w for w in ws if (w.x0 + 1 < r.x0 < w.x1 - 1) or (w.x0 + 1 < r.x1 < w.x1 - 1)]
            if cw:
                hit = (y0, y1, cw)
        if not hit:
            return r
        y0, y1, cw = hit
        last = max(rows, key=lambda t: (t[0] + t[1]) / 2)
        if abs(last[0] - y0) < 0.01 and len(rows) > 1:
            prev = max((t for t in rows if (t[0] + t[1]) / 2 < (y0 + y1) / 2), key=lambda t: (t[0] + t[1]) / 2)
            lo = (prev[0] + prev[1]) / 2 + 0.25 * (prev[1] - prev[0])
            hi = (y0 + y1) / 2 - 0.25 * (y1 - y0)
            r = pymupdf.Rect(r.x0, r.y0, r.x1, quiet_row(page, r.x0, r.x1, min(lo, hi), max(lo, hi)))
            continue
        nx0 = min([r.x0] + [w.x0 - 2 for w in cw if w.x0 < r.x0])
        nx1 = max([r.x1] + [w.x1 + 2 for w in cw if w.x1 > r.x1])
        if r.x0 - nx0 > reach or nx1 - r.x1 > reach:
            return r
        r = pymupdf.Rect(nx0, r.y0, nx1, r.y1)
    return r


def clear_band(page, x0, x1, y, w, side, lim=None, reach=2.5, dpi=DPI_ZOOM):
    """Edge position near y for a frame line of width w pt that is drawn inside its box (below the edge for side 'top',
    above it for 'bottom'): the position within ±reach pt (and within lim=(lo, hi) if given) whose line band covers the
    least glyph ink (glyph_profile: a frame may lie on a printed rule but not on text); ties -> nearest to y."""
    H = page.rect.height
    a_lim, b_lim = (y - reach, y + reach) if lim is None else (max(y - reach, lim[0]), min(y + reach, lim[1]))
    if b_lim < a_lim:
        return y
    lo, hi = max(0.0, a_lim - w - 1), min(H, b_lim + w + 1)
    if hi - lo < w + 1:
        return y
    prof = glyph_profile(page, x0, x1, lo, hi, dpi)
    n = len(prof)
    if n < 3:
        return y
    s = n / (hi - lo)
    base = int(prof.min())
    cost = [max(0, int(v) - base) for v in prof]
    wpx = max(1, int(round(w * s)))
    c0 = (y - lo) * s
    best = None
    for c in range(int(round((a_lim - lo) * s)), int(round((b_lim - lo) * s)) + 1):
        a, b = (c, c + wpx) if side == "top" else (c - wpx, c)
        if a < 0 or b > n:
            continue
        key = (sum(cost[a:b]), abs(c - c0))
        if best is None or key < best[0]:
            best = (key, c)
    return y if best is None else lo + best[1] / s


FRAME_MARGIN = 7        # px (at DPI_ZOOM) of white margin around a zoom crop; its frame is drawn in the margin


def hpad(im, m=FRAME_MARGIN):
    """The crop with a white margin of m px on the left and right only (aligns with framed parts)."""
    out = Image.new("RGB", (im.width + 2 * m, im.height), (255, 255, 255))
    out.paste(im, (m, 0))
    return out


def framed(im, outline, width, fill=None, m=FRAME_MARGIN):
    """The crop inside a white margin of m px, with its frame drawn in the margin – the frame never covers the
    content (iteration 2, S7a/S7b)."""
    out = Image.new("RGB", (im.width + 2 * m, im.height + 2 * m), (255, 255, 255))
    out.paste(im, (m, m))
    return overlay(out, [([0, 0, out.width - 1, out.height - 1], outline, width, fill)])


def row_gap_ys(pt, p, b, x0, x1):
    """Quiet pixel rows directly above and below the text block with bbox b (one or more printed rows): between it and
    the neighbouring rows (or a few points outside it where there is no neighbour)."""
    page = pt.doc[p - 1]
    rows = pt.band_lines(p, b[1] - 40, b[3] + 40, x0, x1)

    def c(r):
        return (r[0] + r[1]) / 2

    own = [r for r in rows if b[1] - 0.5 <= c(r) <= b[3] + 0.5] or [(b[1], b[3], "")]
    above = [r for r in rows if c(r) < b[1] - 0.5]
    below = [r for r in rows if c(r) > b[3] + 0.5]
    t_own = min(own, key=lambda r: r[0])
    b_own = max(own, key=lambda r: r[1])
    t_hi = c(t_own) - 0.25 * (t_own[1] - t_own[0])
    b_lo = c(b_own) + 0.25 * (b_own[1] - b_own[0])
    if above:
        a = max(above, key=c)
        a_lo = c(a) + 0.25 * (a[1] - a[0])
        g0 = quiet_row(page, x0, x1, min(a_lo, t_hi), max(a_lo, t_hi))
    else:
        g0 = quiet_row(page, x0, x1, max(0.0, t_own[0] - 6), t_hi)
    if below:
        n = min(below, key=c)
        n_hi = c(n) - 0.25 * (n[1] - n[0])
        g1 = quiet_row(page, x0, x1, min(b_lo, n_hi), max(b_lo, n_hi))
    else:
        g1 = quiet_row(page, x0, x1, b_lo, min(page.rect.height, b_own[1] + 6))
    return g0, g1


def is_header_text(t):
    """A header row (periods, audit status, units) that must stay inside a header part."""
    return bool(HDR_WORD_RX.search(t) or has_units(t) or YEAR_RX.search(norm_years(t)))


def norm_years(t):
    return re.sub(r"(?<!\d)2 0 2 (\d)(?!\d)", r"202\1", t)


def has_periods(t):
    return len(set(YEAR_RX.findall(norm_years(t)))) >= 2


def has_units(t):
    return bool(UNITS_WORD_RX.search(t))


def units_band(pt, p, y_lo, y_hi, x0, x1):
    """Rect of the (first) units line of page p between y_lo and y_hi, or None."""
    for y0, y1, t in pt.band_lines(p, y_lo, y_hi, x0, x1):
        if has_units(t) and not AMOUNT_RX.search(t):
            return pymupdf.Rect(x0, y0 - 2, x1, y1 + 2)
    return None


def colhdr_block(pt, p, y_lo, y_hi, x0, x1):
    """Rect of the column-header block (period titles + years [+ audit / units]) printed on page p between y_lo and
    y_hi, closest to y_hi (an appendix table that repeats the statement's column headers), or None."""
    lines = pt.band_lines(p, y_lo, y_hi, x0, x1)
    idx = [i for i, (a, b, t) in enumerate(lines) if has_periods(t) and not AMOUNT_RX.search(norm_years(t))]
    if not idx:
        return None
    i1 = i0 = idx[-1]
    while i0 - 1 >= 0 and HDR_WORD_RX.search(lines[i0 - 1][2]) and not AMOUNT_RX.search(norm_years(lines[i0 - 1][2])) \
            and lines[i0][0] - lines[i0 - 1][1] < 14:
        i0 -= 1
    while i1 + 1 < len(lines) and HDR_WORD_RX.search(lines[i1 + 1][2]) and not AMOUNT_RX.search(lines[i1 + 1][2]) \
            and lines[i1 + 1][0] - lines[i1][1] < 14:
        i1 += 1
    return pymupdf.Rect(x0, lines[i0][0] - 2, x1, lines[i1][1] + 2)


def units_elsewhere(d, pt, exclude, x0, x1):
    """(page, Rect) of a units line printed in the header area of another statement page, or None."""
    for p in d["cf_pages"]:
        if p in exclude:
            continue
        g = geo(d, p)
        top = (g.get("hdr_strip") or [0, 0])[0]
        bottom = max((g.get("hdr_strip") or [0, 0])[1] + 25, top + 60)
        b = units_band(pt, p, top - 1, bottom, x0, x1)
        if b:
            return p, b
    return None


def zoom_header_parts(d, pt):
    """Parts of the zoom's header: [(page, Rect, role)], role in header|units; and a caption fragment."""
    segs = fin_segments(d)
    hp = d["header_page"]
    hg = geo(d, hp)
    if not hg.get("hdr_strip"):
        raise SystemExit(f"{d['issuer']} {d['quarter']}: no header geometry on page {hp} – add boxes.header")
    pages_inv = sorted({hp} | {s[0] for s in segs})
    x0, x1 = page_x_range(d, pages_inv, pad=6)
    strip = pymupdf.Rect(x0, hg["hdr_strip"][0], x1, hg["hdr_strip"][1])
    contiguous = len(segs) == 1 and segs[0][0] == hp and segs[0][1] - (hg.get("header_y1") or 0) < 40
    seen = pt.text(hp, pymupdf.Rect(x0, strip.y0, x1, segs[0][1] if contiguous else strip.y1))
    parts, note = [(hp, strip, "header")], ""
    if not has_units(seen):
        limit = segs[0][1] if hp == segs[0][0] else strip.y1 + 80
        b = units_band(pt, hp, strip.y1 - 1, limit, x0, x1)
        if b and b.y0 - strip.y1 < 30:
            parts[0] = (hp, pymupdf.Rect(x0, strip.y0, x1, b.y1), "header")       # extend the strip to the units line
            note = " רצועת הכותרת הורחבה עד שורת יחידות המידה."
        elif b:
            parts.append((hp, b, "units"))
            note = f" שורת יחידות המידה (עמוד {hp}) נוספה מתחת לרצועת הכותרת."
        else:
            ue = units_elsewhere(d, pt, {hp}, x0, x1)
            if ue:
                parts.append((ue[0], ue[1], "units"))
                note = f" יחידות המידה מודפסות בעמוד {ue[0]} בלבד ונוספו מתחת לרצועת הכותרת."
    # iteration 2 (S7d): no part edge may cut through a text row (e.g. the next section heading under the strip)
    parts = [(q, snap_header_rect(pt, q, r, protect=is_header_text) if role == "header"
              else snap_rect(pt, q, r, protect=is_header_text), role) for q, r, role in parts]
    return parts, contiguous, note


def star_crop_plan(d, pt, p, outs_p):
    """Plan of the red (*) crop of page p: (x0, x1, header parts [(page, Rect, role)], caption fragment)."""
    g = geo(d, p)
    xa, xb = page_x_range(d, [p], pad=6, fallback=True)
    for o in outs_p:
        if not o.get("bbox"):
            raise SystemExit(f"{d['issuer']} {d['quarter']}: outside line '{o.get('text')}' has no bbox")
        # the crops always cover the whole (*) line, even if it is wider than the page's content range
        xa, xb = min(xa, o["bbox"][0] - 6), max(xb, o["bbox"][2] + 6)
    first_y = min(o["bbox"][1] for o in outs_p)
    parts, notes = [], []
    seen = ""
    if g.get("hdr_strip") and g["hdr_strip"][0] < first_y - 6:
        r = pymupdf.Rect(xa, g["hdr_strip"][0], xb, min(g["hdr_strip"][1], first_y - 6))
        parts.append((p, r, "header"))
        seen = pt.text(p, r)
    if not has_periods(seen):
        top = parts[0][1].y1 if parts else 0
        blk = colhdr_block(pt, p, top - 1, first_y - 2, xa, xb)
        if blk:
            parts.append((p, blk, "colhdr"))
            seen += " | " + pt.text(p, blk)
            notes.append("כותרות העמודות של הטבלה שבעמוד זה")
    if not has_periods(seen):
        hparts, _, _ = zoom_header_parts(d, pt)
        hparts = [(q, pymupdf.Rect(xa, r.y0, xb, r.y1), role) for q, r, role in hparts]
        parts = hparts + parts
        seen += " | " + " | ".join(pt.text(q, r) for q, r, _ in hparts)
        notes.append(f"רצועת הכותרת של הדוח (עמוד {d['header_page']}) – כותרות העמודות ויחידות המידה")
    if not has_units(seen):
        top = max([r.y1 for q, r, _ in parts if q == p] or [0])
        b = units_band(pt, p, top - 1, first_y - 2, xa, xb)
        if b:
            parts.append((p, b, "units"))
        else:
            ue = units_elsewhere(d, pt, {p}, xa, xb)
            if ue:
                parts.append((ue[0], pymupdf.Rect(xa, ue[1].y0, xb, ue[1].y1), "units"))
                notes.append(f"יחידות המידה מעמוד {ue[0]}")
    # iteration 2 (S7b): part edges snapped to the gaps between text rows; parts on the (*) page stay above its lines
    snapped = []
    for q, r, role in parts:
        s = (snap_header_rect(pt, q, r, protect=is_header_text) if role == "header"
             else snap_rect(pt, q, r, protect=is_header_text))
        if q == p and s.y1 > first_y - 1.5:
            s = pymupdf.Rect(s.x0, s.y0, s.x1, max(r.y1, s.y0 + 2) if r.y1 <= first_y - 1.5 else first_y - 1.5)
        snapped.append((q, s, role))
    return xa, xb, snapped, ("; ".join(notes))


def crop_texts(d, doc):
    """Text inside the header parts of the zoom and of every (*) crop (for validate.py, AC10 / S3–S4)."""
    pt = PageText(doc)
    hparts, contiguous, _ = zoom_header_parts(d, pt)
    segs = fin_segments(d)
    zt = []
    for q, r, role in hparts:
        if contiguous and role == "header":
            r = pymupdf.Rect(r.x0, r.y0, r.x1, segs[0][1])
        zt.append(pt.text(q, r))
    out = {"zoom": " | ".join(zt), "stars": {}}
    by_page = {}
    for o in d.get("outside", []):
        by_page.setdefault(o["page"], []).append(o)
    for p, os_ in sorted(by_page.items()):
        xa, xb, parts, _ = star_crop_plan(d, pt, p, os_)
        out["stars"][p] = " | ".join(pt.text(q, r) for q, r, _ in parts)
    return out


# ----------------------------------------------------------------------------- PDF assembly
class Book:
    def __init__(self, title, issuer=None):
        self.out = pymupdf.open()
        self.w = Writer()
        self.toc = []
        self.title = title
        self.issuer = issuer
        self.entries = []  # for the cover: (page no, text)

    def image_page(self, img, caption, toc_title, jpeg=False, landscape=None):
        margin = 28.0

        def cap_height(W):
            h = 4.0
            for kind, *args in caption:
                if kind == "title":
                    h += 6 + 11.5 * 1.35 * len(self.w.wrap(args[0], 11.5, True, W - 2 * margin))
                elif kind == "file":
                    h += 2 + 9 * 1.35
                else:
                    h += 2 + 9 * 1.35 * len(self.w.wrap(args[0], 9, False, W - 2 * margin))
            return h + 6

        best = None
        for land in ([False, True] if landscape is None else [landscape]):
            W, H = (A4[1], A4[0]) if land else A4
            sc = min((W - 2 * margin) / img.width, (H - margin - cap_height(W) - 30) / img.height)
            if best is None or sc > best[0] * 1.08:
                best = (sc, land, W, H)
        _, land, W, H = best
        page = self.out.new_page(width=W, height=H)
        y = margin + 4
        xr = W - margin
        for kind, *args in caption:
            if kind == "title":
                y = self.w.rtl(page, xr, y + 6, args[0], size=11.5, bold=True, max_width=W - 2 * margin)
            elif kind == "file":
                y = self.w.label_and_ltr(page, xr, y + 2, args[0], args[1], size=9)
            else:
                y = self.w.rtl(page, xr, y + 2, args[0], size=9, max_width=W - 2 * margin,
                               color=(0.15, 0.15, 0.15))
        y += 6
        sc = min((W - 2 * margin) / img.width, (H - y - 30) / img.height)
        iw, ih = img.width * sc, img.height * sc
        rect = pymupdf.Rect(W - margin - iw, y, W - margin, y + ih)
        page.insert_image(rect, stream=png_bytes(img, jpeg=jpeg))
        page.draw_rect(rect, color=(0.6, 0.6, 0.6), width=0.6)
        self.toc.append([1, toc_title, self.out.page_count])
        self.entries.append((self.out.page_count, toc_title))
        return page

    def finish(self, path, cover_lines):
        # cover page inserted at the front
        cover = self.out.new_page(pno=0, width=A4[0], height=A4[1])
        y = 60
        xr = A4[0] - 40
        for kind, *args in cover_lines:
            text = args[0]
            if kind == "h1":
                y = self.w.rtl(cover, xr, y, text, size=16, bold=True, max_width=A4[0] - 80) + 6
            elif kind == "h2":
                y = self.w.rtl(cover, xr, y + 4, text, size=11.5, bold=True, max_width=A4[0] - 80) + 2
            elif kind == "file":
                y = self.w.label_and_ltr(cover, xr, y, args[0], args[1], size=9.5)
            else:
                y = self.w.rtl(cover, xr, y, text, size=9.5, max_width=A4[0] - 80)
        y += 8
        y = self.w.rtl(cover, xr, y, "תוכן:", size=11.5, bold=True)
        for pno, t in self.entries:
            y = self.w.rtl(cover, xr, y + 1, f"עמוד {pno + 1} – {t}", size=9.5, max_width=A4[0] - 80)
        n = self.out.page_count
        for i, pg in enumerate(self.out):
            foot = f"{self.title} – עמוד {i + 1} מתוך {n}"
            vis = _gd(foot, base_dir="R")
            wv = self.w.reg.text_length(vis, fontsize=7.5)
            tw = pymupdf.TextWriter(pg.rect, color=(0.4, 0.4, 0.4))
            tw.append(((pg.rect.width - wv) / 2, pg.rect.height - 14), vis, font=self.w.reg, fontsize=7.5)
            tw.write_text(pg)
        toc = [[1, "שער ותוכן", 1]] + [[lvl, t, p + 1] for lvl, t, p in self.toc]
        self.out.set_toc(toc)
        self.out.set_metadata({"title": self.title, "subject": "צילומי מסך – תזרים מזומנים מפעילות מימון",
                               "creator": "fcf pipeline (.goals/financing-cashflow-breakdown-2026)"})
        tmp = L.temp_path(os.path.basename(path), self.issuer)
        self.out.save(tmp, garbage=3, deflate=True)
        self.out.close()
        L.move_into_place(tmp, path)


def report_images(book, d, img_no_start=1):
    """Add the screenshot pages for one report. Returns the next image number.
    Order (pilot design): full page(s) with the financing section highlighted, the zoom (header strip + financing
    section), one red crop per page carrying (*) lines, then the other statement pages. Every caption states exactly
    what the page shows (Phase C, S2): the (*) lines of THAT page (with the number of the image that enlarges them),
    or that the page has none.
    Iteration 2: every crop edge is snapped off the text rows it would cut (S7b/S7d); the zoom and (*) crops are framed
    in a white margin around them, so no frame covers text, and the contiguous zoom is cut into a blue and an orange
    part (S7a); (*) lines are red-framed on the full pages as well (frame lines centred on the row gaps); full-page
    frame lines are placed off the glyphs; the dashed-line remark is printed only when a dashed line is drawn (S7c);
    blank source cells are named in the zoom legend (S7f); the statement is named per report (M10)."""
    src = os.path.join(L.WORKSPACE, d["company_folder"], d["source_file"])
    doc = pymupdf.open(src)
    pt = PageText(doc)
    who = f"{d['company_name']} ({d['issuer']}) – דוח {d['report_label']}"
    units = d["units"]["units_text"] if d.get("units") else ""
    stmt = L.cf_statement_name(d)
    k = img_no_start
    segs = fin_segments(d)
    hp = d["header_page"]
    col_order = " | ".join(c["label"] for c in d["columns"])
    outs = d.get("outside", [])
    by_page = {}
    for o in outs:
        by_page.setdefault(o["page"], []).append(o)
    star_pages = sorted(by_page)
    # image numbers are known in advance: full pages, zoom, (*) crops, context pages
    zoom_img = img_no_start + len(segs)
    star_img = {p: zoom_img + 1 + i for i, p in enumerate(star_pages)}
    both_in_fin = all(d.get("info", {}).get(x, {}).get("presented_in_financing") for x in ("interest", "dividend"))

    def page_line(p):
        pp = geo(d, p).get("printed_page")
        pr = f"; מספר העמוד המודפס בדוח: {pp}" if pp else ""
        return f"עמוד {p} בקובץ ה-PDF (מתוך {d['page_count']}{pr}) – {stmt}"

    def star_list(p):
        return "; ".join(f"'{o['text']}' ({o['section']})" for o in by_page.get(p, []))

    def stars_elsewhere(p):
        others = [q for q in star_pages if q != p]
        if not others:
            return ""
        return "שורות ה-(*) של דוח זה מופיעות ב" + ", ".join(f"עמוד {q} (תמונה {star_img[q]})" for q in others) + "."

    def star_note_for_page(p, also=False):
        """What the page shows about the (*) lines – exact, page by page."""
        if p in by_page:
            return (f"בעמוד זה {'גם ' if also else ''}שורות (*) של ריבית/דיבידנד ששולמו מחוץ לפעילות המימון: "
                    f"{star_list(p)} – מסומנות במסגרת אדומה ומוצגות בהגדלה בתמונה {star_img[p]}.")
        secs_l = d.get("context_sections", {}).get(str(p), [])
        if not any(s in (L.SECTION_OPERATING, L.SECTION_INVESTING) for s in secs_l):
            return ""
        if outs:
            return ("בעמוד זה אין שורות של ריבית ששולמה או דיבידנד ששולם מחוץ לפעילות המימון. " + stars_elsewhere(p)).strip()
        if both_in_fin:
            return ("בעמוד זה אין שורות של ריבית ששולמה או דיבידנד ששולם מחוץ לפעילות המימון – בדוח זה הן מוצגות "
                    "בפעילות המימון בלבד; לכן שורות (*) שמחוץ למימון = 0.")
        return ("בעמוד זה אין שורות נפרדות של ריבית ששולמה או דיבידנד ששולם מחוץ לפעילות המימון; לכן שורות (*) "
                "שמחוץ למימון = 0 (ראו את ההערות בשורות (*) בקובץ הפירוט).")

    def fb(p, x0, x1, y, w_px, dpi, side, lim=None):
        """Frame edge near y whose drawn line (w_px pixels at dpi, drawn inside the box) avoids glyph ink."""
        return clear_band(doc[p - 1], x0, x1, y, w_px * 72.0 / dpi, side, lim=lim)

    def star_frames(p, clip, dpi, width):
        """Red frames of the (*) lines printed on page p (full-page renders): each frame line is centred on the quiet
        pixel row between the (*) line and its neighbouring row."""
        out = []
        for o in by_page.get(p, []):
            b = o["bbox"]
            xa_, xb_ = b[0] - 3, b[2] + 3
            g0, g1 = row_gap_ys(pt, p, b, xa_, xb_)
            h = width * 72.0 / dpi / 2
            out.append((to_px([xa_, g0 - h, xb_, g1 + h], clip, dpi), RED, width, None))
        return out

    # 1) full page(s) with the financing section highlighted
    for p, y0, y1 in segs:
        page = doc[p - 1]
        g = geo(d, p)
        clip = page.rect
        img = render(page, clip, DPI_PAGE)
        x0, x1 = page_x_range(d, [p], pad=5)
        y0s = snap_edge(pt, p, y0, x0, x1, "top", keep=(y0 + y1) / 2)
        y1s = snap_edge(pt, p, y1, x0, x1, "bottom", keep=(y0 + y1) / 2)
        y0s = fb(p, x0, x1, y0s, 5, DPI_PAGE, "top")
        y1s = fb(p, x0, x1, y1s, 5, DPI_PAGE, "bottom")
        boxes = [(to_px([x0, y0s, x1, y1s], clip, DPI_PAGE), ORANGE, 5, YELLOW + (70,))]
        legend = "מקרא: רקע צהוב ומסגרת כתומה = תזרימי מזומנים מפעילות מימון (מהכותרת ועד שורת הסה\"כ)"
        if g.get("hdr_box"):
            hb = snap_header_rect(pt, p, pymupdf.Rect(*g["hdr_box"]), protect=is_header_text)
            hb = box_off_crossing_rows(pt, p, hb)
            hy0 = fb(p, hb.x0, hb.x1, hb.y0, 4, DPI_PAGE, "top")
            hy1 = fb(p, hb.x0, hb.x1, hb.y1, 4, DPI_PAGE, "bottom",
                     lim=(hb.y1 - 2.5, y0s) if hb.y1 <= y0s + 0.5 else None)
            boxes.append((to_px([hb.x0, hy0, hb.x1, hy1], clip, DPI_PAGE), BLUE, 4, None))
            in_box = pt.text(p, pymupdf.Rect(hb.x0, hy0, hb.x1, hy1))
            if has_units(in_box):
                legend += f"; מסגרת כחולה = שם החברה, שם הדוח, יחידות המידה ({units}) וכותרות העמודות (התקופות)"
            else:
                legend += (f"; מסגרת כחולה = שם החברה, שם הדוח וכותרות העמודות (התקופות); יחידות המידה ({units}) – "
                           f"ברצועת הכותרת שבתמונה {zoom_img}")
        else:
            legend += f"; כותרות העמודות ויחידות המידה ({units}) – ברצועת הכותרת שבתמונה {zoom_img}"
        if p in by_page:
            boxes += star_frames(p, clip, DPI_PAGE, 4)
            legend += "; מסגרת אדומה = שורות (*) – ריבית/דיבידנד ששולמו מחוץ לפעילות המימון"
        img = overlay(img, boxes)
        cap = [("title", f"{who} – תמונה {k}: עמוד מלא, פעילות המימון מודגשת"),
               ("file", "קובץ המקור:", d["source_file"]),
               ("text", page_line(p)),
               ("text", legend + ".")]
        sn = star_note_for_page(p, also=True)
        if sn:
            cap.append(("text", sn))
        book.image_page(img, cap, f"דוח {d['report_label']} – עמוד PDF {p} – עמוד מלא עם הדגשת פעילות המימון")
        k += 1

    # 2) zoomed crop: header strip (+ units line when needed) + financing section. Every part is framed in a white
    #    margin around it, so a frame never covers the content (S7a/S7b). When the header strip and the financing
    #    section are contiguous on the page, the single crop is cut at the row gaps into a blue part (header strip),
    #    the rows between them (if any, unframed) and an orange part (financing section) – nothing is omitted.
    hparts, contiguous, hnote = zoom_header_parts(d, pt)
    pages_inv = sorted({hp} | {s[0] for s in segs})
    x0, x1 = page_x_range(d, pages_inv, pad=6)
    zsegs = [(p, snap_edge(pt, p, y0, x0, x1, "top", keep=(y0 + y1) / 2),
              snap_edge(pt, p, y1, x0, x1, "bottom", keep=(y0 + y1) / 2)) for p, y0, y1 in segs]
    # a header part widened to take in a whole logo (snap_header_rect) widens every part, so the columns stay aligned
    x0 = min([x0] + [r.x0 for _, r, _ in hparts])
    x1 = max([x1] + [r.x1 for _, r, _ in hparts])
    hparts = [(q, pymupdf.Rect(x0, r.y0, x1, r.y1), role) for q, r, role in hparts]
    if contiguous:
        hq, hr, _ = hparts[0]
        fy0, fy1 = zsegs[0][1], zsegs[0][2]
        hb1 = min(hr.y1, fy0)
        run = [framed(render(doc[hq - 1], pymupdf.Rect(x0, hr.y0, x1, hb1), DPI_ZOOM), BLUE, 3)]
        if fy0 - hb1 > 1.0:
            run.append(hpad(render(doc[hq - 1], pymupdf.Rect(x0, hb1, x1, fy0), DPI_ZOOM)))
        run.append(framed(render(doc[hq - 1], pymupdf.Rect(x0, fy0, x1, fy1), DPI_ZOOM), ORANGE, 4, YELLOW + (38,)))
        extra = [framed(render(doc[q - 1], r, DPI_ZOOM), BLUE, 3) for q, r, role in hparts[1:]]
        img = stack(run, sep=False)
        if extra:
            img = stack([img] + extra)
        omitted = " קו מקווקו = קטע שהושמט." if extra else ""
    else:
        parts = [framed(render(doc[q - 1], r, DPI_ZOOM), BLUE, 3) for q, r, role in hparts]
        parts += [framed(render(doc[p - 1], pymupdf.Rect(x0, y0, x1, y1), DPI_ZOOM), ORANGE, 4, YELLOW + (38,))
                  for p, y0, y1 in zsegs]
        img = stack(parts)
        omitted = " הקטע שבין רצועת הכותרת לבין סעיף המימון הושמט (קו מקווקו)."
    fin_pages_txt = ", ".join(str(s[0]) for s in segs)
    zero_txt = "\"-\" או תא ריק בדוח = 0" if d.get("zoom_blank_cells") else "\"-\" = 0"
    cap = [("title", f"{who} – תמונה {k}: הגדלה – פעילות המימון עם כותרות העמודות ויחידות המידה"),
           ("file", "קובץ המקור:", d["source_file"]),
           ("text", f"רצועת הכותרת מעמוד {hp} בקובץ ה-PDF; סעיף המימון מעמוד {fin_pages_txt}.{omitted}{hnote} "
                    f"יחידות: {units}. סכומים בסוגריים = תשלומים (נרשמו בשלילה); {zero_txt}."),
           ("text", f"סדר העמודות בדוח (מימין לשמאל): {col_order}")]
    book.image_page(img, cap, f"דוח {d['report_label']} – הגדלה של פעילות המימון (עמוד PDF {fin_pages_txt})")
    k += 1

    # 3) (*) lines classified outside financing (if any), highlighted – one image per page. Each (*) line is cut at the
    #    quiet pixel rows between it and its neighbouring rows and framed red in a white margin (S7b: no slivers of the
    #    neighbouring rows, and the frame never covers text).
    for p in star_pages:
        os_ = sorted(by_page[p], key=lambda o: o["bbox"][1])
        xa, xb, hparts_s, snote = star_crop_plan(d, pt, p, os_)
        xa = min([xa] + [r.x0 for _, r, _ in hparts_s])
        xb = max([xb] + [r.x1 for _, r, _ in hparts_s])
        hparts_s = [(q, pymupdf.Rect(xa, r.y0, xb, r.y1), role) for q, r, role in hparts_s]
        parts = []
        prev = None
        sep_drawn = False
        for q, r, role in hparts_s:
            im = hpad(render(doc[q - 1], r, DPI_ZOOM))
            if prev is not None and (q != prev[0] or r.y0 - prev[1] > 3):
                parts.append(separator(im.width))
                sep_drawn = True
            parts.append(im)
            prev = (q, r.y1)
        for o in os_:
            b = o["bbox"]
            g0, g1 = row_gap_ys(pt, p, b, xa, xb)
            if prev is not None and prev[0] == p:
                g0 = max(g0, prev[1])
            im = framed(render(doc[p - 1], pymupdf.Rect(xa, g0, xb, g1), DPI_ZOOM), RED, 4, (255, 120, 120, 50))
            if prev is not None and (prev[0] != p or g0 - prev[1] > 3):
                parts.append(separator(im.width))
                sep_drawn = True
            parts.append(im)
            prev = (p, g1)
        img = stack(parts, sep=False)
        hdr_txt = (f"מעל השורות: {snote}." if snote else
                   "מעל השורות: רצועת הכותרת של העמוד (כותרות העמודות ויחידות המידה).")
        dash = " קו מקווקו = קטע שהושמט." if sep_drawn else ""
        cap = [("title", f"{who} – תמונה {k}: (*) שורות ריבית/דיבידנד ששולמו שסווגו מחוץ לפעילות מימון"),
               ("file", "קובץ המקור:", d["source_file"]),
               ("text", page_line(p)),
               ("text", f"מודגש באדום: {star_list(p)}. הסכומים מוצגים בשורות (*) 'לידיעה בלבד' ואינם נכללים בסכום "
                        f"הסעיפים. {hdr_txt}{dash}")]
        book.image_page(img=img, caption=cap,
                        toc_title=f"דוח {d['report_label']} – (*) מחוץ לפעילות מימון, עמוד PDF {p}")
        k += 1

    # 4) the other pages of the cash-flow statement (all pages cited in the workbook)
    ctx_pages = [p for p in d["cf_pages"] if p not in d["fin_pages"]]
    for p in ctx_pages:
        page = doc[p - 1]
        img = render(page, page.rect, DPI_CTX)
        if p in by_page:
            img = overlay(img, star_frames(p, page.rect, DPI_CTX, 3))
        secs_l = d.get("context_sections", {}).get(str(p), [])
        secs = " ו".join(secs_l) if secs_l else "המשך הדוח"
        has_cash_sections = any(s in (L.SECTION_OPERATING, L.SECTION_INVESTING) for s in secs_l)
        if p in by_page:
            title = f"עמוד נוסף של {stmt} ({secs}) – כולל שורות (*)"
            note = star_note_for_page(p)
        elif has_cash_sections:
            title = f"עמוד נוסף של {stmt} ({secs}) – לבדיקת סעיפי (*)"
            note = star_note_for_page(p)
        else:
            title = f"עמוד נוסף של {stmt} ({secs}) – לידיעה"
            note = (f"עמוד המשך של {stmt} – מוצג לשלמות; אין בו תזרימי מזומנים מפעילות מימון "
                    "ואין בו שורות (*).")
            if outs:
                note += " " + stars_elsewhere(p)
        cap = [("title", f"{who} – תמונה {k}: {title}"),
               ("file", "קובץ המקור:", d["source_file"]),
               ("text", page_line(p)),
               ("text", note.strip())]
        book.image_page(img, cap, f"דוח {d['report_label']} – עמוד PDF {p} – {secs}", jpeg=True)
        k += 1
    doc.close()
    return k


def build_screenshots(issuer, reports, out_path, draft=False):
    """reports: list of final data dicts (Q1 first). draft=True marks the cover (unverified data)."""
    d0 = reports[0]
    title = f"{issuer} - צילומי מסך תזרים מימון 2026"
    book = Book(title, issuer)
    k = 1
    for d in reports:
        k = report_images(book, d, k)
    cover = [("h1", "צילומי מסך – תזרימי מזומנים מפעילות מימון – דוחות 2026"),
             ("h2", f"{d0['company_name']} (מספר מנפיק {issuer})")]
    if draft:
        cover.append(("h2", DRAFT_TEXT))
    names = []
    for d in reports:
        if L.cf_statement_name(d) not in names:
            names.append(L.cf_statement_name(d))
    cover += [("text", f"מקור הנתונים: {' / '.join(names)} בדוחות הכספיים הרבעוניים של החברה. "
                       "כל תמונה מציינת את קובץ המקור ואת מספר העמוד בקובץ ה-PDF (מספור פיזי, החל מ-1)."),
              ("file", "הפירוט המספרי (בתיקיית החברה):", f"{issuer} - פירוט תזרים מימון 2026.xlsx")]
    for d in reports:
        cover.append(("file", f"דוח {d['report_label']}:", d["source_file"]))
    if not any(d["quarter"] == "Q1" for d in reports):
        cover.append(("h2", L.MISSING_Q1_TEXT))
    cover.append(("text", "מקרא: רקע צהוב ומסגרת כתומה = פעילות המימון; מסגרת כחולה = שם הדוח, יחידות וכותרות העמודות; "
                          "מסגרת אדומה = שורות (*) שסווגו מחוץ לפעילות המימון (אם יש)."))
    book.finish(out_path, cover)
