from config import *
from gen_traj import normal_traj, abnormal_traj
from util import preprocess, write_trajactories


def main():
    write_trajactories(normal_traj, "../test_data/no/normal_traj.txt")
    write_trajactories(abnormal_traj, "../test_data/ab/abnormal_traj.txt")

    filename = "../test_data/no/normal_sen.txt"
    with open(filename, "w") as file:
        for t in normal_traj:
            cord_2_word = preprocess(t)
            word_list = [value for value in cord_2_word.values()]
            sentence = " ".join(word_list)
            file.write(sentence)
            file.write("\n")

    print("\n========================================")
    print("|     Normal sentences are generated    |")
    print("========================================\n")

    filename = "../test_data/ab/abnormal_sen.txt"
    with open(filename, "w") as file:
        for t in abnormal_traj:
            cord_2_word = preprocess(t)
            word_list = [value for value in cord_2_word.values()]
            sentence = " ".join(word_list)
            file.write(sentence)
            file.write("\n")

    print("\n========================================")
    print("|   Abnormal sentences are generated    |")
    print("========================================\n")


if __name__ == "__main__":
    main()
