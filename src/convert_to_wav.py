import os
import soundfile as sf
from pathlib import Path

# Path to your audio files
input_dir = Path("data/raw/en/wav")

print("Starting conversion from .flac to .wav...")

# Find all flac files
flac_files = list(input_dir.glob("*.flac"))

if not flac_files:
    print("No .flac files found. Did you move them to data/raw/en/wav/ yet?")
else:
    for flac_path in flac_files:
        # Load the flac file
        data, samplerate = sf.read(flac_path)
        
        # Define the new wav path (same name, different extension)
        wav_path = flac_path.with_suffix(".wav")
        
        # Save as wav
        sf.write(wav_path, data, samplerate)
        
        # Delete the old flac file to save space
        os.remove(flac_path)
        print(f"Converted: {flac_path.name} -> {wav_path.name}")

print("All files converted successfully!")
