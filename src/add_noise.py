import json
import os
import argparse
import numpy as np
import soundfile as sf

def add_white_noise(audio, snr_db):
    # Calculate the power of the signal
    sig_power = np.mean(audio**2)
    # Convert SNR from dB to linear scale
    snr_linear = 10**(snr_db / 10)
    # Calculate required noise power
    noise_power = sig_power / snr_linear
    # Generate white noise
    noise = np.random.normal(0, np.sqrt(noise_power), len(audio))
    return audio + noise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", required=True)
    parser.add_argument("--snr", type=int, required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--output_manifest", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.output_manifest), exist_ok=True)

    with open(args.input_manifest, 'r') as f:
        records = [json.loads(line) for line in f]

    for r in records:
        audio, sr = sf.read(r['wav_path'])
        # Add the noise
        noisy_audio = add_white_noise(audio, args.snr)
        
        # Save the new noisy file
        file_name = os.path.basename(r['wav_path']).replace(".wav", f"_snr{args.snr}.wav")
        output_path = os.path.join(args.output_dir, file_name)
        sf.write(output_path, noisy_audio, sr)
        
        # Update the manifest record to point to the noisy file
        r['wav_path'] = output_path
        r['snr_db'] = args.snr

    with open(args.output_manifest, 'w') as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
            
    print(f"Created noisy manifest at {args.output_manifest} for SNR {args.snr}")

if __name__ == "__main__":
    main()
