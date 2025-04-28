from ngram_prob import generate_ngram_probs
from decrypt import gen_shift_list
import math

#Text
text = "CREAS"
# text = "CZGGJOOCDNODNOVIOZSVHKGZ"

def calculate_normalized_probs(text):
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
            prob = probs.get(gram, 1e-10)
            total_prob += prob
        return total_prob

    all_normalized_probs = []

    for n in range(1, 7):
        unigram_probs = []
        for word in word_list:
            prob = word_prob(word, n)
            unigram_probs.append((word, prob))

        total = sum(prob for _, prob in unigram_probs)
        if total == 0:
            total = 1e-12
            
        normalized_probs = [(prob / total, word) for word, prob in unigram_probs]
        normalized_probs.sort(key=lambda x: x[0], reverse=True)
        all_normalized_probs.append((n, normalized_probs))

    return all_normalized_probs

if __name__ == "__main__":
        
    results = calculate_normalized_probs(text)
    
    for n, normalized_probs in results:
        print(f"n is {n}")
        print(normalized_probs)
    print("This word decodes as:")
    print(results[-1][1][0])  