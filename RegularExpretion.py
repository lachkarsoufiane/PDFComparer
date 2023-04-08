import pdfplumber
import re

file_path = "PhoneDirectory.pdf"

# Open the file
file = pdfplumber.open(file_path)

# Define the regular expression pattern
pattern = r'\+\d{1,2}\s\d{3}\s\d{3}'

# Loop through all pages of the PDF
for page in file.pages:

    # Extract the text from the page
    content = page.extract_text()

    # Use the re.findall method to extract all phone numbers
    phone_numbers = re.findall(pattern, content)

    # Print the list of phone numbers for this page
    if phone_numbers:
        print("Page", page.page_number, "contains the following phone numbers:")
        for number in phone_numbers:
            print(number)
    else:
        print("No phone numbers found on page", page.page_number)

# Close the PDF file
file.close()
