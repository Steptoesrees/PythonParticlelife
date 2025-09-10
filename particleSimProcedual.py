import random

class SimpleLLM:
    def __init__(self, corpus):
        """
        Initializes the SimpleLLM with a corpus of text.

        Args:
            corpus: A string containing the text the model will learn from.
        """
        self.corpus = corpus.lower()  # Convert to lowercase for consistency
        self.word_counts = {}  # Dictionary to store word counts
        self.context_counts = {} # Dictionary to store context-word counts

        self._train()  # Train the model upon initialization

    def _train(self):
        """
        Trains the model by counting word occurrences and context-word occurrences.
        """
        words = self.corpus.split()
        for i in range(len(words) - 1):
            context = words[i]
            next_word = words[i+1]

            # Update word counts
            if context not in self.word_counts:
                self.word_counts[context] = 0
            self.word_counts[context] += 1

            # Update context-word counts
            if context not in self.context_counts:
                self.context_counts[context] = {}
            if next_word not in self.context_counts[context]:
                self.context_counts[context][next_word] = 0
            self.context_counts[context][next_word] += 1


    def generate_text(self, prompt, length=50):
        """
        Generates text based on the given prompt.

        Args:
            prompt: The starting word or phrase.
            length: The number of words to generate.

        Returns:
            A string containing the generated text.
        """
        output = prompt
        current_word = prompt.lower()

        for _ in range(length):
            if current_word in self.context_counts:
                possible_next_words = self.context_counts[current_word]
                # Simple probability distribution:
                # Create a list of words, repeating each word according to its count
                weighted_words = []
                for word, count in possible_next_words.items():
                    weighted_words.extend([word] * count)

                if weighted_words:  # Check if there are any possible next words
                    next_word = random.choice(weighted_words)
                    output += " " + next_word
                    current_word = next_word
                else:
                    # No next word found for this context, stop generating
                    break
            else:
                # Context not found, stop generating
                break
        return output

corpus = """
The quick brown fox jumps over the lazy dog.
The lazy dog sleeps soundly.
The quick fox is very cunning.
"""

llm = SimpleLLM(corpus)
prompt = "over"
generated_text = llm.generate_text(prompt, length=20)
print(generated_text)