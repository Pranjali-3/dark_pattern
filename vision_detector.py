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

    dark_count = 0
    confidence_total = 0

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if line:
            result = detect_dark_pattern(line)
            print(result)

            if "no dark pattern" not in result["pattern"].lower():
                dark_count += 1
                confidence_total += result["confidence"]


    # Risk Score Calculation
    if dark_count > 0:
        avg_conf = confidence_total / dark_count
        risk_score = round(avg_conf * 100)
    else:
        risk_score = 0

    if risk_score < 30:
        severity = "LOW RISK 🟢"
    elif risk_score < 60:
        severity = "MEDIUM RISK 🟡"
    else:
        severity = "HIGH RISK 🔴"

    print("\n------------------------")
    print(f"Dark Patterns Found: {dark_count}")
    print(f"Risk Score: {risk_score}/100")
    print(f"Severity Level: {severity}")