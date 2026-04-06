import json
import argparse
import os
from phonemizer import phonemize

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", required=True, help="Language code for espeak (e.g., en-us)")
    parser.add_argument("--manifest", required=True, help="Input manifest (clean.jsonl)")
    parser.add_argument("--output", required=True, help="Output manifest (clean_phon.jsonl)")
    args = parser.parse_args()

    # 1. Load the manifest you created in the last step
    if not os.path.exists(args.manifest):
        print(f"Error: Could not find {args.manifest}")
        return

    with open(args.manifest, 'r', encoding='utf-8') as f:
        records = [json.loads(line) for line in f]

    # 2. Extract the sentences
    texts = [r['ref_text'] for r in records]
    
    print(f"Converting text to phonemes for {args.lang}...")
    
    # 3. Use the phonemizer tool to get IPA symbols
    # We strip stress/accents to make it easier for the AI
    phonemes = phonemize(
        texts,
        language=args.lang,
        backend='espeak',
        strip=True,
        with_stress=False
    )

    # 4. Put the phonemes back into our record list
    for r, ph in zip(records, phonemes):
        r['ref_phon'] = ph.strip()

    # 5. Save the new, updated manifest
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    
    print(f"Success! Created: {args.output}")

if __name__ == "__main__":
    main()
