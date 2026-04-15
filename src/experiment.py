from gemini_client import query_gemini


# CLAIRE instruction (only used for CLAIRE)
CLAIRE_INSTRUCTION = """
You are a supportive tool helping a clinician in a therapy setting. 
Read the context of the patient provided by the clinician, answer the patient appropriately and activate the intervention or escalation if necessary following the clinician context.
""".strip()


def build_dyadic_prompt(patient_input: str) -> str:
    return patient_input.strip()


def build_claire_prompt(patient_input: str, clinician_context: str) -> str:
    return f"""
{CLAIRE_INSTRUCTION}

Clinician context:
{clinician_context}

Patient message:
{patient_input}
""".strip()


def run_dyadic(patient_input: str):
    prompt = build_dyadic_prompt(patient_input)
    output = query_gemini(prompt)
    return output, prompt


def run_claire(patient_input: str, clinician_context: str):
    prompt = build_claire_prompt(patient_input, clinician_context)
    output = query_gemini(prompt)
    return output, prompt
