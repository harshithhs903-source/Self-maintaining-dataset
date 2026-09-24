from transformers import pipeline
print("Loading Transformer model...")
# Load zero-shot classifier
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)
CANDIDATE_LABELS = [
    "Politics",
    "Business",
    "Tech",
    "Sports",
    "Entertainment",
    "Health",
    "Science",
    "World"
]
def classify_text(text):
    result = classifier(text, CANDIDATE_LABELS)
    return result["labels"][0]
# Demo text
sample_text = "Government announces new election reforms"
predicted_topic = classify_text(sample_text)
print("\nSample Text:", sample_text)
print("Predicted Topic:", predicted_topic)