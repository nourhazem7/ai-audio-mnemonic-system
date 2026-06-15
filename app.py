import streamlit as st
from pipeline import run_pipeline

st.set_page_config(
    page_title="AI Audio Mnemonic Generator",
    page_icon="🎧",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
    color: #2F3440;
}

.subtitle {
    font-size: 18px;
    color: #6B7280;
    margin-bottom: 24px;
}

/* Full pipeline bar */
.pipeline-bar {
    background: #FFFFFF;
    border: 1px solid #DCE5F1;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 26px;
    box-shadow: 0px 4px 14px rgba(31, 41, 55, 0.05);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
}

.pipeline-step {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
    min-width: 0;
}

.pipeline-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #2F80ED, #4F9DFF);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
    box-shadow: 0px 5px 12px rgba(47, 128, 237, 0.25);
}

.pipeline-number {
    display: inline-flex;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #2F80ED;
    color: white;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
    margin-right: 6px;
}

.pipeline-title {
    font-weight: 800;
    color: #1F2937;
    font-size: 15px;
    white-space: nowrap;
}

.pipeline-subtitle {
    color: #6B7280;
    font-size: 13px;
    margin-top: 3px;
    white-space: nowrap;
}

.pipeline-arrow {
    color: #AAB3C2;
    font-size: 30px;
    font-weight: 300;
    flex-shrink: 0;
}

.stage-label {
    color: #6FB8F5;
    letter-spacing: 1.5px;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 8px;
}

.card {
    background-color: #EEF3FA;
    padding: 24px;
    border-radius: 14px;
    border: 1px solid #DCE5F1;
    margin-bottom: 20px;
    color: #1F2937;
    min-height: 125px;
}

.concept-tag {
    display: inline-block;
    background-color: #4B6EA8;
    color: white;
    padding: 10px 16px;
    margin: 6px;
    border-radius: 24px;
    font-size: 15px;
    font-weight: 700;
}

.mnemonic-box {
    background-color: #123F2A;
    color: #5CFF8A;
    padding: 22px 24px;
    border-radius: 14px;
    font-size: 19px;
    font-weight: 700;
    line-height: 1.65;
    width: fit-content;
    min-width: 430px;
    max-width: 560px;
    margin-top: 10px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.12);
}

.big-number {
    font-size: 34px;
    font-weight: 500;
    color: #2F3440;
    margin-top: -8px;
}

.stats-row {
    margin-top: 35px;
    margin-bottom: 24px;
    padding-bottom: 14px;
    border-bottom: 1px solid #E5E7EB;
}

/* Red centered Streamlit button */
div.stButton {
    display: flex;
    justify-content: center;
}

div.stButton > button:first-child {
    background-color: #E9252D;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2.4rem;
    font-size: 18px;
    font-weight: 800;
    box-shadow: 0px 4px 10px rgba(233, 37, 45, 0.25);
    margin-top: 16px;
    margin-bottom: 34px;
}

div.stButton > button:first-child:hover {
    background-color: #C91F26;
    color: white;
    border: none;
}

div.stButton > button:first-child:active {
    background-color: #B91C1C;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AI Audio Mnemonic Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Transform educational text into refined concepts, memorable mnemonics, and audio output.</div>',
    unsafe_allow_html=True
)

# Pipeline bar inside one actual container
st.markdown("""
<div class="pipeline-bar">
    <div class="pipeline-step">
        <div class="pipeline-icon">📝</div>
        <div>
            <div class="pipeline-title"><span class="pipeline-number">1</span>Input</div>
            <div class="pipeline-subtitle">Educational Text</div>
        </div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-icon">🔍</div>
        <div>
            <div class="pipeline-title"><span class="pipeline-number">2</span>Extract Concepts</div>
            <div class="pipeline-subtitle">Keywords & Entities</div>
        </div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-icon">💡</div>
        <div>
            <div class="pipeline-title"><span class="pipeline-number">3</span>Refine Concepts</div>
            <div class="pipeline-subtitle">Learning Propositions</div>
        </div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-icon">✨</div>
        <div>
            <div class="pipeline-title"><span class="pipeline-number">4</span>Generate Mnemonic</div>
            <div class="pipeline-subtitle">AABB Rhyme</div>
        </div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-icon">🎧</div>
        <div>
            <div class="pipeline-title"><span class="pipeline-number">5</span>Synthesize Audio</div>
            <div class="pipeline-subtitle">Audio Mnemonic</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

input_text = st.text_area(
    "Enter educational text",
    height=180,
    placeholder="Paste your educational content here..."
)

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    run_button = st.button(
        "Generate Mnemonic",
        use_container_width=True
    )

if run_button and input_text.strip():

    with st.spinner("Running full AI mnemonic pipeline..."):
        result = run_pipeline(input_text)

    # -----------------------------
    # Concept Extraction + Refinement
    # -----------------------------
    col1, col2 = st.columns([1, 1.4])

    with col1:
        st.markdown('<div class="stage-label">CONCEPT EXTRACTION</div>', unsafe_allow_html=True)
        st.subheader("Extracted Concepts")

        concepts_html = ""
        for concept in result["concept_list"]:
            concepts_html += f'<span class="concept-tag">{concept}</span>'

        st.markdown(
            f"""
            <div class="card">
                {concepts_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown('<div class="stage-label">CONCEPT REFINEMENT</div>', unsafe_allow_html=True)
        st.subheader("Refined Learning Propositions")

        propositions_html = "<ul>"
        for proposition in result["refined_concepts"]:
            propositions_html += f"<li>{proposition}</li>"
        propositions_html += "</ul>"

        st.markdown(
            f"""
            <div class="card">
                {propositions_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------
    # Scores BEFORE mnemonic/audio
    # -----------------------------
    st.markdown('<div class="stats-row">', unsafe_allow_html=True)

    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:
        st.caption("Concepts Extracted")
        st.markdown(
            f"<div class='big-number'>{len(result['concept_list'])}</div>",
            unsafe_allow_html=True
        )

    with score_col2:
        st.caption("Refined Propositions")
        st.markdown(
            f"<div class='big-number'>{len(result['refined_concepts'])}</div>",
            unsafe_allow_html=True
        )

    with score_col3:
        st.caption("Audio Generated")
        audio_status = "✓" if result.get("audio_path") else "—"
        st.markdown(
            f"<div class='big-number'>{audio_status}</div>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # Mnemonic + Audio
    # -----------------------------
    mnemonic_col, audio_col = st.columns([1, 1.25])

    with mnemonic_col:
        st.markdown('<div class="stage-label">MNEMONIC GENERATION</div>', unsafe_allow_html=True)
        st.subheader("Generated Mnemonic")

        mnemonic_text = result["mnemonic"].replace("\n", "<br>")

        st.markdown(
            f"""
            <div class="mnemonic-box">
                {mnemonic_text}
            </div>
            """,
            unsafe_allow_html=True
        )

    with audio_col:
        st.markdown('<div class="stage-label">AUDIO SYNTHESIS</div>', unsafe_allow_html=True)
        st.subheader("Audio Output")

        if result.get("audio_path"):
            st.audio(result["audio_path"], format="audio/mp3")
        else:
            st.info("Audio was not generated.")

elif run_button:
    st.warning("Please enter educational text first.")
