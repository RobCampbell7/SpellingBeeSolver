"""Print a list of words across several columns."""

from random import sample


def printInColumns(words, noOfColumns):
    """Print words in noOfColumns columns, filling each column top to bottom."""
    columns = [words[i::noOfColumns] for i in range(noOfColumns)]
    columns = [col for col in columns if len(col) > 0]
    if len(columns) == 0:
        return

    widths = [len(max(col, key=len)) for col in columns]
    for row in range(len(columns[0])):
        cells = []
        for col, width in zip(columns, widths):
            if row < len(col):
                cells.append(" {0:>{1}} ".format(col[row], width))
        print("".join(cells))


if __name__ == "__main__":
    with open("words.txt", "r") as dictFile:
        words = [line.strip().upper() for line in dictFile]

    printInColumns(sorted(sample(words, 801), key=len), 4)
