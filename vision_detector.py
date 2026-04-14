import cv2
import pytesseract
from classifier import detect_multiple

# Tell pytesseract where tesseract is
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path):

    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found")
        return []

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    return lines


if __name__ == "__main__":

    extracted_lines = extract_text("test.png")

    print("\nExtracted Text:")
    print("----------------")

    for line in extracted_lines:
        print(line)


    print("\nDark Pattern Detection:")
    print("------------------------")

    results = detect_multiple(extracted_lines)

    dark_count = 0
    confidence_total = 0


    for r in results:

        print(f"\nText: {r['text']}")

        for pattern in r["patterns"]:

            print(
                f"Detected: {pattern['pattern']} "
                f"(Confidence: {round(pattern['confidence'],2)})"
            )

            if pattern["confidence"] > 0.45:
                dark_count += 1
                confidence_total += pattern["confidence"]


    # -----------------------------
    # Risk Score Calculation
    # -----------------------------

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