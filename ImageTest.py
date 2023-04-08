import pytesseract
from PIL import Image


# Load the image
img = Image.open('image.png')

# Extract text from the image
text = pytesseract.image_to_string(img)

# Print the extracted text
print(text)
