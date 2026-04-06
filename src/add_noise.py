import json
import os
import argparse
import numpy as np
import soundfile as sf
import yaml # lets the script read  params.yaml

def add_white_noise(audio, snr_db, seed):
    # This ensures the "random" noise is exactly the same every time
    np.random.seed(seed)
    sig_power = np.mean(audio**2)
    snr_linear = 10**(snr_db / 10)
    noise_power = sig_power / snr_linear
    noise = np.random.normal(0, np.sqrt(noise_power), len(audio))
    return audio + noise

def main():
    # Load settings from  params.yaml
    with open("params.yaml", 'r') as f:
        params = yaml.safe_load(f)
    
    seed = params['seed'] 

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", required=True)
    parser.add_argument("--snr", type=int, required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--output_manifest", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.input_manifest, 'r') as f:
        records = [json.loads(line) for line in f]

    for r in records:
        audio, sr = sf.read(r['wav_path'])
        # Pass the seed to the noise function
        noisy_audio = add_white_noise(audio, args.snr, seed)
        
        file_name = os.path.basename(r['wav_path']).replace(".wav", f"_snr{args.snr}.wav")
        output_path = os.path.join(args.output_dir, file_name)
        sf.write(output_path, noisy_audio, sr)
        
        r['wav_path'] = output_path
        r['snr_db'] = args.snr

    with open(args.output_manifest, 'w') as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
            
    print(f"Created reproducible noisy manifest (Seed: {seed}) at {args.output_manifest}")

if __name__ == "__main__":
    main()
