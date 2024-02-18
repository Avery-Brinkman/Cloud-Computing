import os
import socket

INPUT = "/home/data"
OUTPUT = "/home/output"


# List all the text files in /home/data (A)
def listTextFiles() -> str:
    out = "Text files in /home/data:\n"
    # Get the files
    files = os.listdir(INPUT)
    # Add the files to the output
    for f in files:
        # Only add .txt files
        if f.endswith(".txt"):
            out += f"  {f}\n"
    return out


# Open the file and parse the words (B)
def parseFile(file: str) -> dict:
    wordCounts = {"__total__": 0}
    # Open file in utf-8
    with open(file, "r", encoding="utf-8") as f:
        # Read and lowercase the file
        words = f.read().lower()
        # Replace dashes with spaces and split
        words = words.replace("—", " ").split()
        for word in words:
            # Strip punctuation
            word = word.strip(".,!?;:‘’")
            # Add to the dictionary
            wordCounts[word] = wordCounts.get(word, 0) + 1
            # Increment total
            wordCounts["__total__"] = wordCounts.get("__total__", 0) + 1
    # Return the dictionary
    return wordCounts


# Open IF.txt and Limerick-1.txt and get the word counts in each file (C & D)
def getWordCounts() -> str:
    out = ""
    # Parse the files
    ifFile = parseFile(f"{INPUT}/IF.txt")
    limerick = parseFile(f"{INPUT}/Limerick-1.txt")

    # Display info
    out += f"IF.txt word count        : {ifFile['__total__']}\n"
    out += f"Limerick-1.txt word count: {limerick['__total__']}\n"
    out += "\n"
    out += f"Total word count: {ifFile['__total__'] + limerick['__total__']}\n"
    out += "\n"

    # Don't need total anymore
    ifFile.pop("__total__")

    # Sort
    sortedIF = sorted(ifFile.items(), key=lambda x: x[1], reverse=True)
    out += "IF.txt maximum word counts:\n"
    # Get the top 3
    for i in range(3):
        out += f"  {sortedIF[i][0]}: {sortedIF[i][1]}\n"

    return out


# (E)
def getIP() -> str:
    return f"IP Address: {socket.gethostbyname(socket.gethostname())}\n"


def main():
    output = listTextFiles() + "\n" + getWordCounts() + "\n" + getIP()

    # (F)
    with open(f"{OUTPUT}/result.txt", "w") as f:
        f.write(output)

    # (G)
    print(output)


if __name__ == "__main__":
    main()
