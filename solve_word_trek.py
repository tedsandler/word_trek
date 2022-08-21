
import os
import re
import sys
import string
import itertools


def get_wordlist(fname, wordlen=4):
    wordlist = set([])
    with open(fname) as fin:
        for line in fin:
            word = line.strip()
            if len(word) == wordlen and word.isalpha():
                wordlist.add(word)
    return wordlist


def get_word_chain(start_word, current_word, parents):
    word_chain = [current_word]

    while current_word != start_word:
        current_word = parents[current_word]
        word_chain.append(current_word)

    return word_chain[::-1]


def edit_word(word, pos, new_char):
    return word[:pos] + new_char + word[(pos+1):]


def get_neighbors(current_word, wordlist):
    neighbors = set([])
    letters = list(string.ascii_lowercase)
    
    for pos in range(len(current_word)):
        for new_char in letters:
            new_word = edit_word(current_word, pos, new_char)
            if new_word in wordlist:
                neighbors.add(new_word)
    
    for perm in itertools.permutations(current_word):
        new_word = ''.join(perm)
        if new_word in wordlist:
            neighbors.add(new_word)

    return neighbors


def solve(start_word, end_word, wordlist):
    queue = [start_word]
    parents = {start_word : None}

    while queue:

        current_word = queue[0]
        queue = queue[1:]

        if current_word == end_word:
            return get_word_chain(start_word, current_word, parents)

        neighbors = get_neighbors(current_word, wordlist)
        for neighbor in neighbors:
            if neighbor not in parents:
                parents[neighbor] = current_word
                queue.append(neighbor)

    return None


def main():
    if len (sys.argv) != 3:
        print("usage: <START_WORD> <END_WORD>")
        sys.exit(1)

    start_word, end_word = sys.argv[1:3]
    wordlist = get_wordlist('unix-words.txt')
    word_chain = solve(start_word, end_word, wordlist)

    if word_chain:
        for i, word in enumerate(word_chain):
            print(f"step {i}:\t{word}")
    else:
        print(f"sorry, I could not find a path from {start_word} to {end_word}")

    sys.exit(0)


if __name__ == "__main__":
    main()
