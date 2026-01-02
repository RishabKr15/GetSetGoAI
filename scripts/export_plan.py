import sys
from pathlib import Path

def md_to_pdf_simple(md_path: Path, pdf_path: Path):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except Exception as e:
        print("Missing dependency: reportlab. Install it with `pip install reportlab`.")
        raise

    text = md_path.read_text(encoding="utf-8")

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin
    line_height = 12

    for paragraph in text.split("\n\n"):
        for line in paragraph.splitlines():
            if y < margin:
                c.showPage()
                y = height - margin
            # crude wrap
            if len(line) > 100:
                # wrap long lines
                for i in range(0, len(line), 100):
                    c.drawString(margin, y, line[i:i+100])
                    y -= line_height
            else:
                c.drawString(margin, y, line)
                y -= line_height
        y -= line_height  # extra space between paragraphs

    c.save()


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/export_plan.py <input.md> <output.pdf>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])
    if not md_path.exists():
        print(f"Input file not found: {md_path}")
        sys.exit(2)

    md_to_pdf_simple(md_path, pdf_path)
    print(f"Wrote PDF: {pdf_path}")


if __name__ == "__main__":
    main()
