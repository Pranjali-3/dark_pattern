import re
from classifier import detect_multiple
from vision_detector import extract_text
from ui_detector import detect_ui_deception


# Dark pattern phrases
DARK_PATTERN_PHRASES = [

    # Urgency
    "only few left",
    "only 2 left",
    "only 1 left",
    "selling fast",
    "almost sold out",
    "limited time",
    "deal ends",
    "offer ending",
    "hurry",
    "last chance",

    # Social pressure
    "people bought",
    "people ordered",
    "frequently bought",
    "popular choice",
    "most people choose",
    "recommended for you",

    # Subscription traps
    "auto renew",
    "cancel anytime",
    "free trial",

    # Pricing deception
    "best deal",
    "special price",
    "limited deal",
    "lightning deal",
    "exclusive deal",

    # Ecommerce
    "add protection plan",
    "add warranty",
    "bundle and save",
    "frequently bought together",
    "sponsored"
]


# Validate if meaningful dark pattern
def is_valid_dark_pattern(text):

    text_lower = text.lower()

    if len(text) < 5:
        return False

    if not re.search("[a-zA-Z]", text):
        return False

    for phrase in DARK_PATTERN_PHRASES:
        if phrase in text_lower:
            return True

    urgency_words = [
        "only",
        "limited",
        "deal",
        "offer",
        "expires",
        "left",
        "stock",
        "fast"
    ]

    if any(word in text_lower for word in urgency_words):
        return True

    return False


# Main Detection Function
def detect_dark_patterns(image):

    text = extract_text(image)

    dark_patterns = []

    # Convert OCR text to lines
    if isinstance(text, list):
        lines = text
    else:
        lines = text.split("\n")

    # Text based detection
    for line in lines:

        line = line.strip()

        if not is_valid_dark_pattern(line):
            continue

        result = detect_multiple([line])

        for item in result:

            for r in item.get("patterns", []):

                confidence = r.get("confidence", 0)

                if confidence > 0.50:

                    dark_patterns.append({
                        "text": line,
                        "pattern": r.get("pattern"),
                        "confidence": confidence
                    })


    # UI Detection
    ui_results = detect_ui_deception(image)

    for ui in ui_results:
        dark_patterns.append(ui)


    # -----------------------
    # Smart Risk Scoring
    # -----------------------

    risk_score = 0

    for pattern in dark_patterns:

        confidence = pattern["confidence"]
        text = pattern["text"].lower()

        # Strong dark patterns
        if any(word in text for word in [
            "only",
            "limited",
            "selling fast",
            "only left",
            "deal ends"
        ]):
            risk_score += confidence * 100

        # Medium
        elif any(word in text for word in [
            "offer",
            "recommended",
            "sponsored",
            "popular"
        ]):
            risk_score += confidence * 50

        # Weak
        else:
            risk_score += confidence * 25


    risk_score = min(100, int(risk_score))


    # -----------------------
    # Severity Level
    # -----------------------

    if risk_score < 25:
        severity = "LOW RISK 🟢"

    elif risk_score < 60:
        severity = "MEDIUM RISK 🟡"

    else:
        severity = "HIGH RISK 🔴"


    return {
        "patterns": dark_patterns,
        "risk_score": risk_score,
        "severity": severity
    }