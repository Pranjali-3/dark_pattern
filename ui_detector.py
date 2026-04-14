import cv2
import pytesseract
import numpy as np

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def detect_ui_deception(image_path):

    img = cv2.imread(image_path)

    if img is None:
        print("Error: Image not found")
        return []

    h, w, _ = img.shape

    # Get OCR data with bounding boxes
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    n_boxes = len(data['text'])

    suspicious_elements = []

    for i in range(n_boxes):

        text = data['text'][i].strip()

        if text == "":
            continue

        x = data['left'][i]
        y = data['top'][i]
        width = data['width'][i]
        height = data['height'][i]

        confidence = int(data['conf'][i])

        # -----------------------------
        # Rule 1: Very Small Text
        # -----------------------------

        if height < 15 and confidence > 40:
            suspicious_elements.append({
                "type": "tiny_text",
                "text": text,
                "confidence": 0.7,
                "position": (x, y)
            })

        # -----------------------------
        # Rule 2: Bottom Screen Hidden Text
        # -----------------------------

        if y > (h * 0.75):
            suspicious_elements.append({
                "type": "bottom_hidden_text",
                "text": text,
                "confidence": 0.6,
                "position": (x, y)
            })

        # -----------------------------
        # Rule 3: Star (*) disclaimer
        # -----------------------------

        if "*" in text or "terms" in text.lower():
            suspicious_elements.append({
                "type": "hidden_disclaimer",
                "text": text,
                "confidence": 0.85,
                "position": (x, y)
            })

        # -----------------------------
        # Rule 4: Small width suspicious text
        # -----------------------------

        if width < 40 and height < 20:
            suspicious_elements.append({
                "type": "misleading_small_text",
                "text": text,
                "confidence": 0.65,
                "position": (x, y)
            })

    return suspicious_elements


# -----------------------------
# Testing
# -----------------------------

if __name__ == "__main__":

    results = detect_ui_deception("test.png")

    print("\nUI Deception Detection")
    print("-------------------------")

    if len(results) == 0:
        print("No UI deception detected")

    else:
        for r in results:
            print(f"\nType: {r['type']}")
            print(f"Text: {r['text']}")
            print(f"Confidence: {r['confidence']}")
            print(f"Position: {r['position']}")