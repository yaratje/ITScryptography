from ngram_prob import generate_ngram_probs
from decrypt import gen_shift_list
import math

#Text
text = "CREAS"
# text = "CZGGJOOCDNODNOVIOZSVHKGZ"

#unigram up to 5-gram
ngram_prob = generate_ngram_probs()

#generates the word list but like 1 is the bottom one from the list in the paper
word_list = gen_shift_list(text)


#log probability ofword using the n-gram probs
def word_prob(word, n):
    probs = ngram_prob.get(n, {})
    total_prob = 0.0 

    for i in range(len(word) - n + 1):
        gram = word[i:i+n]
        prob = probs.get(gram, 1e-10)  #prob is very small
        total_prob += prob
    
    return total_prob

for n in range (1,6):
    unigram_probs = []
    for word in word_list:
        prob = word_prob(word,n)
        unigram_probs.append((word,prob))
    
    total = sum(prob for _, prob in unigram_probs)
    normalized_probs = [(prob / total, word) for word, prob in unigram_probs]
    normalized_probs.sort(key=lambda x: x[0], reverse=True)
    print(f"n is {n}")
    print(normalized_probs)

print("This word decodes as:")
print(normalized_probs[0])
