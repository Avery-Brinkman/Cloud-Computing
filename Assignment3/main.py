import os
import socket


# List all the text files in /home/data (A)
def listTextFiles() -> str:
    out = ""
    files = os.listdir("/home/data")
    out += "Text files in /home/data:\n"
    for f in files:
        if f.endswith(".txt"):
            out += f + "\n"
    return out


# Open the file and parse the words (B)
def parseFile(file: str) -> dict:
    with open(file, "r") as f:
        words = f.read().lower().split()
        wordCounts = {word: words.count(word) for word in words}
        wordCounts["__total__"] = len(words)
        return wordCounts

    return {"__total__": 0}


# Open IF.txt and Limerick-1.txt and get the word counts in each file (C & D)
def getWordCounts() -> str:
    out = ""
    ifFile = parseFile("/home/data/IF.txt")
    limerick = parseFile("/home/data/Limerick-1.txt")

    # Display info
    out += f"IF.txt word count: {ifFile['__total__']}\n"
    out += f"Limerick-1.txt word count: {limerick['__total__']}\n"
    out += f"Total word count: {ifFile['__total__'] + limerick['__total__']}\n"

    # Don't need total anymore
    ifFile.pop("__total__")

    # Sort
    sortedIF = sorted(ifFile.items(), key=lambda x: x[1], reverse=True)
    out += "IF.txt maximum word counts:\n"
    for i in range(3):
        out += f"{sortedIF[i][0]}: {sortedIF[i][1]}\n"

    return out


# (E)
def getIP() -> str:
    return f"IP Address: {socket.gethostbyname(socket.gethostname())}\n"


def main():
    output = listTextFiles() + "\n" + getWordCounts() + "\n" + getIP()

    # (F)
    with open("/home/output/result.txt", "w") as f:
        f.write(output)

    # (G)
    print(output)


if __name__ == "__main__":
    main()
