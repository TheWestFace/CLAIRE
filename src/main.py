import pandas as pd
import json
import os
from experiment import run_experiment

# Load data
patients = pd.read_csv("data/patients.csv")
clinicians = pd.read_csv("data/clinicians.csv")

os.makedirs("results", exist_ok=True)

results = []

for i in range(len(patients)):
    patient_input = patients.iloc[i]["input"]
    clinician_context = clinicians.iloc[i]["context"]

    output, prompt = run_experiment(patient_input, clinician_context)

    condition = "dyadic" if str(clinician_context).strip() == "" else "claire"

    results.append(
        {
            "id": int(patients.iloc[i]["id"]),
            "condition": condition,
            "patient_input": patient_input,
            "clinician_context": (
                clinician_context if str(clinician_context).strip() != "" else None
            ),
            "model_output": output,
            "prompt_used": prompt,
        }
    )

# Save with timestamped file
output_path = "results/outputs.json"

with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"✅ Experiment complete. Saved to {output_path}")
