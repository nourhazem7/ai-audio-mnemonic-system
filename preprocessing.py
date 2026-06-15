import spacy
import re
from nltk.corpus import stopwords

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load stopwords
STOPWORDS = set(stopwords.words("english"))

def preprocess(text: str) -> dict:
    
    # Basic cleaning
    text_clean = re.sub(r"[^a-zA-Z\s]", " ", text)
    
    # Process with spaCy
    doc = nlp(text_clean)

    original_tokens = []
    cleaned_tokens = []

    for token in doc:

        if token.is_space:
            continue

        original_tokens.append(token.text)

        # Remove stopwords, punctuation, short tokens
        if (
            token.text.lower() not in STOPWORDS
            and token.is_alpha
            and len(token.lemma_) > 2
        ):
            cleaned_tokens.append(token.lemma_.lower())

    return {
        "cleaned_tokens": cleaned_tokens,
        "cleaned_text": " ".join(cleaned_tokens),
        "original_token_count": len(original_tokens),
        "stopwords_removed": len(original_tokens) - len(cleaned_tokens),
    }


if __name__ == "__main__":

    sample = """
    sample = "Mitochondria produce ATP through cellular respiration. Chloroplasts are involved in photosynthesis using sunlight, water, and carbon dioxide to produce glucose and oxygen."
    """

    result = preprocess(sample)

    print("Cleaned tokens:")
    print(result["cleaned_tokens"])

    print("\nCleaned text:")
    print(result["cleaned_text"])

    print(f"\nOriginal tokens: {result['original_token_count']}")
    print(f"Stopwords removed: {result['stopwords_removed']}")