from preprocessing import preprocess
from keybert_extraction import extract_keywords
from ner_extraction import extract_entities
from concept_selection import merge_and_clean_concepts, select_final_concepts
from concept_refinement import refine_concepts
from mnemonic_generation import generate_mnemonic
from audio_synthesis import synthesize_audio


def run_pipeline(text: str) -> dict:
    print("\n" + "=" * 50)
    print("STAGE 1: KEYWORD EXTRACTION PIPELINE")
    print("=" * 50)

    # Step 1: Preprocess
    print("\n[1/5] Preprocessing...")
    preprocessed = preprocess(text)
    print(f"  Original tokens   : {preprocessed['original_token_count']}")
    print(f"  Stopwords removed : {preprocessed['stopwords_removed']}")
    print(f"  Cleaned tokens    : {preprocessed['cleaned_tokens']}")

    # Step 2: KeyBERT
    print("\n[2/5] Extracting keywords with KeyBERT...")
    keybert_result = extract_keywords(preprocessed["cleaned_text"])
    print("  Keywords:")
    for kw in keybert_result["keywords"]:
        print(f"    {kw['term']} — score: {kw['score']}")

    # Step 3: NER
    print("\n[3/5] Extracting entities with SciSpaCy NER...")
    ner_result = extract_entities(text)
    print("  Entities:")
    for ent in ner_result["entities"]:
        print(f"    {ent['term']} — {ent['label']}")

    # Step 4: Merge + Select Concepts
    print("\n[4/5] Merging and selecting concepts...")

    merged_concepts = merge_and_clean_concepts(
        keybert_result["keywords"],
        ner_result["entities"]
    )

    selected_concepts = select_final_concepts(
        concepts=merged_concepts,
        original_text=text,
        max_core=5,
        max_total=8
    )

    final_concepts = selected_concepts["final_list"]

    print(f"  Merged + cleaned concepts: {[c['term'] for c in merged_concepts]}")
    print(f"  Core concepts: {selected_concepts['core']}")
    print(f"  Supporting concepts: {selected_concepts['supporting']}")
    print(f"  Final concept list ({len(final_concepts)}): {final_concepts}")

    # Step 5: Concept Refinement
    print("\n[5/5] Refining concepts into learning propositions...")

    refined_output = refine_concepts(
        concept_list=final_concepts,
        original_text=text,
        max_refined=5
    )

    refined_concepts = refined_output["refined_concepts"]

    print(f"  Refined concepts ({len(refined_concepts)}):")
    for concept in refined_concepts:
        print(f"    - {concept}")

    print(f"\n  Total after refinement: {len(refined_concepts)} → ready for Stage 2\n")

    # Stage 2: Mnemonic Generation
    print("=" * 50)
    print("STAGE 2: MNEMONIC GENERATION")
    print("=" * 50)

    mnemonic_result = generate_mnemonic(
        concept_list=refined_concepts,
        original_text=text
    )
    
    if mnemonic_result["error"]:
        print(f"  Error: {mnemonic_result['error']}")
        mnemonic_text = None
    else:
        mnemonic_text = mnemonic_result["mnemonic"]
        print("\nGenerated Mnemonic:\n")
        print(mnemonic_text)


    # Stage 3: Audio Synthesis
    print("\n" + "=" * 50)
    print("STAGE 3: AUDIO SYNTHESIS")
    print("=" * 50)

    if mnemonic_text:
        audio_result = synthesize_audio(mnemonic_text)

        if audio_result["error"]:
            print(f"  Error: {audio_result['error']}")
            audio_path = None
        else:
            audio_path = audio_result["audio_path"]
            print(f"\n  Duration: {audio_result['duration_seconds']:.1f} seconds")
            print(f"  Saved to: {audio_path}")
    else:
        audio_path = None

    return {
        "input_text": text,
        "preprocessed": preprocessed,
        "keywords": keybert_result["keywords"],
        "entities": ner_result["entities"],
        "merged_concepts": merged_concepts,
        "core_concepts": selected_concepts["core"],
        "supporting_concepts": selected_concepts["supporting"],
        "concept_list": final_concepts,
        "refined_concepts": refined_concepts,
        "mnemonic": mnemonic_text,
        "audio_path": audio_path,
    }


if __name__ == "__main__":
    print("\nEnter educational text.")
    print("Press Enter on an empty line when finished:\n")

    lines = []

    while True:
        line = input()

        if line.strip() == "":
            break

        lines.append(line)

    user_text = " ".join(lines).strip()

    if not user_text:
        print("No input provided.")
    else:
        result = run_pipeline(user_text)