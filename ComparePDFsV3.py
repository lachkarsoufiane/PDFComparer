import pdfplumber
import difflib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def compare_pdfs(pdf1_path, pdf2_path, output_path):
    # Open the two PDF files to compare
    with pdfplumber.open(pdf1_path) as pdf1, pdfplumber.open(pdf2_path) as pdf2:
        # Initialize the PDF canvas for the output file
        c = canvas.Canvas(output_path, pagesize=letter)
        # Iterate over the pages in the first PDF file
        for i, page1 in enumerate(pdf1.pages):
            # Extract the text from the first page
            text1 = page1.extract_text()
            # Extract the corresponding page from the second PDF file
            page2 = pdf2.pages[i]
            # Extract the text from the second page
            text2 = page2.extract_text()
            # Compute the difference between the two texts
            d = difflib.Differ()
            diff = list(d.compare(text1.splitlines(), text2.splitlines()))
            # Initialize the y coordinate for the text in the output file
            y = 750
            # Iterate over the lines in the difference
            for line in diff:
                if line[0] == " ":
                    # If the line is unchanged, add it to the output
                    c.drawString(100, y, line[2:])
                    y -= 20
                elif line[0] == "+":
                    # If the line was added in the second file, highlight it in green
                    c.setFillColorRGB(0, 1, 0)
                    c.drawString(100, y, line[2:])
                    y -= 20
                elif line[0] == "-":
                    # If the line was removed in the second file, highlight it in red
                    c.setFillColorRGB(1, 0, 0)
                    c.drawString(100, y, line[2:])
                    y -= 20
            # Move to the next page in the output file
            c.showPage()
        # Save the output file
        c.save()


# Example usage
compare_pdfs("file1.pdf", "file2.pdf", "diff.pdf")
