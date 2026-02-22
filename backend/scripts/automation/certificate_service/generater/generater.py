from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os

os.makedirs("certificates", exist_ok=True)


TEMPLATE = "certificate_template.pdf"

# ---- CHANGE THESE ONCE ----
NAME_X = 425   # X coordinate of {name}
NAME_Y = 330   # Y coordinate of {name}
FONT_SIZE = 24
# --------------------------------

def create_overlay(name):
    packet = BytesIO()

    c = canvas.Canvas(packet, pagesize=A4)
    c.setFont("Times-Italic", FONT_SIZE)

    # Draw name exactly where placeholder exists
    c.drawCentredString(NAME_X, NAME_Y, name)

    c.save()
    packet.seek(0)
    return PdfReader(packet)


def generate_certificate(name):
    template = PdfReader(TEMPLATE)
    writer = PdfWriter()

    overlay = create_overlay(name)

    page = template.pages[0]
    page.merge_page(overlay.pages[0])

    writer.add_page(page)

    filename = f"certificates/{name}.pdf"
    with open(filename, "wb") as f:
        writer.write(f)


# Read names
with open("students.txt") as f:
    names = [n.strip() for n in f if n.strip()]

for name in names:
    generate_certificate(name)

print("✅ Certificates generated!")