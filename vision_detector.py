import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.convertScaleAbs(gray, alpha=1.8, beta=0)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    resized = cv2.resize(
        thresh,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    text = pytesseract.image_to_string(resized)

    return text