import re
from typing import List, Dict
import ollama


MODEL_NAME = "deepseek-r1:1.5b"
TEMPERATURE = 0.2
MAX_TOKENS = 700


def remove_thinking(text: str) -> str:
    """
    Removes DeepSeek R1 reasoning blocks if they appear.
    """
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.strip()


def clean_line(line: str) -> str:
    """
    Removes bullets, numbering, markdown, and extra spaces.
    """
    line = line.strip()

    # remove bullets / numbering
    line = re.sub(r"^\s*[\-\*\d]+[\.\)]?\s*", "", line)

    # remove markdown bold
    line = re.sub(r"\*\*", "", line)

    # normalize spaces
    line = re.sub(r"\s+", " ", line)

    return line.strip()


def remove_exact_duplicates(lines: List[str]) -> List[str]:
    """
    Removes only exact duplicates.
    """
    unique = []
    seen = set()

    for line in lines:
        key = line.lower().strip()

        if key not in seen:
            unique.append(line)
            seen.add(key)

    return unique


def build_refinement_prompt(
    concept_list: List[str],
    original_text: str,
    max_refined: int
) -> str:

    concepts = "\n".join(f"- {concept}" for concept in concept_list)

    return f"""
You are an educational concept refinement assistant.

Original educational text:
{original_text}

Extracted concepts:
{concepts}

Task:
Transform the extracted concepts into {max_refined} concise learning propositions.

Rules:
- Use only information from the original text.
- Transform the extracted concepts into concise learning propositions.
- Restore relationships between concepts when clearly stated in the text.
- Do not add new facts or external knowledge.
- Do not write isolated keywords.
- Do not write headings.
- Each proposition must be a complete sentence.
- Each proposition should contain only one clear educational idea.
- Preserve important technical terms.
- Preserve abbreviations only if they already appear in the original text.
- Do not create new abbreviations, equations, or symbolic expressions.
- Do not introduce mathematical notation unless it exists in the original text.
- Ensure propositions collectively cover the main concepts from the original text.
- Preserve distinct concepts such as definitions, variables, equations, components, predictions, and errors when present.
- Avoid repeating the same concept in different words.
- Keep each sentence clear, concise, and student-friendly.
- Return only the refined learning propositions, one per line.
"""


def call_refinement_llm(prompt: str, retries: int = 3) -> str:

    for attempt in range(retries):

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            options={
                "temperature": TEMPERATURE,
                "num_predict": MAX_TOKENS
            }
        )

        output = response["message"]["content"].strip()

        if output:
            return output

        print(f"Empty refinement output. Retrying... Attempt {attempt + 1}/{retries}")

    return ""

def parse_refined_output(
    raw_output: str,
    max_refined: int,
    concept_list: List[str]
) -> List[str]:

    raw_output = remove_thinking(raw_output)

    lines = raw_output.split("\n")

    refined = []

    for line in lines:

        line = clean_line(line)

        if not line:
            continue

        # skip accidental explanation lines
        if line.lower().startswith(
            ("here are", "these are", "refined")
        ):
            continue

        # avoid tiny meaningless fragments
        if len(line.split()) < 5:
            continue

        # add punctuation if missing
        if not line.endswith((".", "!", "?")):
            line = line + "."

        # remove broken / incomplete endings
        bad_endings = (
            "to.", "and.", "or.","the.",
            "a.", "an.", "of.", "in.",
            "with.","from.", "through.", "while.","based on.","such as."
        )

        if line.lower().endswith(bad_endings):
            continue
        if "each proposition" in line.lower():
            continue
        if "students understand" in line.lower():
            continue
        refined.append(line)

    # remove only exact duplicates
    refined = remove_exact_duplicates(refined)

    # fallback protection
    if not refined:

        refined = [
            concept.strip().rstrip(".") + "."
            for concept in concept_list[:max_refined]
            if concept.strip()
        ]

    return refined[:max_refined]


def refine_concepts(
    concept_list: List[str],
    original_text: str,
    max_refined: int = 5
) -> Dict:
    """
    LLM-based concept refinement:
    Uses DeepSeek R1 through Ollama to transform extracted concepts
    into meaningful learning propositions before mnemonic generation.
    """

    if not concept_list:
        return {
            "refined_concepts": [],
            "all_refined": [],
            "raw_output": "",
            "error": "Empty concept list"
        }

    prompt = build_refinement_prompt(
        concept_list=concept_list,
        original_text=original_text,
        max_refined=max_refined
    )

    try:

        raw_output = call_refinement_llm(prompt)

        # debug print during testing
        print("\nRAW REFINEMENT OUTPUT:")
        print(raw_output)

        refined = parse_refined_output(
            raw_output=raw_output,
            max_refined=max_refined,
            concept_list=concept_list
        )

        return {
            "refined_concepts": refined,
            "all_refined": refined,
            "raw_output": raw_output,
            "error": None
        }

    except Exception as e:

        return {
            "refined_concepts": [],
            "all_refined": [],
            "raw_output": "",
            "error": str(e)
        }

