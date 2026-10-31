"""Check that every test puzzle has at least one pangram in the word lists.

Reads testPuzzles.txt, where each line is one puzzle written as its 7 letters with the centre letter
first, and reports the pangrams found for each. Puzzles that no list can solve are the ones worth
looking at: a real Spelling Bee puzzle always has at least one pangram, so a miss means the word
list is short of a word it should hold.

Needs the package installed. Run it with `python testing/checkPangrams.py`; the exit status is 1
if any puzzle is missed.
"""

import os

from spellingbee.spellingBee import BIG_WORD_FILE, PUZZLE_LETTERS, WORD_FILE, isPangram

PUZZLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testPuzzles.txt")
SHOWN_PER_PUZZLE = 3


def readPuzzles(path):
    """Return a list of (centreLetter, outerLetters) pairs, one per puzzle in the file."""
    puzzles = []
    with open(path, "r") as puzzleFile:
        for number, line in enumerate(puzzleFile, 1):
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            letters = [char for char in line.upper() if char.isalpha()]
            if len(letters) != PUZZLE_LETTERS or len(set(letters)) != PUZZLE_LETTERS:
                raise SystemExit("Line %d is not %d distinct letters: %s"
                                 % (number, PUZZLE_LETTERS, line))
            puzzles.append((letters[0], tuple(letters[1:])))
    return puzzles


def findPangrams(wordFile, puzzles, includeCaps=False):
    """Return a list of the pangrams found for each puzzle, in the same order as puzzles.

    A pangram uses every one of the puzzle's letters and no others, so its set of distinct letters
    is exactly the puzzle's set. That makes one pass over the word list enough to answer for every
    puzzle at once, however many there are.
    """
    found = [[] for puzzle in puzzles]
    byLetters = {}
    for index, (centreLetter, outerLetters) in enumerate(puzzles):
        # keyed on the full letter set, so puzzles with the same 7 letters but a different centre share an entry
        byLetters.setdefault(frozenset((centreLetter,) + outerLetters), []).append(index)

    with open(wordFile, "r") as dictFile:
        for line in dictFile:
            word = line.strip()
            if not word.isalpha():
                continue
            if not includeCaps and not word.islower():
                continue
            word = word.upper()
            if not isPangram(word):
                continue
            for index in byLetters.get(frozenset(word), ()):
                found[index].append(word)
    return found


def describe(pangrams):
    """Return a readable summary of the pangrams found for one puzzle."""
    shown = ", ".join(sorted(pangrams, key=len)[:SHOWN_PER_PUZZLE])
    if len(pangrams) > SHOWN_PER_PUZZLE:
        shown += ", +%d more" % (len(pangrams) - SHOWN_PER_PUZZLE)
    return shown


def main():
    puzzles = readPuzzles(PUZZLE_FILE)
    default = findPangrams(WORD_FILE, puzzles)
    # big list with caps allowed is the most generous check, only reported when words.txt has nothing
    big = findPangrams(BIG_WORD_FILE, puzzles, includeCaps=True)

    missed = 0
    inDefault = 0
    for index, (centreLetter, outerLetters) in enumerate(puzzles):
        letters = "%s %s" % (centreLetter, "".join(outerLetters))
        if len(default[index]) > 0:
            inDefault += 1
            print("%-9s %-14s %s" % (letters, "words.txt", describe(default[index])))
        elif len(big[index]) > 0:
            print("%-9s %-14s %s" % (letters, "megaWords.txt", describe(big[index])))
        else:
            missed += 1
            print("%-9s %-14s no pangram found" % (letters, "MISSED"))

    print("\n%d puzzles: %d solved by words.txt, %d more by megaWords.txt, %d missed"
          % (len(puzzles), inDefault, len(puzzles) - inDefault - missed, missed))
    if missed > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
