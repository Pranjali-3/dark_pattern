from transformers import pipeline

model = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)


def detect_dark_pattern(text):

    labels = [
    "False Urgency like 'Only 2 left', 'Limited offer', 'Hurry now'",
    "Confirmshaming like 'No thanks I hate saving money'",
    "Sneak into Basket like items automatically added to cart",
    "Hidden Costs like fees revealed later or small star conditions",
    "Forced Continuity like subscription hard to cancel",
    "No dark pattern or normal UI text"
]

    result = model(text, candidate_labels=labels, multi_label=True)

    # Handle both return formats
    if isinstance(result, list):
        result = result[0]

    label = result["labels"][0]
    score = result["scores"][0]

    return {
        "text": text,
        "pattern": label,
        "confidence": round(score, 2)
    }