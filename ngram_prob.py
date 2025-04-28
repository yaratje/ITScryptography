from nltk.corpus import brown
from nltk import ngrams
import string
from collections import Counter

#nltk.download("brown")
#nltk.download("webtext")

from nltk.corpus import brown, gutenberg, webtext, reuters

#justg do them allll

#get all them probabilities
def ngram_probs(n, text):
    ngram_counts = Counter(ngrams(text, n))
    total = sum(ngram_counts.values())
    ngram_probs = {''.join(k): (v / total) * 100 for k, v in ngram_counts.items()}
    return ngram_probs

def generate_ngram_probs():
    text = (
        brown.raw() +
        gutenberg.raw() +
        webtext.raw() +
        reuters.raw()
    )

    text = ''.join([c for c in text.upper() if c in string.ascii_uppercase])
    ngram_freqs = {}
    #only letters and upper case
    text = ''.join([c for c in text.upper() if c in string.ascii_uppercase])

    for n in range(1,6):
        ngram_freqs[n] = ngram_probs(n, text)

    #print(ngram_freqs[2])
    return ngram_freqs

