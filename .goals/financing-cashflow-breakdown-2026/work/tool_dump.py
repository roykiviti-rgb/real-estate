# -*- coding: utf-8 -*-
"""Generic dump tool (UTF-8 output file, never touches the source PDF).

Usage:
  python tool_dump.py <pdf> <out.txt> scan                 -> per-page keyword hits for cash-flow statements
  python tool_dump.py <pdf> <out.txt> text  <p> [<p>...]   -> plain text of pages (1-based)
  python tool_dump.py <pdf> <out.txt> words <p> [<p>...]   -> words grouped in visual lines with x-coordinates
"""
import sys
import pymupdf

KEYWORDS = [
    "תזרימי המזומנים", "תזרימי מזומנים", "תזרים מזומנים", "תזרים המזומנים",
    "פעילות מימון", "פעילויות מימון", "לפעילות מימון", "מפעילות מימון",
    "מאוחד", "מאוחדים", "נפרד", "המיוחסים לחברה", "38ד", "מזומנים נטו",
]


def lines_of(page, ymin=0, ymax=1e9):
    words = [w for w in page.get_text("words") if ymin <= w[1] <= ymax]
    words.sort(key=lambda w: (round(w[3], 1), -w[0]))
    lines = []
    for w in words:
        if lines and abs(lines[-1][0] - w[3]) <= 2.0:
            lines[-1][1].append(w)
        else:
            lines.append([w[3], [w]])
    for ln in lines:
        ln[1].sort(key=lambda w: -w[0])
    return lines


def main():
    pdf, out, mode = sys.argv[1], sys.argv[2], sys.argv[3]
    pages = [int(p) for p in sys.argv[4:]]
    doc = pymupdf.open(pdf)
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"file={pdf}\npages={doc.page_count}\n")
        if mode == "scan":
            for i, page in enumerate(doc):
                txt = page.get_text("text")
                hits = {k: txt.count(k) for k in KEYWORDS}
                if any(hits.values()):
                    first = " | ".join([l.strip() for l in txt.splitlines() if l.strip()][:8])
                    f.write(f"p{i+1}: " + ", ".join(f"{k}={v}" for k, v in hits.items() if v)
                            + " :: " + first[:300] + "\n")
        elif mode == "text":
            for p in pages:
                f.write(f"\n===== page {p} rect={doc[p-1].rect} rot={doc[p-1].rotation}\n")
                f.write(doc[p - 1].get_text("text"))
        elif mode == "words":
            for p in pages:
                page = doc[p - 1]
                f.write(f"\n===== page {p} rect={page.rect} rot={page.rotation}\n")
                for yb, ws in lines_of(page):
                    f.write(f"y={yb:7.2f} :: " + "  ".join(f"[{w[0]:.1f}-{w[2]:.1f}]{w[4]}" for w in ws) + "\n")
        else:
            raise SystemExit("unknown mode " + mode)


if __name__ == "__main__":
    main()
