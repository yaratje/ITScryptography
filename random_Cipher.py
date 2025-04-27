import nltk
import string
import random
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import brown, gutenberg, webtext, reuters
from nltk.util import ngrams
from collections import Counter
from ngram_prob import generate_ngram_probs

ngram_freqs = generate_ngram_probs()

#scoring function 
def score_text(text):
    score = 0.0
    for n in range(1, 6):
        probs = ngram_freqs[n]
        for gram in ngrams(text, n):
            g = ''.join(gram)
            score += np.log(probs.get(g, 1e-8))
    return score

#generate key
alphabet = list(string.ascii_uppercase)

def random_key():
    shuffled = alphabet.copy()
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def invert_key(key):
    return {v: k for k, v in key.items()}

def encrypt(text, key):
    return ''.join(key.get(c, c) for c in text)

def decrypt(text, key):
    inv = invert_key(key)
    return ''.join(inv.get(c, c) for c in text)

#simulation parameters
NUM_KEYS = 1000
MAX_N = 40

#Generate keyspace
random.seed(42)
keyspace = [random_key() for _ in range(NUM_KEYS)]

# Choose a true key and sample plaintext
true_key = random.choice(keyspace)
plaintext = "WELL I REALLY HOPE THAT THIS IS GOING TO WORK BUT YOU NEVER KNOW WHEN PROGRAMMING SO LETS JUST HOPE FOR THE BEST"
ciphertext_full = encrypt(plaintext, true_key)

#equivocation H_K(N)
H_values = []

for N in range(1, MAX_N + 1):
    ctxt = ciphertext_full[:N]
    scores = np.array([score_text(decrypt(ctxt, k)) for k in keyspace])
    
    # Posterior probabilities
    exps = np.exp(scores - scores.max())  # softmax stability
    p = exps / exps.sum()
    
    # Shannon entropy
    H = -np.sum(p * np.log2(p + 1e-12))
    H_values.append(H)

#plot
plt.figure(figsize=(10, 6))
plt.plot(range(1, MAX_N + 1), H_values, marker='o')
plt.title("Simulated Equivocation $H_K(N)$ for Random Cipher")
plt.xlabel("Number of Intercepted Letters (N)")
plt.ylabel("Equivocation $H_K(N)$ [bits]")
plt.grid(True)
plt.tight_layout()
plt.savefig("plot.png")



#THEORECTIAL PART
H_K0 = np.log2(NUM_KEYS)  #entropy of keyspace
D = 1.3                   #redundancy per letter for English (Shannon’s estimate)
R = D / np.log2(26)       # redundancy rate
N_0 = H_K0 / D            #unicity distance
lambda_decay = D / H_K0  #decay rate
A = H_K0 - D * N_0

def H_K_theoretical(N):
    if N < N_0:
        return H_K0 - D * N
    else:
        return A * np.exp(-lambda_decay * (N - N_0))


def H_M_theoretical(N):
    if N * R < H_K0:
        return R * N  #R0N << H(K)
    else:
        return H_K_theoretical(N)  #R0N >> H(K)


# Compute theoretical values over the same range
N_values = np.arange(1, MAX_N + 1)
H_K_theory = [H_K_theoretical(N) for N in N_values]
H_M_theory = [H_M_theoretical(N) for N in N_values]

# --- Plot everything together ---
plt.figure(figsize=(10, 6))
plt.plot(N_values, H_values, 'bo-', label='Simulated $H_K(N)$')
plt.plot(N_values, H_K_theory, 'r--', label='Theoretical $H_K(N)$')
plt.plot(N_values, H_M_theory, 'g--', label='Theoretical $H_M(N)$')
plt.axvline(x=N_0, color='gray', linestyle=':', label=f'Unicity Distance ≈ {N_0:.1f}')

plt.title("Simulated vs Theoretical Equivocation")
plt.xlabel("Number of Intercepted Letters $N$")
plt.ylabel("Equivocation [bits]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/plot_with_theory.png")