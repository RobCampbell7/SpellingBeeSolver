
def insert(word, wordLst):
    index = len(wordLst)
    for i in range(len(wordLst)):
        if len(word) < len(wordLst[i]):
            index = i - 1
            break
    return wordLst[:index] + [word] + wordLst[index:]

lst = []
print(insert("abcdef", lst))
