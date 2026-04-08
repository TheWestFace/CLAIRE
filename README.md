<div align="center">
  <h1><b> CLAIRE </b></h1>
</div>

## Overview

**CLAIRE (Clinician-Led AI for Relational Ethics)** is a Python-based experimental framework for studying how clinician-provided context influences large language model (LLM) responses in safety-critical mental health scenarios.

The system simulates patient–AI interactions under two conditions:

- **Dyadic setting**: Patient interacts with the LLM without any clinician context  
- **CLAIRE setting**: Patient interacts with the LLM with clinician-provided contextual guidance (e.g., risk level, safety instructions)

The goal is to evaluate whether clinician-injected context improves safety, empathy, and crisis handling in LLM responses.

---

## Research Objective

This project evaluates the hypothesis:

> LLMs operating under clinician-informed (CLAIRE) settings produce safer and more appropriate responses than LLMs operating in dyadic (patient-only) settings.

### Experiments Included

#### 1. Context Injection Study
- Compares dyadic vs CLAIRE responses
- Tests whether clinician context changes model behavior in safety-critical situations

#### 2. Crisis Escalation Behavior
- Evaluates whether the model:
  - Recognizes crisis language
  - Avoids harmful guidance
  - Provides appropriate escalation (e.g., crisis hotline suggestions)

---

## Repo Structure
```
claire/
├── src/
│ ├── gemini_client.py # Handles LLM API calls
│ ├── experiment.py # Prompt construction + experiment logic
│ ├── main.py # Runs full experiment pipeline
│
├── data/
│ ├── patients.csv # Patient inputs (test cases)
│ ├── clinicians.csv # Clinician context (dyadic vs CLAIRE)
│
├── results/
│ ├── outputs.json # Stored model outputs (generated)
│
├── .env # API key (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Create Environment
```
conda create -n claire-ai python=3.10
conda activate claire-ai
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Set Up API Key
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_api_key_here
```

### 4. Run Experiment
```
python src/main.py
```
After execution, results will be saved to:
```
results/outputs.json
```