import string
import random
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import brown
from nltk.util import ngrams
from ngram_prob import generate_ngram_probs


# simulation parameters
NUM_KEYS = 100000
MAX_N = 40

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

def score_text(text, ngram_freqs):
    score = 0.0
    for n in range(1, 6):
        probs = ngram_freqs[n]
        for gram in ngrams(text, n):
            g = ''.join(gram)
            score += np.log(probs.get(g, 1e-8))
    return score

sentences = brown.sents()
plaintext = ' '.join([' '.join(random.choice(sentences)) for _ in range(5)])  # 5 random sentences
plaintext = plaintext.upper()
plaintext = ''.join(c for c in plaintext if c in string.ascii_uppercase + ' ')

print(f"Plaintext sample:\n{plaintext[:500]}\n")

# cipher true
true_key = random_key()
ciphertext_full = encrypt(plaintext, true_key)

ngram_freqs = generate_ngram_probs()

random.seed(42)
keyspace = [random_key() for _ in range(NUM_KEYS)]

# Equivocaiton
H_values = []
H_message_values = []
D = 2.3   
H_K0 = np.log2(NUM_KEYS)
N_0 = H_K0 / D

for N in range(1, MAX_N + 1):
    ctxt = ciphertext_full[:N]
    scores = np.array([score_text(decrypt(ctxt, k), ngram_freqs) for k in keyspace])

    exps = np.exp(scores - scores.max())
    p = exps / exps.sum()

    H = -np.sum(p * np.log2(p + 1e-12))
    H_values.append(H)

    if N < N_0:
        H_message = D * N
    else:
        H_message = H
    H_message_values.append(H_message)


# plot
N_range = range(1, MAX_N + 1)
plt.plot(N_range, H_values, marker='o', label="Simulated Key Equivocation $H_K(N)$")

plt.title("Simulated Key Equivocation $H_K(N)$ for Simple Substitution Cipher")
plt.xlabel("Number of Intercepted Letters (N)")
plt.ylabel("Equivocation [bits]")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(f"plots/simple_substitution_equivocation_D{D}_keys{NUM_KEYS}.png")
plt.show()