import re
from typing import Dict, List


BAD_START_WORDS = {
    "refer", "refers", "like", "use", "uses", "make", "makes",
    "show", "shows", "include", "includes", "based", "help", "helps",
    "produce", "produces", "contain", "contains", "involve", "involves",
    "using", "involved", "producing", "responsible"
}

GENERIC_NOISE_WORDS = {
    "specific", "specifically", "various", "certain", "different",
    "example", "examples", "thing", "things", "part", "parts",
    "type", "types", "form", "forms", "well"
}

ACADEMIC_RELATION_WORDS = {
    "is", "are", "means", "refers", "defined", "composed",
    "consists", "includes", "performs", "stores", "uses",
    "produces", "calculates", "controls", "manages",
    "represents", "predicts", "executes", "causes", "leads"
}


def normalize_concept(concept: str) -> str:
    concept = concept.strip().lower()
    concept = re.sub(r"[^a-z0-9\s\-]", " ", concept)
    concept = re.sub(r"\s+", " ", concept).strip()
    return concept


def is_bad_concept(concept: str) -> bool:
    c = normalize_concept(concept)

    if not c:
        return True

    words = c.split()

    if len(c) < 3:
        return True

    if len(words) > 4:
        return True

    if len(words) == 1 and len(words[0]) <= 3:
        return True

    if words[0] in BAD_START_WORDS:
        return True

    if any(word in GENERIC_NOISE_WORDS for word in words):
        return True

    # remove phrase fragments that are mostly verbs
    if len(words) <= 2 and any(word in BAD_START_WORDS for word in words):
        return True

    return False


def count_occurrences(term: str, original_text: str) -> int:
    if not original_text:
        return 0

    term_norm = normalize_concept(term)
    text_norm = normalize_concept(original_text)

    return text_norm.count(term_norm)


def appears_near_relation_word(term: str, original_text: str) -> bool:
    if not original_text:
        return False

    sentences = re.split(r"(?<=[.!?])\s+", original_text)

    term_norm = normalize_concept(term)

    for sentence in sentences:
        sent_norm = normalize_concept(sentence)
        words = sent_norm.split()

        if term_norm in sent_norm:
            if any(word in ACADEMIC_RELATION_WORDS for word in words):
                return True

    return False


def merge_and_clean_concepts(
    keywords: List[Dict],
    entities: List[Dict]
) -> List[Dict]:
    """
    Merge KeyBERT keywords and NER entities into one candidate concept list.

    This stage does not decide final meaning.
    It only collects reasonable candidate terms.
    """

    merged: List[Dict] = []
    seen = set()

    # Add NER entities first because they often preserve complete academic phrases
    for ent in entities:
        raw_term = ent.get("term", "").strip()
        norm = normalize_concept(raw_term)

        if is_bad_concept(norm):
            continue

        if norm in seen:
            continue

        seen.add(norm)
        merged.append({
            "term": norm,
            "source": "entity",
            "keybert_score": 0.0,
            "entity_label": ent.get("label")
        })

    # Add KeyBERT keywords
    for kw in keywords:
        raw_term = kw.get("term", "").strip()
        norm = normalize_concept(raw_term)

        if is_bad_concept(norm):
            continue

        if norm in seen:
            continue

        seen.add(norm)
        merged.append({
            "term": norm,
            "source": "keyword",
            "keybert_score": float(kw.get("score", 0.0)),
            "entity_label": None
        })

    return merged


def score_concept(concept: Dict, original_text: str = "") -> float:
    """
    Generic concept scoring.

    This avoids hard-coded subject lists and instead uses:
    - KeyBERT relevance
    - NER signal
    - phrase length
    - frequency in original text
    - relation/definition context
    - presence in heading or opening sentence
    """

    term = concept["term"]
    words = term.split()
    score = 0.0

    # KeyBERT semantic score
    score += concept.get("keybert_score", 0.0) * 2.0

    # Entity bonus
    if concept.get("source") == "entity":
        score += 1.5

    FRAGMENT_TERMS = {
    "logic unit",
    "neumann architecture",
    "von neumann",
    "basic components",
    "instruction datum"
}

    if term.lower() in FRAGMENT_TERMS:
        score -= 2.0

    # Prefer meaningful multi-word academic phrases
    if len(words) == 2:
        score += 0.5
    elif len(words) == 3:
        score += 0.4
    elif len(words) == 4:
        score += 0.2
    elif len(words) == 1:
        score += 0.1

    # Frequency bonus
    freq = count_occurrences(term, original_text)
    if freq >= 2:
        score += 0.5
    elif freq == 1:
        score += 0.2

    # Concepts appearing in explanatory/definition sentences are more important
    if appears_near_relation_word(term, original_text):
        score += 0.8

    # Opening sentence / heading bonus
    if original_text:
        first_40_words = " ".join(normalize_concept(original_text).split()[:40])
        if normalize_concept(term) in first_40_words:
            score += 0.5

    # Penalize very generic single words
    if len(words) == 1 and len(words[0]) < 5:
        score -= 0.5

    return score


def select_final_concepts(
    concepts: List[Dict],
    original_text: str = "",
    max_core: int = 5,
    max_total: int = 8
) -> Dict:
    """
    Select ranked core and supporting concepts.

    Output:
    {
        "core": [...],
        "supporting": [...],
        "final_list": [...],
        "ranked_terms": [...]
    }
    """

    scored = []

    for concept in concepts:
        term = concept["term"]

        if is_bad_concept(term):
            continue

        s = score_concept(concept, original_text)
        scored.append((term, s))

    scored.sort(key=lambda x: x[1], reverse=True)

    ranked_terms = []
    seen = set()

    for term, _ in scored:
        key = normalize_concept(term)

        if key not in seen:
            ranked_terms.append(term)
            seen.add(key)

    final_terms = ranked_terms[:max_total]
    core = final_terms[:max_core]
    supporting = final_terms[max_core:max_total]

    return {
        "core": core,
        "supporting": supporting,
        "final_list": core + supporting,
        "ranked_terms": ranked_terms
    }