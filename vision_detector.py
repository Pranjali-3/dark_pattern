import cv2
import pytesseract
from PIL import Image
from main_brain import detect_dark_pattern   # <-- connect AI brain

# Tell pytesseract where tesseract is
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found")
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    return text


if __name__ == "__main__":
    text = extract_text("test.png")

    print("\nExtracted Text:")
    print("----------------")
    print(text)

    print("\nDark Pattern Detection:")
    print("------------------------")

    lines = text.split("\n")

    for line in lines:
        if line.strip():
            result = detect_dark_pattern(line)
            print(result)