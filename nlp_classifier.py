from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

labels = [
    "False Urgency: forcing user to act quickly like 'Only 2 left'",
    "Confirmshaming: guilt-based opt-out like 'No thanks I hate saving money'",
    "Hidden Costs: extra fees revealed later",
    "Forced Continuity: subscription difficult to cancel",
    "Sneak into Basket: items automatically added to cart",
    "Privacy Zuckering: forcing user to share personal data",
    "Bait and Switch: user promised one thing but gets another",
    "Misleading Buttons: confusing button labels",
    "Trick Questions: confusing wording to mislead users",
    "No Dark Pattern"
]

def classify_texts(texts):
    results = []

    for text in texts:
        res = classifier(
            text,
            labels,
            hypothesis_template="This example is {}."
        )

        label = res["labels"][0]
        score = round(res["scores"][0], 2)

        if score < 0.4:
            label = "No Dark Pattern"

        results.append({
            "text": text,
            "pattern": label,
            "confidence": score
        })

    return results