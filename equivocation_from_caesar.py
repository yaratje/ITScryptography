from caesar_cipher import calculate_normalized_probs
import numpy as np
import matplotlib.pyplot as plt


message = "CREAS"  

def calculate_equivocation(text):
    all_normalized_probs = calculate_normalized_probs(text)
    H_values = []

    for n_val, normalized_probs in all_normalized_probs:
        probs = np.array([p for p, _ in normalized_probs])
        
        # calculate equivocaton 
        H = -np.sum(probs * np.log2(probs + 1e-12))
        print(n_val, H)
        H_values.append(H)

    return H_values

if __name__ == "__main__":
    H_values = calculate_equivocation(message)

    plt.plot(range(1, len(message)+1), H_values, marker='o')
    plt.title("Key Equivocation $H_E(K)$ vs. Number of Observed Letters $N$")
    plt.xlabel("Number of Observed Letters (N)")
    plt.ylabel("Equivocation [bits]")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/plot_equivocation_from_caesar.png")
    