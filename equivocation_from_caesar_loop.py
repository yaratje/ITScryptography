import numpy as np
import matplotlib.pyplot as plt
import random
import nltk
from nltk.corpus import brown
import string
from equivocation_from_caesar import calculate_equivocation

nltk.download('brown')

num_trials = 10
message_length = 5


def generate_random_message(length=5):
    word_list = brown.words()
    message = ''
    while len(message) < length:
        word = random.choice(word_list).upper()
        # Only add if all characters are letters (A-Z)
        if all(c in string.ascii_uppercase for c in word):
            message += word
    return message[:length]


if __name__ == "__main__":
    all_H_values = []

    for i in range(num_trials):
        print(i)
        message = generate_random_message(message_length)
        
        # message = "CREAS"
        print(message)
        H_values = calculate_equivocation(message)
        all_H_values.append(H_values)

    all_H_values = np.array(all_H_values)
    mean_H_values = np.mean(all_H_values, axis=0)

    plt.plot(range(1, message_length + 1), mean_H_values, marker='o')
    plt.title("Average Key Equivocation $H_E(K)$ vs. Number of Observed Letters $N$")
    plt.xlabel("Number of Observed Letters (N)")
    plt.ylabel("Mean Equivocation [bits]")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"plots/plot_equivocation_from_caesar_avg_n{num_trials}_len{message_length}.png")