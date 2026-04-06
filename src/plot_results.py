import json
import os
import matplotlib.pyplot as plt

def main():
    # Define the levels and where to find their scores
    levels = ['Clean', '40', '20', '10']
    metric_files = [
        'metrics/per_clean.json',
        'metrics/per_snr40.json',
        'metrics/per_snr20.json',
        'metrics/per_snr10.json'
    ]
    
    per_scores = []
    
    # Read the JSON files you just created
    for file_path in metric_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                # Convert the decimal (e.g., 0.043) to a percentage (4.3%)
                per_scores.append(data['per'] * 100)
        else:
            print(f"Warning: Could not find {file_path}")
            per_scores.append(0)

    # Create the graph
    plt.figure(figsize=(8, 5))
    plt.plot(levels, per_scores, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)
    
    # Add titles and labels
    plt.title('Speech Recognition Robustness to Noise', fontsize=14)
    plt.xlabel('Signal-to-Noise Ratio (SNR) in dB', fontsize=12)
    plt.ylabel('Phoneme Error Rate (PER %)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Annotate the exact numbers on the graph
    for i, score in enumerate(per_scores):
        plt.annotate(f"{score:.2f}%", (levels[i], per_scores[i]), 
                     textcoords="offset points", xytext=(0,10), ha='center')

    # Save the picture
    os.makedirs('figures', exist_ok=True)
    output_path = 'figures/per_degradation.png'
    plt.savefig(output_path, bbox_inches='tight')
    print(f"Success! Graph saved to {output_path}")

if __name__ == "__main__":
    main()
