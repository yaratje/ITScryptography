# ITScryptography
This repository contains code for reproducing and analyzing cryptographic properties, specifically equivocation and key uncertainty—for the Caesar Cipher and Simple Substitution Cipher as described and discussed by Shannon in "Communication Theory of Secrecy Systems" (1949). 

## Project Files

- **`caesar_cipher.py`**  
  Calculates and normalizes n-gram probabilities for possible Caesar cipher decryptions.

- **`ngram_prob.py`**  
  Generates n-gram probabilities from English text corpora.

- **`decrypt.py`**  
  Provides utility functions to generate all possible Caesar cipher shifts for a given ciphertext.

- **`equivocation_from_caesar.py`**  
  Calculates the equivocation (remaining uncertainty about the key) as more letters of the caesar ciphertext are revealed.

- **`equivocation_from_caesar_loop.py`**  
  Runs multiple trials using random English word-based messages and calculates the average equivocation as more ciphertext is observed.

- **`equivocation_simple_substitution.py`**  
  Simulates equivocation for a Simple Substitution Cipher by generating random keys and scoring decrypted text using n-gram statistics.

## Run the experiments:
    All the experiments can be run via the command line. Parameters are located as variables in the experiment files.

    For example, to run the repeated Caesar cipher equivocation simulation:

    ```bash
    python equivocation_from_caesar_loop.py
    ```

    This script will generate and save plots inside the `plots/` folder.