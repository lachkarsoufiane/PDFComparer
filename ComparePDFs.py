import argparse
from io import BytesIO
import difflib
import PyPDF2


def compare_pdfs(pdf1, pdf2):
    # Load the two PDFs
    pdf1_reader = PyPDF2.PdfReader(pdf1)
    pdf2_reader = PyPDF2.PdfReader(pdf2)

    # Initialize the output string
    output = ""

    # Loop over each page in the PDFs
    for i in range(min(len(pdf1_reader.pages), len(pdf2_reader.pages))):
        # Extract the text from each page
        pdf1_text = pdf1_reader.pages[i].extract_text()
        pdf2_text = pdf2_reader.pages[i].extract_text()

        # Compare the text using the difflib library
        diff = difflib.Differ().compare(pdf1_text.splitlines(),
                                        pdf2_text.splitlines())

        # Add the differences to the output string

        for line in diff:
            if line.startswith("+"):
                output += f"+ {line[2:]}\n"
            elif line.startswith("-"):
                output += f"- {line[2:]}\n"

    # Return the output string
    return output


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Compare two PDF files")
    parser.add_argument("pdf1", help="Path to the first PDF file")
    parser.add_argument("pdf2", help="Path to the second PDF file")
    args = parser.parse_args()

    # Compare the PDFs and print the output
    pdf1_bytes = open(args.pdf1, "rb").read()
    pdf2_bytes = open(args.pdf2, "rb").read()
    output = compare_pdfs(BytesIO(pdf1_bytes), BytesIO(pdf2_bytes))
    print(output)
