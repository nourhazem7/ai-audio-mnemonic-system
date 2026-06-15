import spacy

nlp = spacy.load("en_core_sci_sm")

def extract_entities(text: str) -> dict:
    doc = nlp(text)

    entities = []
    seen = set()

    for ent in doc.ents:
        entity_text = ent.text.strip()

        if len(entity_text) < 3:
            continue
        if entity_text.isdigit():
            continue

        key = entity_text.lower()
        if key in seen:
            continue

        seen.add(key)

        entities.append({
            "term": entity_text,
            "label": ent.label_
        })

    return {
    "entities": entities,
    "entity_count": len(entities)
}

if __name__ == "__main__":
    sample = """
    Mitochondria produce ATP through cellular respiration.
    Chloroplasts are involved in photosynthesis.
    """

    result = extract_entities(sample)

    print("Entities:")
    for ent in result["entities"]:
        print(f"{ent['term']} — {ent['label']}")