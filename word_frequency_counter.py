import re
from collections import Counter

# Part 8
# Mini Project: Word Frequency Counter
print("\nPart 8\nMini Project: Word Frequency Counter")
text = input("Paste your paragraph: ").lower()
words = re.findall(r"\b\w+\b", text)
count = Counter(words)

for word, freq in count.most_common(5):
    print(f"{word}: {freq}")
