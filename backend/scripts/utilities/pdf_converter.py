import sys
import os
import platform
import subprocess
from fpdf import FPDF
from PyPDF2 import PdfMerger
from PIL import Image


class PDFConverter:
    def __init__(self):
        self.system = platform.system()

    def docx_to_pdf(self, input_path, output_path=None):
        if self.system in ["Windows", "Darwin"]:  
            try:
                from docx2pdf import convert
                convert(input_path, output_path)
                print(f"✅ Converted {input_path} → {output_path or 'same folder'} (docx2pdf)")
            except ImportError:
                print("❌ Please install docx2pdf: pip install docx2pdf")
        else:  
            if not output_path:
                output_path = os.path.dirname(input_path) or "."
            try:
                subprocess.run(
                    ["soffice", "--headless", "--convert-to", "pdf", input_path, "--outdir", output_path],
                    check=True
                )
                print(f"✅ Converted {input_path} → {output_path} (LibreOffice)")
            except Exception as e:
                print(f"❌ LibreOffice conversion failed: {e}")

    def images_to_pdf(self, image_paths, output_path):
        pdf = FPDF()
        for image_path in image_paths:
            cover = Image.open(image_path)
            width, height = cover.size
            width, height = float(width * 0.264583), float(height * 0.264583)

            pdf.add_page()
            pdf.image(image_path, 0, 0, width, height)

        pdf.output(output_path, "F")
        print(f"✅ Converted images {image_paths} → {output_path}")

    def merge_pdfs(self, input_paths, output_path):
        merger = PdfMerger()
        for pdf in input_paths:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()
        print(f"✅ Merged {input_paths} → {output_path}")


if __name__ == "__main__":
    converter = PDFConverter()

    if len(sys.argv) < 2:
        print("Usage: python pdf_converter.py <command> [args]")
        print("Commands:")
        print("  docx2pdf <input.docx> [output.pdf/folder]")
        print("  img2pdf <img1> <img2> ... <output.pdf>")
        print("  merge <pdf1> <pdf2> ... <output.pdf>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "docx2pdf":
        if len(sys.argv) < 3:
            print("Usage: docx2pdf <input.docx> [output.pdf/folder]")
            sys.exit(1)
        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        converter.docx_to_pdf(input_file, output_file)

    elif command == "img2pdf":
        if len(sys.argv) < 4:
            print("Usage: img2pdf <img1> <img2> ... <output.pdf>")
            sys.exit(1)
        *images, output = sys.argv[2:]
        converter.images_to_pdf(images, output)

    elif command == "merge":
        if len(sys.argv) < 4:
            print("Usage: merge <pdf1> <pdf2> ... <output.pdf>")
            sys.exit(1)
        *pdfs, output = sys.argv[2:]
        converter.merge_pdfs(pdfs, output)

    else:
        print("❌ Unknown command")
