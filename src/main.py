import json
import os
import time
import argparse
import pandas as pd

from experiment import run_experiment

DATA_PATH = "data/cases.csv"


def main():
    # -----------------------------
    # Parse batch arguments
    # -----------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0, help="Start index of batch")
    parser.add_argument("--size", type=int, default=5, help="Batch size")
    args = parser.parse_args()

    start = args.start
    size = args.size

    # -----------------------------
    # Load data
    # -----------------------------
    df = pd.read_csv(DATA_PATH)
    df = df.iloc[start:start + size]

    # -----------------------------
    # Output paths
    # -----------------------------
    os.makedirs("results", exist_ok=True)

    output_path = f"results/outputs_batch_{start}_{start + size - 1}.json"
    paired_output_path = f"results/paired_outputs_batch_{start}_{start + size - 1}.csv"

    results = []
    paired_rows = []

    print(f"Running batch from {start} to {start + size - 1}")

    # -----------------------------
    # Main loop
    # -----------------------------
    for _, row in df.iterrows():
        case_id = int(row["id"])
        prompt_type = str(row["prompt_type"]).strip().lower()
        patient_input = str(row["patient_input"]).strip()

        print(f"\nProcessing case {case_id} ({prompt_type})")

        case_outputs = {}

        # Alternate order to reduce bias
        conditions = ["dyadic", "claire"] if case_id % 2 == 1 else ["claire", "dyadic"]

        for condition in conditions:
            print(f"  → Running {condition}...")

            output, prompt = run_experiment(
                patient_input=patient_input,
                condition=condition
            )

            results.append({
                "id": case_id,
                "prompt_type": prompt_type,
                "condition": condition,
                "patient_input": patient_input,
                "model_output": output,
                "prompt_used": prompt,
            })

            case_outputs[condition] = output

            # -----------------------------
            # Rate limiting (VERY IMPORTANT)
            # -----------------------------
            time.sleep(7)

        # Save paired comparison
        paired_rows.append({
            "id": case_id,
            "prompt_type": prompt_type,
            "patient_input": patient_input,
            "dyadic_output": case_outputs.get("dyadic", ""),
            "claire_output": case_outputs.get("claire", ""),
        })

    # -----------------------------
    # Save results
    # -----------------------------
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    pd.DataFrame(paired_rows).to_csv(paired_output_path, index=False)

    print("\n Batch completed!")
    print(f"Saved JSON → {output_path}")
    print(f"Saved CSV  → {paired_output_path}")


if __name__ == "__main__":
    main()
