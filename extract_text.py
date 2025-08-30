# scripts/extract_text.py
# Usage: python extract_text.py ../data/physics_book.pdf ../data/physics_book.txt

import sys
import pdfplumber

def pdf_to_text(pdf_path, out_txt):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            page_text = p.extract_text() or ""
            # basic clean: strip headers/footers heuristics (optional)
            text.append(page_text)
    all_text = "\n\n".join(text)
    # further simple cleaning
    all_text = all_text.replace("\r", "\n")
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(all_text)
    print("Saved:", out_txt)

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    out_txt = sys.argv[2]
    pdf_to_text(pdf_path, out_txt)
