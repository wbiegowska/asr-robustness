import json
import argparse
import os
from jiwer import cer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, help="Input predictions JSONL")
    parser.add_argument("--output_metrics", required=True, help="Output JSON file for the score")
    args = parser.parse_args()

    with open(args.manifest, 'r', encoding='utf-8') as f:
        records = [json.loads(line) for line in f]

    refs = []
    preds = []

    for r in records:
        # The lab instructions say to strip spaces before comparing
        # because different tools group phonemes differently
        ref = r['ref_phon'].replace(" ", "") if r.get('ref_phon') else ""
        pred = r['pred_phon'].replace(" ", "") if r.get('pred_phon') else ""
        
        refs.append(ref)
        preds.append(pred)

    # We use jiwer's Character Error Rate (cer) on the stripped strings, 
    # which perfectly calculates the Phoneme Error Rate (S + D + I / N)
    error_rate = cer(refs, preds)

    print(f"Manifest: {os.path.basename(args.manifest)}")
    print(f"Phoneme Error Rate (PER): {error_rate:.4f} ({(error_rate * 100):.2f}% error)")
    print("-" * 40)

    # Save metrics to a file
    os.makedirs(os.path.dirname(args.output_metrics), exist_ok=True)
    with open(args.output_metrics, 'w', encoding='utf-8') as f:
        json.dump({"per": error_rate}, f, indent=4)

if __name__ == "__main__":
    main()
