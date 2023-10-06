from config import *
from dataset import trajactories
from util import preprocess, write_trajactories


def main():
    write_trajactories(trajactories)

    filename = "sentences.txt"
    with open(filename, "w") as file:
        for t in trajactories:
            cord_2_word = preprocess(t)
            word_list = [value for value in cord_2_word.values()]
            sentence = " ".join(word_list)
            file.write(sentence)
            file.write("\n")

    print("\n========================================")
    print("|     Test sentences are generated     |")
    print("========================================\n")


if __name__ == "__main__":
    main()
