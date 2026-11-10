# -*- coding: utf-8 -*-
"""Review helper: render a PDF page with a labelled coordinate grid (PDF points, origin top-left, the
coordinate system used by override 'boxes', 'bbox' and line geometry), so that boxes can be read visually.

Usage (from any directory):
  python tool_grid.py <issuer> <Q1|Q2> <page> [--clip y0 y1] [--step 10] [--dpi 150] [--file <pdf name>]
    --clip   render only the horizontal band y0..y1 (points) – use with a higher --dpi for small text
    --step   minor grid step in points (labels every 5 steps)
    --file   another PDF of the company folder (default: the data source from roles.json / override)
Output: %TEMP%/fcf_run/<issuer>/grid_<Q>_p<page>_<hhmmss>.png (path printed) + the page size.
Read-only on the source PDF.
"""
import sys

sys.dont_write_bytecode = True
import argparse  # noqa: E402
import os  # noqa: E402
import time  # noqa: E402

import pymupdf  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import fcf_lib as L  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issuer")
    ap.add_argument("q", choices=["Q1", "Q2"])
    ap.add_argument("page", type=int)
    ap.add_argument("--clip", nargs=2, type=float)
    ap.add_argument("--step", type=float, default=10.0)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--file")
    a = ap.parse_args()
    folder = L.company_folder(a.issuer)
    ov_p = os.path.join(L.OVERRIDES_DIR, f"{a.issuer}_{a.q}.json")
    ov = L.load_json(ov_p) if os.path.exists(ov_p) else {}
    fname = a.file or ov.get("source_file") or os.path.basename(L.source_rel(a.issuer, a.q).replace("\\", "/"))
    with pymupdf.open(os.path.join(L.WORKSPACE, folder, fname)) as doc:
        page = doc[a.page - 1]
        W, H = page.rect.width, page.rect.height
        y0, y1 = (a.clip if a.clip else (0.0, H))
        clip = pymupdf.Rect(0, y0, W, y1)
        pix = page.get_pixmap(dpi=a.dpi, clip=clip, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    s = a.dpi / 72.0
    margin = int(46 * s / 2)
    canvas = Image.new("RGB", (img.width + 2 * margin, img.height + 2 * margin), (255, 255, 255))
    canvas.paste(img, (margin, margin))
    ov_img = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov_img)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", max(10, int(6.5 * s)))
    except Exception:  # pragma: no cover
        font = ImageFont.load_default()

    def X(x):
        return margin + x * s

    def Y(y):
        return margin + (y - y0) * s

    step = a.step
    k = 0
    x = 0.0
    while x <= W + 0.01:
        major = (k % 5 == 0)
        dr.line([(X(x), Y(y0)), (X(x), Y(y1))], fill=(255, 0, 0, 110 if major else 45), width=2 if major else 1)
        if major:
            for yy in (margin * 0.15, Y(y1) + margin * 0.1):
                dr.text((X(x) - 8, yy), f"{x:.0f}", fill=(200, 0, 0, 255), font=font)
        x += step
        k += 1
    k = 0
    yv = (int(y0 / step) + (0 if y0 % step == 0 else 1)) * step
    while yv <= y1 + 0.01:
        major = (round(yv / step) % 5 == 0)
        dr.line([(X(0), Y(yv)), (X(W), Y(yv))], fill=(0, 0, 255, 110 if major else 45), width=2 if major else 1)
        if major:
            dr.text((2, Y(yv) - 6), f"{yv:.0f}", fill=(0, 0, 200, 255), font=font)
            dr.text((X(W) + 3, Y(yv) - 6), f"{yv:.0f}", fill=(0, 0, 200, 255), font=font)
        yv += step
        k += 1
    out_img = Image.alpha_composite(canvas.convert("RGBA"), ov_img).convert("RGB")
    out = os.path.join(L.temp_dir(a.issuer), f"grid_{a.q}_p{a.page}_{time.strftime('%H%M%S')}.png")
    out_img.save(out)
    print(out)
    print(f"page size: {W:.1f} x {H:.1f} pt; rendered band y={y0:.0f}..{y1:.0f}; grid step {step:g} pt "
          f"(red labels = x, blue labels = y)")


if __name__ == "__main__":
    main()
