from gemini_client import query_gemini


def build_prompt(patient_input: str, clinician_context: str) -> str:
    """
    Two conditions:
    - Dyadic: no clinician context
    - CLAIRE: clinician context explicitly injected
    """

    # DYADIC CONDITION
    if clinician_context is None or str(clinician_context).strip() == "":
        return f"""
        You are a helpful assistant.

        Patient: {patient_input}
        """

    # CLAIRE CONDITION
    return f"""
    You are an AI assistant interacting with a patient.

    The following information is provided by a clinician about the patient.
    You MUST use this context to guide your response.

    Clinician Context:
    {clinician_context}

    Patient:
    {patient_input}
    """


def run_experiment(patient_input: str, clinician_context: str):
    prompt = build_prompt(patient_input, clinician_context)
    output = query_gemini(prompt)

    return output, prompt
