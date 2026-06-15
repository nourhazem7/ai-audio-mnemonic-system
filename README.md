# AI Audio Mnemonic Generator

## Bachelor Thesis Project

**Automatically Designing an Audio-Based Mnemonic System for Improved Learning and Recall in Educational Settings**

---

## Overview

This repository contains the implementation of a bachelor thesis project developed at **The German University in Cairo (GUC)**.

The project presents an AI-powered educational system that automatically transforms educational content into educationally meaningful audio mnemonics designed to improve learning and recall. The goal is to improve information retention and learning effectiveness by combining natural language processing, large language models, mnemonic generation techniques, and speech synthesis.

The system extracts important concepts from educational text, reconstructs them into meaningful learning propositions, generates rhyming mnemonics designed to maintain educational meaning and conceptual accuracy, and finally converts the generated mnemonic into audio. Rather than relying on a single generated mnemonic, the system follows an overgenerate-and-rerank strategy by producing multiple mnemonic candidates, evaluating them according to educational and structural criteria, and selecting the highest-scoring candidate for audio synthesis.

The system automatically:

- Extracts and ranks educational concepts
- Refines concepts into complete learning propositions
- Generates multiple mnemonic candidates
- Evaluates and re-ranks candidate mnemonics
- Selects the highest-scoring mnemonic
- Synthesizes the final audio mnemonic

---

## Authors

**Nour Hazem Mohsen**  
Computer Science and Engineering  
The German University in Cairo (GUC)

### Supervisor

**Dr. Yomna M. I. Hassan**

---

## System Pipeline

The system follows a multi-stage processing pipeline:

1. Educational Text Input
2. Text Preprocessing
3. Concept Extraction

   * KeyBERT keyword extraction
   * SciSpaCy entity extraction
4. Concept Selection and Ranking
5. Concept Refinement

   * DeepSeek-R1 (via Ollama)
6. Mnemonic Generation

   * GPT-4o-mini
7. Candidate Scoring and Re-ranking
8. Audio Synthesis

   * ElevenLabs
   * Audio post-processing using pydub

Final Output:

```text
Educational Text
      ↓
Concept Extraction
      ↓
Concept Selection
      ↓
Concept Refinement
      ↓
Mnemonic Generation
      ↓
Candidate Re-ranking
      ↓
Audio Synthesis
      ↓
Audio Mnemonic
```

## Technologies Used

### Natural Language Processing

* Python
* KeyBERT
* SciSpaCy

### Large Language Models

* DeepSeek-R1 (Concept Refinement)
* GPT-4o-mini (Mnemonic Generation)

### Local Inference Framework

* Ollama

### Audio Generation

* ElevenLabs
* pydub

### User Interface

* Streamlit

---

## Project Structure

```text
ai-audio-mnemonic-system/

├── app.py
├── pipeline.py
├── preprocessing.py
├── keybert_extraction.py
├── ner_extraction.py
├── concept_selection.py
├── concept_refinement.py
├── mnemonic_generation.py
├── audio_synthesis.py
│
├── assets/
├── outputs/
├── data/
│
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/nourhazem7/ai-audio-mnemonic-system.git
cd ai-audio-mnemonic-system
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
ELEVENLABS_API_KEY=YOUR_ELEVENLABS_API_KEY
```

---

## Running the System

Start the Streamlit application:

```bash
python -m streamlit run app.py
```

The web interface allows users to:

* Enter educational text
* View extracted concepts
* View refined learning propositions
* Read the generated mnemonic
* Listen to the generated audio mnemonic
* Download the generated audio mnemonic

---

## Research Contributions

This work contributes an end-to-end automated pipeline for educational mnemonic generation by integrating:

* Concept extraction and selection
* Semantic concept refinement
* Structured educational mnemonic generation
* Candidate evaluation and ranking
* Audio mnemonic synthesis

The system aims to preserve educational accuracy while improving memorability through mnemonic techniques and speech-based delivery.

---

## Future Work

Potential future extensions include:

* Personalized mnemonic generation
* Adaptive learner feedback integration
* Multi-language support
* Musical mnemonic generation
* Extension of the current sequential pipeline into a more collaborative multi-agent framework, where specialized agents can interact and contribute to concept extraction, semantic refinement, mnemonic generation, evaluation, and educational validation.
* Large-scale educational evaluation studies

---

## Disclaimer

This repository contains the implementation of an academic research project developed for educational and research purposes.
