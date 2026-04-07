import os
import json
import io
import requests
import soundfile as sf
import pandas as pd

def main():
    # URL for the FLEURS French dataset
    url = "https://huggingface.co/datasets/google/fleurs/resolve/refs%2Fconvert%2Fparquet/fr_fr/train/0000.parquet"
    print("Downloading 5 French audio files (this might take a minute)...")
    
    # Download the parquet file directly
    r = requests.get(url)
    
    # Safety check: Make sure it didn't get a 404 Not Found error
    if r.status_code != 200:
        print(f"Download failed! Error code: {r.status_code}")
        return

    # Read only the first 5 rows to save time
    df = pd.read_parquet(io.BytesIO(r.content)).head(5)

    os.makedirs('data/raw/fr/wav', exist_ok=True)
    os.makedirs('data/manifests/fr', exist_ok=True)

    records = []
    for idx, row in df.iterrows():
        wav_path = f"data/raw/fr/wav/fr_{idx}.wav"
        
        # Read the raw audio bytes
        audio_bytes = row['audio']['bytes']
        signal, sr = sf.read(io.BytesIO(audio_bytes))
        
        # Save to your laptop at 16kHz
        sf.write(wav_path, signal, 16000)
        
        records.append({
            "utt_id": f"fr_{idx}",
            "lang": "fr",
            "wav_path": wav_path,
            "ref_text": row['raw_transcription'],
            "sr": 16000
        })

    # Save the manifest
    with open('data/manifests/fr/clean.jsonl', 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
            
    print("Success! French data is ready in data/manifests/fr/clean.jsonl")

if __name__ == "__main__":
    main()
