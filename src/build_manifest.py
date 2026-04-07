import os
import json
import hashlib
import soundfile as sf
import argparse

def get_md5(file_path):
    """Creates a unique fingerprint for the audio file to ensure it hasn't changed."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        # Read in small 4KB chunks to save memory [cite: 151]
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    # These are the instructions the script needs to run
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", required=True, help="Language code (e.g., en)")
    parser.add_argument("--raw_dir", required=True, help="Where the .wav files are")
    parser.add_argument("--transcript", required=True, help="The .tsv file with text")
    parser.add_argument("--output", required=True, help="Where to save the JSONL map")
    args = parser.parse_args()

    records = []
    
    # Check if the transcript file actually exists
    if not os.path.exists(args.transcript):
        print(f"Error: Transcript {args.transcript} not found.")
        return

    # Read the transcript file (format: filename [TAB] text) [cite: 150]
    with open(args.transcript, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            
            file_stem, text = parts[0], parts[1]
            # Find the matching audio file [cite: 150]
            wav_path = os.path.join(args.raw_dir, f"{file_stem}.wav")
            
            if os.path.exists(wav_path):
                # Get metadata (length and sample rate) without loading the whole file [cite: 151]
                info = sf.info(wav_path)
                
                # Build the 'record' for this specific sentence [cite: 501, 512]
                records.append({
                    "utt_id": f"{args.lang}_{file_stem}",
                    "lang": args.lang,
                    "wav_path": wav_path,
                    "ref_text": text,
                    "ref_phon": None,     # This is empty for now [cite: 162]
                    "sr": info.samplerate,
                    "duration_s": round(info.duration, 2),
                    "snr_db": None,       # This is empty for now [cite: 162, 417]
                    "audio_md5": get_md5(wav_path)
                })

    # Create the output folder if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Atomic write: Write to a temporary file first, then rename it.
    # This prevents crashing if the computer turns off mid-save[cite: 205, 551].
    tmp_path = args.output + ".tmp"
    with open(tmp_path, 'w', encoding='utf-8') as f:
        for r in records:
            # Each line is one JSON object [cite: 499, 546]
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    
    # Replace the old file with the new one [cite: 205, 213]
    os.replace(tmp_path, args.output)
    print(f"Success! Created map: {args.output} with {len(records)} entries.")

if __name__ == "__main__":
    main()
