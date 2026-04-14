from classifier import detect_multiple
from vision_detector import extract_text
from ui_detector import detect_ui_deception


def detect_dark_patterns(image_path):

    print("\nExtracting Text...")
    print("----------------------")

    text = extract_text(image_path)

    print(text)

    print("\nAI Dark Pattern Detection")
    print("--------------------------")

    dark_patterns = []
    confidence_total = 0
    count = 0

    # -----------------------------
    # Text Based Detection
    # -----------------------------

    if isinstance(text, list):
        lines = text
    else:
        lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if line:

            result = detect_multiple([line])

            print("DEBUG:", result)

            # result is list
            for item in result:

                patterns = item.get("patterns", [])

                for r in patterns:

                    confidence = r.get("confidence", 0)

                    if confidence > 0.45:

                        dark_patterns.append({
                            "text": line,
                            "pattern": r.get("pattern"),
                            "confidence": confidence
                        })

                        confidence_total += confidence
                        count += 1

                        print(f"\nText: {line}")
                        print(f"Detected: {r.get('pattern')} ({round(confidence,2)})")


    # -----------------------------
    # UI Deception Detection
    # -----------------------------

    print("\nUI Deception Detection")
    print("--------------------------")

    ui_results = detect_ui_deception(image_path)

    for ui in ui_results:

        confidence = ui.get("confidence", 0)

        if confidence > 0.45:

            dark_patterns.append({
                "text": ui.get("text"),
                "pattern": ui.get("type"),
                "confidence": confidence
            })

            confidence_total += confidence
            count += 1

            print(f"\nUI Type: {ui.get('type')}")
            print(f"Text: {ui.get('text')}")
            print(f"Confidence: {confidence}")


    # -----------------------------
    # Risk Score
    # -----------------------------

    if count > 0:
        risk_score = round((confidence_total / count) * 100)
    else:
        risk_score = 0


    # -----------------------------
    # Severity
    # -----------------------------

    if risk_score < 30:
        severity = "LOW RISK 🟢"
    elif risk_score < 60:
        severity = "MEDIUM RISK 🟡"
    else:
        severity = "HIGH RISK 🔴"


    print("\n--------------------------")
    print(f"Total Dark Patterns: {count}")
    print(f"Risk Score: {risk_score}/100")
    print(f"Severity: {severity}")


    return {
        "patterns": dark_patterns,
        "risk_score": risk_score,
        "severity": severity
    }


# -----------------------------
# Testing
# -----------------------------

if __name__ == "__main__":

    detect_dark_patterns("test.png")