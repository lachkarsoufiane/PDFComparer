import argparse
from io import BytesIO
import difflib
import pdfplumber
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def compare_pdfs(pdf1, pdf2):
    # Carga los dos archivos PDF
    pdf1_reader = pdfplumber.open(pdf1)
    pdf2_reader = pdfplumber.open(pdf2)

    output = ""

    # Recorre cada página en los archivos PDF
    for i in range(min(len(pdf1_reader.pages), len(pdf2_reader.pages))):
        # Extrae el texto de cada página
        pdf1_text = pdf1_reader.pages[i].extract_text()
        pdf2_text = pdf2_reader.pages[i].extract_text()

        # Compara el texto usando la biblioteca difflib
        diff = difflib.Differ().compare(pdf1_text.splitlines(),
                                        pdf2_text.splitlines())

        # Agrega las diferencias a la cadena de salida
        for line in diff:
            if line.startswith("+"):
                output += f"+ {line[2:]}\n"
            elif line.startswith("-"):
                output += f"- {line[2:]}\n"

    return output


if __name__ == "__main__":
    # Analiza los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(description="Compare two PDF files")
    parser.add_argument("pdf1", help="Path to the first PDF file")
    parser.add_argument("pdf2", help="Path to the second PDF file")
    parser.add_argument("output", help="Path to the output PDF file")
    args = parser.parse_args()

    # Compara los archivos PDF e imprime la salida
    pdf1_bytes = open(args.pdf1, "rb").read()
    pdf2_bytes = open(args.pdf2, "rb").read()
    output_text = compare_pdfs(BytesIO(pdf1_bytes), BytesIO(pdf2_bytes))

    # Crea un nuevo documento PDF y escribe la salida
    with open(args.output, "wb") as f:
        c = canvas.Canvas(f, pagesize=letter)

        # Agrega el texto a la página
        textobject = c.beginText()
        textobject.setTextOrigin(50, 750)
        textobject.setFont("Helvetica", 12)
        for line in output_text.split("\n"):
            textobject.textLine(line)
        c.drawText(textobject)

        # Agrega un marcador para el texto
        c.bookmarkPage("Differences")
        c.addOutlineEntry("Differences", "Differences", 0)

        c.showPage()
        c.save()

    print(f"Output saved to {args.output}")
