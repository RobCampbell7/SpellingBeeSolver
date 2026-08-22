"""Core word finding for the NYT Spelling Bee puzzle.

A word solves the puzzle if it is at least four letters long, contains the centre letter, and uses
no letters beyond the seven the puzzle provides. Letters may be reused as often as you like.
"""

import os

MIN_LENGTH = 4
PUZZLE_LETTERS = 7

CWD = os.path.dirname(os.path.abspath(__file__))
WORD_FILE = os.path.join(CWD, "words.txt")
BIG_WORD_FILE = os.path.join(CWD, "megaWords.txt")


def possible(word, centreLetter, outerLetters):
    """Return True if word is a valid solution for the given letters."""
    if len(word) < MIN_LENGTH or centreLetter not in word:
        return False
    for char in word:
        if char != centreLetter and char not in outerLetters:
            return False
    return True


def isPangram(word):
    """Return True if word uses all seven of the puzzle's letters."""
    return len(set(word)) == PUZZLE_LETTERS


def isPerfectPangram(word):
    """Return True if word uses all seven letters exactly once each."""
    return len(word) == PUZZLE_LETTERS and isPangram(word)


def findWords(wordFile, centreLetter, outerLetters, includeCaps=False):
    """Yield every solution in wordFile, uppercased, in word list order.

    Words that are capitalised in the word list are proper nouns or abbreviations, which the puzzle
    does not accept, so they are skipped unless includeCaps is set.
    """
    with open(wordFile, "r") as dictFile:
        for line in dictFile:
            word = line.strip()
            if not word.isalpha():
                continue
            if not includeCaps and not word.islower():
                continue
            word = word.upper()
            if possible(word, centreLetter, outerLetters):
                yield word


def solve(wordFile, centreLetter, outerLetters, includeCaps=False):
    """Return (perfectPangrams, pangrams, otherWords), each sorted by length."""
    perfect = []
    pangrams = []
    otherWords = []
    for word in findWords(wordFile, centreLetter, outerLetters, includeCaps):
        if isPerfectPangram(word):
            perfect.append(word)
        elif isPangram(word):
            pangrams.append(word)
        else:
            otherWords.append(word)
    perfect.sort()
    pangrams.sort(key=len)
    otherWords.sort(key=len)
    return perfect, pangrams, otherWords
