import json
import time
import argparse
from pathlib import Path

import pandas as pd

from experiment import run_dyadic, run_claire

BASE_DIR = Path(__file__).resolve().parent.parent
CONTEXTS_PATH = BASE_DIR / "data" / "contexts.csv"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Patient input message to evaluate"
    )
    parser.add_argument(
        "--prompt_type",
        type=str,
        default="manual",
        help="Optional label such as clear, subtle, neutral, or manual"
    )
    parser.add_argument(
        "--results_subdir",
        type=str,
        default="cases_define",
        help="Subfolder inside results/ where outputs will be saved"
    )
    parser.add_argument(
        "--tag",
        type=str,
        default="manual_run",
        help="Tag used in output filenames"
    )
    parser.add_argument(
        "--sleep",
        type=int,
        default=7,
        help="Seconds to wait between API calls"
    )
    args = parser.parse_args()

    patient_input = args.input.strip()
    prompt_type = args.prompt_type.strip().lower()

    contexts_df = pd.read_csv(CONTEXTS_PATH)

    results_dir = BASE_DIR / "results" / args.results_subdir
    results_dir.mkdir(parents=True, exist_ok=True)

    output_json_path = results_dir / f"{args.tag}_outputs.json"
    output_csv_path = results_dir / f"{args.tag}_outputs.csv"
    paired_csv_path = results_dir / f"{args.tag}_paired_outputs.csv"

    all_results = []
    paired_row = {
        "prompt_type": prompt_type,
        "patient_input": patient_input,
        "dyadic_output": "",
    }

    print("Running manual input experiment")
    print(f"Patient input: {patient_input}")

    # 1) Dyadic
    print("\n→ Running dyadic...")
    dyadic_output, dyadic_prompt = run_dyadic(patient_input)

    all_results.append({
        "prompt_type": prompt_type,
        "run_type": "dyadic",
        "context_id": "",
        "context_type": "",
        "context_text": "",
        "patient_input": patient_input,
        "model_output": dyadic_output,
        "prompt_used": dyadic_prompt,
    })

    paired_row["dyadic_output"] = dyadic_output
    time.sleep(args.sleep)

    # 2) CLAIRE with 6 contexts
    for _, context_row in contexts_df.iterrows():
        context_id = int(context_row["id"])
        context_type = str(context_row["context_type"]).strip().lower()
        context_text = str(context_row["context_text"]).strip()

        print(f"→ Running claire context {context_id} ({context_type})...")

        claire_output, claire_prompt = run_claire(
            patient_input=patient_input,
            clinician_context=context_text,
        )

        all_results.append({
            "prompt_type": prompt_type,
            "run_type": "claire",
            "context_id": context_id,
            "context_type": context_type,
            "context_text": context_text,
            "patient_input": patient_input,
            "model_output": claire_output,
            "prompt_used": claire_prompt,
        })

        paired_row[f"claire_context_{context_id}_output"] = claire_output
        time.sleep(args.sleep)

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    pd.DataFrame(all_results).to_csv(output_csv_path, index=False)
    pd.DataFrame([paired_row]).to_csv(paired_csv_path, index=False)

    print("\n Experiment completed!")
    print(f"Saved JSON → {output_json_path}")
    print(f"Saved flat CSV → {output_csv_path}")
    print(f"Saved paired CSV → {paired_csv_path}")


if __name__ == "__main__":
    main()
