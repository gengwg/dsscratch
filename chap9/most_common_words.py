"""
count the most common words in input
"""
import sys
from collections import Counter

try:
    num_words = int(sys.argv[1])
except:
    print "usage: {} num_words".format(sys.argv[0])
    sys.exit(1)

counter = Counter(word.lower()
                  for line in sys.stdin             # lowercase words
                  for word in line.strip().split()   # split on spaces
                  if word)  # skip empty words

for word, count in counter.most_common(num_words):
    sys.stdout.write(str(count))
    sys.stdout.write("\t")
    sys.stdout.write(word)
    sys.stdout.write("\n")


