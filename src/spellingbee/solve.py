"""Solve the NYT Spelling Bee puzzle (https://www.nytimes.com/puzzles/spelling-bee).

Run with no arguments to be prompted for the puzzle's letters and have the solutions printed. See
--help for the word list and typing switches.
"""

import argparse
import time

from displayWords import printInColumns
from spellingBee import BIG_WORD_FILE, PUZZLE_LETTERS, WORD_FILE, solve

COLUMNS = 4


def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-b", "--big", action="store_true",
                        help="use the larger, more obscure word list")
    parser.add_argument("-c", "--caps", action="store_true",
                        help="also allow capitalised words, such as proper nouns")
    parser.add_argument("-t", "--type", dest="typeOut", action="store_true",
                        help="type the solutions into the focused window instead of printing them")
    parser.add_argument("--delay", type=float, default=0.0, metavar="SECONDS",
                        help="pause between typed words (default: %(default)s)")
    return parser.parse_args()


def readPuzzle():
    """Prompt for the puzzle's letters, returning (centreLetter, outerLetters)."""
    centreLetter = "".join(c for c in input("Centre Letter : ").upper() if c.isalpha())
    outerLetters = tuple(c for c in input("Outer Letters : ").upper() if c.isalpha())

    if len(centreLetter) != 1:
        raise SystemExit("The centre letter must be a single letter.")
    if len(set(outerLetters)) != len(outerLetters):
        raise SystemExit("The outer letters must all be different.")
    if len(outerLetters) != PUZZLE_LETTERS - 1:
        raise SystemExit("Expected %d outer letters, got %d."
                         % (PUZZLE_LETTERS - 1, len(outerLetters)))
    if centreLetter in outerLetters:
        raise SystemExit("The centre letter cannot also be an outer letter.")
    return centreLetter, outerLetters


def printWords(perfect, pangrams, otherWords):
    if len(perfect) > 0:
        print("\nPerfect pangrams:")
        print(*perfect, sep=",\n")

    if len(pangrams) > 0:
        print("\nPangrams:")
        print(*pangrams, sep=",\n")

    if len(otherWords) > 0:
        print("\nAll words:")
        printInColumns(otherWords, COLUMNS)
    elif len(perfect) == 0 and len(pangrams) == 0:
        print("\nNo solutions found. Try again with -b and/or -c.")


def typeWords(words, delay):
    """Type each word into whichever window has focus, one per line."""
    try:
        import keyboard
    except ImportError:
        raise SystemExit("Typing needs the 'keyboard' package: pip install keyboard")

    print("\n%d words to type. Focus the puzzle window, then press shift+enter to begin."
          % len(words))
    keyboard.wait("shift+enter")
    for word in words:
        keyboard.write(word.lower())
        keyboard.press_and_release("enter")
        if delay > 0:
            time.sleep(delay)


def main():
    args = parseArgs()
    wordFile = BIG_WORD_FILE if args.big else WORD_FILE
    centreLetter, outerLetters = readPuzzle()
    perfect, pangrams, otherWords = solve(wordFile, centreLetter, outerLetters, args.caps)

    if args.typeOut:
        typeWords(perfect + pangrams + otherWords, args.delay)
    else:
        printWords(perfect, pangrams, otherWords)


if __name__ == "__main__":
    main()
