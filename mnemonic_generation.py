import os
import re
from dotenv import load_dotenv
load_dotenv()
# from groq import Groq
from openai import OpenAI
# import ollama


# =========================================================
# CONFIG
# =========================================================
# MODEL_NAME = "llama-3.3-70b-versatile"
# MODEL_NAME = "deepseek-r1:1.5b"
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0.55
MAX_TOKENS = 230
NUM_CANDIDATES = 10

APPROVED_MNEMONICS = {
    # Optional benchmark cases
}

# BANNED_ENDINGS = {
#     "care", "share", "somehow", "tonight", "divine", "you see",
#     "for you and me", "you and me", "with care", "take flight" ,"fine", "divine", "bright", "light", "flow", "go", "strong", "belong",
# "day and night", "through the flow", "as they go" ,"key", "glee", "free", "to state", "to create", "to know",
# "with glee", "great might" , "share", "state" , "care to share" ,"zero state"
# }

# PROMPT_TEMPLATE = """You are an educational mnemonic generator.

# A student has read the following educational text:
# {original_text}

# Important concepts (core + supporting):
# {concepts}

# Write EXACTLY 4 lines as a short educational mnemonic.
# Each line must teach one clear fact from the refined concepts.
# Avoid vague rhyme fillers.

# Rules:
# - Use the ORIGINAL TEXT as the main source of meaning.
# - Use the concept list only as guidance for the most important ideas.
# - You may use natural connecting words such as "are", "like", "helps", "through", or "because" when they improve clarity and meaning.
# - Use AABB rhyme scheme:
#   - line 1 rhymes with line 2
#   - line 3 rhymes with line 4
# - Choose rhyme endings from meaningful educational words in the topic when possible.
# - Each rhyming line must still teach a factual point.
# - Do NOT use empty filler rhyme endings such as key, glee, free, fine, divine, bright, light, for you and me.
# - Keep each line short and natural (roughly 7-10 syllables)
# - Be scientifically or academically accurate
# - Use clear, student-friendly English
# - Do NOT split words into syllables
# - Do NOT use hyphens inside words
# - Every line must teach one clear factual point
# - Do NOT use filler rhyme phrases such as "with care", "to last", "you and me", "somehow", "take flight"
# - Do NOT use vague filler words such as strong, bright, tight, day and night
# - Educational accuracy is more important than perfect rhyme
# - If a perfect rhyme sounds unnatural, prefer a simple natural rhyme
# - Focus on memorability, correctness, and natural phrasing rather than fancy poetry

BANNED_ENDINGS = {
    "for you and me", "you and me", "with care", "care to share", "take flight", "takes flight",
    "day and night", "through the flow", "as they go", "to state", "to create", "to know",
    "great might", "zero state", "you see", "fair", "oh my", "sky", "high", "fly", "try", "why", "gift"
    "might", "right", "bright", "light", "win", "begin", "quest", "prize", "shine", "clarify",
    "in play", "at play", "shows the way", "leads the way","share the load", "with the load", "where they begin",
    "it's fine", "is fine", "clear way", "understanding all", "error's call", "helps us know", "works with might"
}
PROMPT_TEMPLATE = """You are an educational mnemonic generator.

A student has read the following educational text:
{original_text}

Refined learning points:
{concepts}

Write EXACTLY 4 lines as a short educational mnemonic.

Rules:
-  Use AABB rhyme, but rhyme words should preferably be technical or concept-related rather than poetic filler:
    line 1 rhymes with line 2, line 3 rhymes with line 4.
- Each line must teach one clear factual point from the refined learning points.
- Use the original text as the source of meaning.
- Choose meaningful topic-related rhyme words when possible.
- Keep each line short and natural, roughly 7-10 syllables.
- Use clear student-friendly English.
- Do NOT add ideas not found in the original text.
- Avoid metaphorical rhyme words (pace, space, might, sight) unless they are part of the scientific meaning.
- Do not change grammar just to rhyme. Each line must be grammatically correct.
- Cover as many refined learning points as possible across the four lines.
- Do not use filler rhyme endings such as: oh my, sky, fly, high, might, right, win, quest, prize, shine, clarify.
- Every line must teach a real concept from the refined propositions.
- Do not add poetic filler just to rhyme.
- Do NOT use filler endings such as key, glee, free, fine, divine, bright, light, strong, tight, day and night, for you and me, with care, take flight, somehow, to state, to create, or to know, you know.
- Educational accuracy is more important than fancy poetry.

Return only the 4 lines, nothing else.
"""

# =========================================================
# PROMPT / API
# =========================================================
def build_prompt(concept_list: list, original_text: str = "") -> str:
    concepts_str = ", ".join(concept_list)
    return PROMPT_TEMPLATE.format(
        concepts=concepts_str,
        original_text=original_text
    )


def call_llm(prompt: str, temperature: float = TEMPERATURE) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=MODEL_NAME,   # gpt-4o-mini
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=MAX_TOKENS
    )

    return response.choices[0].message.content
# def call_llm(prompt: str, temperature: float = TEMPERATURE) -> str:

#     response = ollama.chat(
#         model=MODEL_NAME,   # e.g. "deepseek-r1"
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         options={
#             "temperature": temperature,
#             "num_predict": MAX_TOKENS   
#         }
#     )
#     return response["message"]["content"]
# def call_llm(prompt: str, temperature: float = TEMPERATURE) -> str:
#     client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
#     response = client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=temperature,
#         max_tokens=MAX_TOKENS,
#     )
#     return response.choices[0].message.content


# =========================================================
# CLEANING
# =========================================================
def clean_mnemonic(raw: str) -> str:
    lines = raw.strip().split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()
        line = re.sub(r"^\s*[\-\*\d]+[\.\)]?\s*", "", line)
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            cleaned.append(line)

    return "\n".join(cleaned[:4])


def normalize_text_for_checks(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def contains_split_words(text: str) -> bool:
    if re.search(r"\b[a-zA-Z]{1,4}(?:-[a-zA-Z]{1,4})+\b", text):
        return True

    for line in text.split("\n"):
        words = line.split()
        short_chunks = 0
        for w in words:
            if len(w) <= 3:
                short_chunks += 1
        if short_chunks >= max(3, len(words) // 2):
            return True

    return False


def ends_with_banned_phrase(line: str) -> bool:
    lower = line.lower().strip()
    lower = re.sub(r"[^\w\s]", "", lower) 
    for phrase in BANNED_ENDINGS:
        if lower.endswith(phrase):
            return True
    return False


# =========================================================
# RHYME / STRUCTURE HELPERS
# =========================================================
def get_last_word(line: str) -> str:
    words = re.findall(r"[A-Za-z']+", line.lower())
    return words[-1] if words else ""


def rhyme_key(word: str) -> str:
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return ""

    vowels = "aeiouy"
    last_vowel_pos = -1
    for i in range(len(word) - 1, -1, -1):
        if word[i] in vowels:
            last_vowel_pos = i
            break

    if last_vowel_pos == -1:
        return word[-3:] if len(word) >= 3 else word

    return word[last_vowel_pos:]


def rhyme_score(line_a: str, line_b: str) -> int:
    w1 = get_last_word(line_a)
    w2 = get_last_word(line_b)

    if not w1 or not w2:
        return 0

    if w1 == w2:
        return 0

    k1 = rhyme_key(w1)
    k2 = rhyme_key(w2)

    if k1 == k2 and len(k1) >= 2:
        return 3
    if len(k1) >= 2 and len(k2) >= 2 and k1[-2:] == k2[-2:]:
        return 2
    if len(k1) >= 1 and len(k2) >= 1 and k1[-1:] == k2[-1:]:
        return 1

    return 0


def count_syllables_word(word: str) -> int:
    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)

    if not word:
        return 0

    vowels = "aeiouy"
    count = 0
    prev_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel

    if word.endswith("e") and count > 1:
        count -= 1

    return max(1, count)


def count_syllables_line(line: str) -> int:
    words = re.findall(r"[A-Za-z']+", line)
    return sum(count_syllables_word(w) for w in words)


# =========================================================
# CONCEPT COVERAGE
# =========================================================
def concept_coverage_score(lines: list[str], concept_list: list[str], original_text: str = "") -> int:
    joined = normalize_text_for_checks(" ".join(lines))
    original_norm = normalize_text_for_checks(original_text)
    score = 0

    for concept in concept_list:
        concept_norm = normalize_text_for_checks(concept)
        if not concept_norm:
            continue

        tokens = [t for t in concept_norm.split() if len(t) > 3]

        if concept_norm in joined:
            score += 2
            continue

        token_hits = sum(1 for t in tokens if t in joined)
        if token_hits >= 2:
            score += 2
        elif token_hits == 1:
            score += 1

    if original_norm:
        original_tokens = {t for t in original_norm.split() if len(t) > 4}
        mnemonic_tokens = set(joined.split())
        overlap = len(original_tokens & mnemonic_tokens)

        if overlap >= 6:
            score += 3
        elif overlap >= 4:
            score += 2
        elif overlap >= 2:
            score += 1

    return score


# =========================================================
# VALIDATION / SCORING
# =========================================================
def unnatural_phrase_penalty(text: str) -> int:
    penalties = 0

    unnatural_patterns = [
        r"lead the play",
        r"start of the plain",
        r"output erodes",
        r"shows the way",
        r"at play",
        r"with might",
        r"share the load",
        r"understanding all",
        r"error's call",
        r"helps us know",
        r"where they begin",
        r"it's fine",
        r"clear way"
    ]

    lower = text.lower()

    for pattern in unnatural_patterns:
        if re.search(pattern, lower):
            penalties += 6

    return penalties

def validate_and_score_mnemonic(
    mnemonic: str,
    concept_list: list[str],
    original_text: str = ""
) -> tuple[bool, int, list[str]]:
    reasons = []
    score = 0

    if not mnemonic or not mnemonic.strip():
        return False, 0, ["Empty output"]
    

    if contains_split_words(mnemonic):
        return False, 0, ["Contains split/broken words"]
    

    lines = [line.strip() for line in mnemonic.split("\n") if line.strip()]

    if len(lines) != 4:
        return False, 0, [f"Expected 4 lines, got {len(lines)}"]

    for i, line in enumerate(lines, start=1):
        if len(line.split()) < 4:
            reasons.append(f"Line {i} too short")
        if len(line.split()) > 12:
            reasons.append(f"Line {i} too long")
        if ends_with_banned_phrase(line):
            reasons.append(f"Line {i} ends with filler phrase")
        if ends_with_banned_phrase(line):
            return False,0,["Banned filler ending"]

    a_score = rhyme_score(lines[0], lines[1])
    b_score = rhyme_score(lines[2], lines[3])

    if a_score == 0:
        reasons.append("Lines 1 and 2 do not rhyme well")
    else:
        score += a_score * 2

    if b_score == 0:
        reasons.append("Lines 3 and 4 do not rhyme well")
    else:
        score += b_score * 2

    syllable_penalty = 0
    for i, line in enumerate(lines, start=1):
        syl = count_syllables_line(line)
        if 7 <= syl <= 10:
            score += 2
        elif 6 <= syl <= 11:
            score += 1
        else:
            syllable_penalty += 1
            reasons.append(f"Line {i} syllables out of range ({syl})")

    score += 4* concept_coverage_score(lines, concept_list, original_text)

    score -= unnatural_phrase_penalty(mnemonic)

    last_words = [get_last_word(line) for line in lines]
    
    if len(set(last_words)) < 3:
        score -= 2
        reasons.append("Too much repetition in line endings")

    for line in lines:
        if not re.search(r"[A-Za-z]", line):
            reasons.append("Invalid non-text line")
        if line[0].islower():
            score -= 1

    hard_fail = any([
        "Contains split/broken words" in reasons,
        len(lines) != 4
    ])
    BAD_PHRASES = {
        "parts unit","does math to compute","cycle pace", "great might","zero state",
        "oh my","meets the sky","shows the way", "at play", "error's call","understanding all", 
        "leads the way","share the load", "helps us know","where they begin",
        "it's fine", "clear way", "works with might",
        "input brings data, output's the load" , "lead the play","start of the plain","output erodes",
    }

    for phrase in BAD_PHRASES:
        if phrase in mnemonic.lower():
            return False, 0, [f"Bad phrase: {phrase}"]
        
    is_valid = (not hard_fail) and (a_score > 0) and (b_score > 0) and (syllable_penalty <= 2)

    return is_valid, score, reasons


# =========================================================
# MULTI-CANDIDATE GENERATION
# =========================================================
def generate_candidates(prompt: str, num_candidates: int = NUM_CANDIDATES) -> list[str]:
    candidates = []
    for _ in range(num_candidates):
        raw = call_llm(prompt, temperature=TEMPERATURE)
        cleaned = clean_mnemonic(raw)
        candidates.append(cleaned)
    return candidates


def choose_best_candidate(
    candidates: list[str],
    concept_list: list[str],
    original_text: str = ""
) -> dict:
    scored = []

    for candidate in candidates:
        is_valid, score, reasons = validate_and_score_mnemonic(candidate, concept_list, original_text)
        scored.append({
            "mnemonic": candidate,
            "is_valid": is_valid,
            "score": score,
            "reasons": reasons,
        })

    valid_candidates = [c for c in scored if c["is_valid"]]
    if valid_candidates:
        return sorted(valid_candidates, key=lambda x: x["score"], reverse=True)[0]

    return sorted(scored, key=lambda x: x["score"], reverse=True)[0]


def make_lookup_key(concept_list: list[str]) -> str:
    normalized = sorted(normalize_text_for_checks(c) for c in concept_list if c.strip())
    return "|".join(normalized)


# =========================================================
# MAIN PIPELINE
# =========================================================
def generate_mnemonic(concept_list: list, original_text: str = "") -> dict:
    if not concept_list:
        return {"mnemonic": None, "error": "Empty concept list"}

    lookup_key = make_lookup_key(concept_list)
    if lookup_key in APPROVED_MNEMONICS:
        return {
            "mnemonic": APPROVED_MNEMONICS[lookup_key],
            "prompt_used": None,
            "concept_list": concept_list,
            "source": "approved_lookup",
            "score": 999,
            "validation_reasons": [],
            "error": None
        }

    prompt = build_prompt(concept_list, original_text)

    try:
        candidates = generate_candidates(prompt, num_candidates=NUM_CANDIDATES)
        best = choose_best_candidate(candidates, concept_list, original_text)

        return {
            "mnemonic": best["mnemonic"],
            "prompt_used": prompt,
            "concept_list": concept_list,
            "source": "llm_generated",
            "score": best["score"],
            "validation_reasons": best["reasons"],
            "all_candidates": candidates,
            "error": None if best["mnemonic"] else "No mnemonic generated"
        }

    except Exception as e:
        return {
            "mnemonic": None,
            "error": f"API error: {str(e)}"
        }


# =========================================================
# TEST
# =========================================================
if __name__ == "__main__":
    sample_text = (
        "Photosynthesis is the process by which plants use sunlight, water, "
        "and carbon dioxide to produce glucose and oxygen. Chloroplasts "
        "contain chlorophyll which absorbs light energy."
    )

    sample_concepts = [
        "photosynthesis",
        "sunlight",
        "water",
        "carbon dioxide",
        "glucose",
        "oxygen",
        "chloroplasts",
        "chlorophyll"
    ]

    result = generate_mnemonic(
        concept_list=sample_concepts,
        original_text=sample_text
    )

    if result["error"]:
        print("Error:", result["error"])
    else:
        print("\nBEST MNEMONIC")
        print("-" * 40)
        print(result["mnemonic"])
        print("-" * 40)
        print("Score:", result["score"])
        print("Reasons:", result["validation_reasons"])
        print("\nALL CANDIDATES:")
        for i, c in enumerate(result["all_candidates"], start=1):
            print(f"\nCandidate {i}:")
            print(c)

