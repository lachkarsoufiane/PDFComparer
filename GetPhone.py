import pdfplumber
import re

file_path = "PhoneNumbers.pdf"

# Open the file
file = pdfplumber.open(file_path)

# Specify the page
page_1 = file.pages[1]

# Extract the text from the page
content = page_1.extract_text()

# Define the regular expression pattern
pattern = r'\+\d{1,2}\s\d{3}\s\d{2}\s\d{2}\s\d{2}'

# Use the re.findall method to extract all phone numbers
phone_numbers = re.findall(pattern, content)

# Print the list of phone numbers
print("The phone numbers are:")
for number in phone_numbers:
    print(number)
