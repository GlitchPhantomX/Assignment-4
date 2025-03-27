import random
import re
from collections import defaultdict

class MarkovChain:
    def __init__(self, text, n_gram=2):
        self.n_gram = n_gram  
        self.words = self.preprocess_text(text)
        self.index = defaultdict(list)
        self.build_index()

    def preprocess_text(self, text):
        """Cleans and tokenizes the input text."""
        text = text.lower()  
        text = re.sub(r"[^\w\s]", "", text) 
        return text.split()

    def build_index(self):
        """Creates the Markov chain index using n-grams."""
        for i in range(len(self.words) - self.n_gram):
            key = tuple(self.words[i:i + self.n_gram])
            next_word = self.words[i + self.n_gram]
            self.index[key].append(next_word)

    def generate_text(self, length=50):
        """Generates text using the Markov chain."""
        if not self.index:
            return "⚠️ Not enough data to generate text."

        current_tuple = random.choice(list(self.index.keys()))
        output = list(current_tuple)

        for _ in range(length - self.n_gram):
            next_words = self.index.get(current_tuple, [])
            if not next_words:
                break
            next_word = random.choice(next_words)
            output.append(next_word)
            current_tuple = tuple(output[-self.n_gram:])

        return " ".join(output).capitalize() + "."

if __name__ == "__main__":
    default_text = ("The quick brown fox jumps over the lazy dog. "
                    "The fox is clever and fast, while the dog is sleepy.")

    input_text = input("Enter text to train the Markov Chain (or press Enter to use default text): ").strip()
    if not input_text:
        print("ℹ Using default text corpus.")
        input_text = default_text

    markov_chain = MarkovChain(input_text, n_gram=2)
    generated_text = markov_chain.generate_text(100)
    
    print("\n🔹 Generated Text:\n" + generated_text)
