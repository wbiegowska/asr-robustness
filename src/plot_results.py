import json
import os
import matplotlib.pyplot as plt

def main():
    languages = ['en', 'fr']
    levels = ['Clean', '40', '20', '10']
    
    plt.figure(figsize=(9, 6))
    all_language_scores = []
    
    for lang in languages:
        metric_files = [
            f'metrics/per_{lang}_clean.json',
            f'metrics/per_{lang}_snr40.json',
            f'metrics/per_{lang}_snr20.json',
            f'metrics/per_{lang}_snr10.json'
        ]
        
        per_scores = []
        for file_path in metric_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    per_scores.append(data['per'] * 100)
            else:
                per_scores.append(0)
                
        all_language_scores.append(per_scores)
        plt.plot(levels, per_scores, marker='o', linestyle='-', linewidth=2, label=lang.upper())

    # Plot the Mean curve
    if len(all_language_scores) == 2:
        mean_scores = [(en + fr) / 2 for en, fr in zip(all_language_scores[0], all_language_scores[1])]
        plt.plot(levels, mean_scores, marker='s', linestyle='--', color='black', linewidth=2, label='Mean')

    plt.title('Phoneme Error Rate vs Noise (Multi-Language)', fontsize=14)
    plt.xlabel('Signal-to-Noise Ratio (SNR) in dB', fontsize=12)
    plt.ylabel('Phoneme Error Rate (PER %)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    os.makedirs('figures', exist_ok=True)
    plt.savefig('figures/per_degradation_multi.png', bbox_inches='tight')
    print("Success! Multi-language graph saved to figures/per_degradation_multi.png")

if __name__ == "__main__":
    main()
