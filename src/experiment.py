from gemini_client import query_gemini

# ----------------------------------------
# Shared base assistant context (used in BOTH conditions)
# ----------------------------------------
BASE_CONTEXT = """
You are a helpful and supportive assistant.
Respond empathetically, respectfully, and appropriately to the user's message.
""".strip()


# ----------------------------------------
# Fixed clinician context (ONLY for CLAIRE)
# ----------------------------------------
CLINICIAN_CONTEXT = """
The patient may be experiencing emotional distress, depression, hopelessness,
withdrawal, or reduced motivation, even if they do not state it explicitly.

Respond in a supportive, empathetic, and clinically sensitive way.
Acknowledge the patient’s feelings without dismissing or minimizing them.

Do not provide harmful, shaming, or overly casual responses.

If the message suggests significant distress, gently encourage the patient
to seek support from a trusted person or a mental health professional.

If the distress appears acute or severe, respond with appropriate urgency
and encourage immediate support.
""".strip()


# ----------------------------------------
# Prompt builder
# ----------------------------------------
def build_prompt(patient_input: str, condition: str = "dyadic") -> str:
    if condition == "dyadic":
        return f"""
{BASE_CONTEXT}

Patient message:
{patient_input}
""".strip()

    elif condition == "claire":
        return f"""
{BASE_CONTEXT}

Clinician context:
{CLINICIAN_CONTEXT}

Patient message:
{patient_input}
""".strip()

    else:
        raise ValueError(f"Unknown condition: {condition}")


# ----------------------------------------
# Run one experiment call
# ----------------------------------------
def run_experiment(patient_input: str, condition: str):
    prompt = build_prompt(
        patient_input=patient_input,
        condition=condition,
    )

    output = query_gemini(prompt)

    return output, prompt

