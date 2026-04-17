import pytesseract
import cv2


def detect_ui_deception(image):

    results = []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DICT
    )

    suspicious_words = [
        "only",
        "limited",
        "deal",
        "offer",
        "expires",
        "left",
        "stock",
        "fast",
        "recommended",
        "sponsored",
        "popular",
        "buy now",
        "add to cart"
    ]

    n_boxes = len(data['text'])

    for i in range(n_boxes):

        text = data['text'][i].strip()

        if text == "":
            continue

        height = data['height'][i]

        if height < 25:

            if any(word in text.lower() for word in suspicious_words):

                results.append({
                    "text": text,
                    "pattern": "ui_dark_pattern",
                    "confidence": 0.75
                })

    return results