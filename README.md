# Spelling Bee Solver
This program is intended to solve the NYT SpellingBee puzzle
(https://www.nytimes.com/puzzles/spelling-bee).

By running `python solve.py` in this directory the user is prompted to enter the centre letter of 
the puzzle and then the 6 other letters.
The program then checks from a predefined word list to find the all words that can be generated 
from these letters, each word must contain the centre letter but does not have to contain all 
outer letters.

Finding the pangram or pangrams of the puzzle requires finding words that contain all 7 letters. 

The output of this program is several lists printed to the console. First any perfect pangrams are 
found, these contain each letter only once. Then all other found pangrams are printed from 
shortest to longest. After this all remaing words are printed in order from shortest to longest.

## Switches
Additionally this program has two switches than can be added to increase the amount of words 
considered. Typically the puzzle does not allow proper nouns or some particuarly obscure words 
however if a solution is not found the word list can be changed with switches increase the number 
of possible solutions.

These two switches are `-b` and `-c`.

The `-b` tag changes the word list used from `./words.txt` to `./megaWords.txt`. This list 
contains several more obscure words.

The `-c` tag allows for words which are capitalised in the word list to also be included for 
possible solutions. This allows proper nouns to be included.

These switches can be entered in any of the following manner and are not case sensitive:\
`python solve.py -b -c`\
`python solve.py -c -b`\
`python solve.py -b`\
`python solve.py -c`

## Functionality
This program works by iterating through the given word list and counting the number of distinct 
letters in the word. If no letters outside of the 7 provided in the puzzle are present the word is 
a valid solution and is added to the relevant list. If the word is a valid solution and has 7 
distinct letters then it is a pangram and is added to the list of pangrams. Finally if the word is valid, has 7 distinct letters and is of length 7 then it is a perfect pangram and is added to that list.
