import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Dark Pattern Examples
# -----------------------------

dark_patterns = {
    "false_urgency": [
        "Only 2 left",
        "Limited offer",
        "Hurry now",
        "Selling out fast",
        "Popular choice today"
    ],

    "forced_continuity": [
        "Subscribe now",
        "Start free trial",
        "Auto renew subscription",
        "Continue membership"
    ],

    "hidden_cost": [
        "Cancel anytime*",
        "Terms apply",
        "Additional charges may apply",
        "Processing fee added later"
    ],

    "confirm_shaming": [
        "No thanks I hate saving money",
        "I don't want better deals",
        "I prefer paying more"
    ],

    "misleading_ui": [
        "Best value",
        "Recommended plan",
        "Most popular option",
        "Highlighted premium plan"
    ]
}

# -----------------------------
# Create Embeddings
# -----------------------------

pattern_embeddings = {}

for pattern, examples in dark_patterns.items():
    pattern_embeddings[pattern] = model.encode(examples)


# -----------------------------
# Detection Function
# -----------------------------

def detect_dark_patterns(text):

    text_embedding = model.encode([text])[0]

    results = []

    for pattern, embeddings in pattern_embeddings.items():

        similarities = np.dot(embeddings, text_embedding) / (
            np.linalg.norm(embeddings, axis=1) * np.linalg.norm(text_embedding)
        )

        max_score = np.max(similarities)

        if max_score > 0.35:
            results.append({
                "pattern": pattern,
                "confidence": float(max_score)
            })

    return results


# -----------------------------
# Batch Detection
# -----------------------------

def detect_multiple(text_list):

    final_results = []

    for text in text_list:
        patterns = detect_dark_patterns(text)

        if patterns:
            final_results.append({
                "text": text,
                "patterns": patterns
            })

    return final_results


# -----------------------------
# Test
# -----------------------------

if __name__ == "__main__":

    test = [
        "Only 2 left! Hurry now",
        "Subscribe now to continue",
        "Cancel anytime* terms apply",
        "Most popular premium plan",
        "Selling out fast"
    ]

    result = detect_multiple(test)

    print("\nDark Pattern Detection\n")

    for r in result:
        print(r)