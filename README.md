# Spelling Bee Solver
This program solves the NYT SpellingBee puzzle (https://www.nytimes.com/puzzles/spelling-bee).

Run `python solve.py` in this directory and you are prompted for the centre letter of the puzzle and
then the 6 outer letters. The program searches a word list for every word that can be made from
those letters. Each word must be at least 4 letters long and contain the centre letter, but does not
have to use all of the outer letters, and letters may be reused.

The solutions are printed as three lists. First any perfect pangrams, which use all 7 letters
exactly once each. Then any other pangrams, which use all 7 letters, shortest first. Finally the
remaining words, shortest first, in columns.

## Word lists
| List | Words | Source |
| --- | --- | --- |
| `words.txt` | 152,041 | [Collins Scrabble Words 2021][csw21], the tournament list |
| `megaWords.txt` | 273,409 | [SCOWL/aspell][scowl], every English spelling variant |

The Collins list holds no proper nouns, so it is stored entirely in lowercase. The SCOWL list covers
US, GB (both `-ise` and `-ize`), Canadian and Australian spellings with no diacritics, and keeps its
capitalised words, which is what the `-c` switch reaches.

Both lists are built by `buildWordList.py`, which downloads the raw sources into `./sources`
(ignored by git) and filters them down. Rebuild them at any time with:

```
python buildWordList.py
```

Only words of 4 letters or more, made purely of ASCII letters, and using no more than 7 distinct
letters are kept, since nothing else can ever be a solution: an eighth distinct letter is one the
puzzle does not have. That filtering is what takes the lists down from 277,610 and 519,175 words.
To change what is kept, edit `allow()` in `buildWordList.py` and rebuild.

## Switches
The word list can be widened when a puzzle has no solution in the default list. The puzzle usually
rejects proper nouns and particularly obscure words, so these are left out unless asked for.

| Switch | Effect |
| --- | --- |
| `-b`, `--big` | Search `megaWords.txt`: about twice as many words, and far looser |
| `-c`, `--caps` | Also allow capitalised words, such as proper nouns. Needs `-b` |
| `-t`, `--type` | Type the solutions into another window instead of printing them |
| `--delay SECONDS` | Pause between typed words. Only useful with `-t` |

Switches can be given in any order and combined:\
`python solve.py -b -c`\
`python solve.py -c -b`\
`python solve.py -b`\
`python solve.py -c`

## Typing the answers
With `-t` the solutions are typed straight into whichever window has focus, one word per line,
rather than printed. After the letters are entered the program waits, so switch to the puzzle and
press `shift+enter` to start. This needs the `keyboard` package:

```
pip install keyboard
```

## Files
| File | Purpose |
| --- | --- |
| `solve.py` | Command line entry point: reads the puzzle, prints or types words |
| `spellingBee.py` | The solving itself: word matching and pangram detection |
| `displayWords.py` | Prints a list of words in aligned columns |
| `buildWordList.py` | Downloads the raw sources and filters them into the two lists |
| `words.txt` | Default word list |
| `megaWords.txt` | Larger word list used by `-b` |
| `testing/checkPangrams.py` | Checks every test puzzle for a pangram |
| `testing/testPuzzles.txt` | Past puzzles, 7 letters a line, centre letter first |

## Testing
A real Spelling Bee puzzle always has at least one pangram, so a puzzle with none is a word list
that is missing a word it should hold. `testing/checkPangrams.py` reads every puzzle in
`testing/testPuzzles.txt`, reports the pangrams found for each and which list they came from, and
exits 1 if any puzzle is missed.

```
python testing/checkPangrams.py
```

## Functionality
The solver reads the chosen word list one word at a time. A word is a solution if it is at least 4
letters long, contains the centre letter, and contains no letter outside the 7 the puzzle provides.
Solutions with 7 distinct letters are pangrams, and a pangram exactly 7 letters long is a perfect
pangram.

`words.txt` is published under licence with Collins, an imprint of HarperCollins Publishers Limited.

[csw21]: https://github.com/scrabblewords/scrabblewords
[scowl]: https://github.com/nlile/dictionary-word-list
