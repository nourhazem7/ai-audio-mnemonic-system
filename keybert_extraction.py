from keybert import KeyBERT

kw_model = KeyBERT()

def extract_keywords(cleaned_text: str, top_n: int = 5) -> dict:
    keywords = kw_model.extract_keywords(
        cleaned_text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=top_n
    )

    return {
        "keywords": [{"term": kw, "score": round(score, 4)} for kw, score in keywords]
    }

if __name__ == "__main__":
    sample_cleaned = "photosynthesis process plant use sunlight water carbon dioxide produce oxygen energy form glucose"

    result = extract_keywords(sample_cleaned)
    print("Keywords:")
    for kw in result["keywords"]:
        print(f"  {kw['term']} — score: {kw['score']}")