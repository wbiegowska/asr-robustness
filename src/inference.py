import json
import os
import argparse
import torch
import soundfile as sf
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--model_name", required=True)
    parser.add_argument("--output_manifest", required=True)
    args = parser.parse_args()

    print(f"Loading AI model: {args.model_name}...")
    processor = Wav2Vec2Processor.from_pretrained(args.model_name)
    model = Wav2Vec2ForCTC.from_pretrained(args.model_name)

    with open(args.manifest, 'r', encoding='utf-8') as f:
        records = [json.loads(line) for line in f]

    results = []
    print(f"Processing...")

    for r in records:
        speech, sr = sf.read(r['wav_path'])
        
        if speech.dtype != np.float32:
            speech = speech.astype(np.float32)
            
        input_values = processor(speech, return_tensors="pt", sampling_rate=16000).input_values
        
        with torch.no_grad():
            logits = model(input_values).logits
        
        predicted_ids = torch.argmax(logits, dim=-1)
        prediction = processor.batch_decode(predicted_ids)[0]
        
        r['pred_phon'] = prediction.lower()
        results.append(r)
        print(f"File: {os.path.basename(r['wav_path'])} | Guess: {prediction}")

    os.makedirs(os.path.dirname(args.output_manifest), exist_ok=True)
    with open(args.output_manifest, 'w', encoding='utf-8') as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            
    print(f"Success! Saved to {args.output_manifest}")

if __name__ == "__main__":
    main()
