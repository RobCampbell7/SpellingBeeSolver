import sys

def possible(word):
    if CENTRELETTER in word:
        for char in word:
            if char != CENTRELETTER and char not in OUTERLETTERS:
                return False
        return True
    else:
        return False

def uniqueLetters(word):
    foundLetters = []
    for char in word:
        if char not in foundLetters:
            foundLetters.append(char)
    return foundLetters

def usedLetters(word):
    foundLetters = []
    for char in word:
        if char not in foundLetters:
            foundLetters.append(char)
    return len(foundLetters)

CENTRELETTER = "F"
OUTERLETTERS = ("L", "T", "E", "M", "O", "I")

includeCaps = False
if len(sys.argv) == 1:
    wordFile = "words.txt"
elif len(sys.argv) == 2:
    if sys.argv[1] == "-B":
        wordFile = "megaWords.txt"
    elif sys.argv[1] == "-C":
        includeCaps = True
    else:
        raise Exception("Invalid argument: '" + sys.argv[1] + "'")
elif len(sys.argv) == 3:
    args = sorted([a.upper() for a in sys.argv[1:]])
    if args[0] == "-B":
        wordFile = "megaWords.txt"
    else:
        raise Exception("Invalid argument: '" + sys.argv[1] + "'")
    if args[1] == "-C":
        wordFile = "megaWords.txt"
    else:
        raise Exception("Invalid argument: '" + sys.argv[2] + "'")
else:
    raise Exception("Too many arguments/s: '" + " ".join(sys.argv[1:]) + "'")

CENTRELETTER = input("Centre Letter : ").upper()
outerInput = input("Outer Letters : ").upper().replace(" ", "").replace(",", "")
OUTERLETTERS = tuple([*outerInput])

    
perfect = []
pangrams = []
possibleWords = []
with open(wordFile, "r") as dictFile:
    for word in dictFile.readlines():
        word = word.replace("\n", "").replace(" ", "").upper()
        if possible(word) == True and (includeCaps or word != word.lower()):
            if usedLetters(word) == 7:
                if len(word) == 7:
                    perfect.append(word)
                pangrams.append(word)
            else:
                possibleWords.append(word)
pangrams.sort(key = len)
possibleWords.sort(key = len)

if len(perfect) > 0:
    print("\nPerfect pangrams:")
    print(*perfect, sep = ",\n")

print("\nPangrams:")
print(*pangrams, sep = ",\n")

print("\nAll words:")
print(*possibleWords, sep = ",\n")