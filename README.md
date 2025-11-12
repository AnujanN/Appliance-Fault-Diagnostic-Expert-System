# Household Appliance Fault Diagnostic — Expert System

Brief, practical expert system for diagnosing common household appliance faults. It combines a rule-based inference engine (Experta) with an LLM-based natural-language fact extractor and an LLM-powered explanation generator for improved explainability.

## Current Features

- Natural Language Input (NLU): Describe the problem in plain English (for example, "My washing machine won't drain and makes a grinding noise"). The system's LLM extractor converts natural text to structured facts (appliance, symptoms, observations).
- Manual Input Mode: Classic checkboxes and structured prompts for users who prefer precise selection.
- Rule-Based Expert Engine:
   - Forward-chaining inference implemented with Experta.
   - A knowledge base of ~67 realistic diagnostic rules (including combination rules for multi-symptom cases).
   - Confidence scoring and uncertainty handling that takes symptom counts into account.
- Explainability:
   - The engine produces structured, traceable reasoning and alternative hypotheses.
   - A focused LLM rewrites the technical reasoning for the primary diagnosis into a user-friendly "Why this recommendation?" explanation — the symbolic explanation remains visible and auditable.
- Recommendations and Action Types:
   - Combined output that includes the recommended steps and an action-type badge (DIY vs Professional).
   - Even when "Professional" is recommended, the system provides explicit technical details so the user and technician know what to expect.
- Handling Incomplete Information:
   - Graceful degradation: the system still provides useful troubleshooting tips when only partial details are available.
- Logging & Feedback Scaffolds:
   - Diagnosis and feedback logs are recorded (runtime JSON files) to support future training or analysis.
- Frontends:
   - Streamlit UI (original interactive demo).
   - Minimal professional Flask frontend (light theme) with consistent, readable styling for diagnosis, explanation, and recommendations.
- LLM Integration:
   - Primary fact extractor uses Groq (configurable via `GROQ_API_KEY`).
   - A simple rule-based extractor is used as a fallback if the LLM is unavailable.

## Files of interest

- `app.py` — Streamlit frontend.
- `app_flask.py` — Flask frontend (light, professional theme).
- `engine.py` — Experta-based diagnostic engine and rules.
- `llm_extractor.py` — Groq LLM-based fact extractor (text → Facts).
- `explanation_generator.py` — Focused LLM explanation generator for "Why this recommendation?" (rewrites expert reasoning to plain English).
- `test_llm.py` — Quick test harness for the LLM extractor.
- `diagnosis_logs.json` — Created at runtime; stores diagnosis cases.
- `feedback_data.json` — Created at runtime; stores user feedback for each case.
- `VIDEO_VOICEOVER_TELEPROMPTER.md` — Teleprompter-friendly spoken script for a 2-minute demo video.

## Quick Setup (Windows)

1. Create & activate a virtual environment (recommended):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Environment variables:

Create a `.env` file in the project root or set environment variables in PowerShell. Example `.env`:

```
GROQ_API_KEY=your_groq_api_key_here
```

Or set it in PowerShell for the current session:

```powershell
$env:GROQ_API_KEY = "your_groq_api_key_here"
```

## Running the project

- Streamlit UI:

```powershell
streamlit run app.py
```

- Flask UI:

```powershell
python app_flask.py
```

- Test the LLM extractor:

```powershell
python test_llm.py
```

## Notes & Best Practices

- LLM usage is scoped and focused: the extractor converts free text into structured facts; the explanation LLM only rewrites the primary diagnosis' reasoning to be user-friendly and does not overwrite the symbolic trace.
- Keep `diagnosis_logs.json` and `feedback_data.json` for future calibration and training.
- Add `.env` and `__pycache__/` to `.gitignore` and do not commit secrets.
- Safety: always include safety warnings in UI and recommendations (e.g., unplug appliances before working on them; call a professional for electrical/fuel hazards).

## Extensibility Ideas

- Collect feedback and use it to train a symptom classifier (e.g., TF-IDF + RandomForest or a light neural model).
- Train an NER model (spaCy) once enough labeled data is available to improve extractor accuracy.
- Implement a confidence calibrator that adjusts displayed percentages using historical feedback.

## Want help automating setup or docs?

I can:
- Add a quick-start PowerShell script that creates the venv and installs dependencies.
- Add a README section with example inputs → extractor output → engine reasoning to demonstrate the neuro-symbolic flow.
- Provide instructions and code changes for switching LLM providers (Groq ↔ OpenAI).

