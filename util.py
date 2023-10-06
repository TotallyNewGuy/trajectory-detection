import math
from typing import List
from config import *


def preprocess(coordinates: List[List[int]]):
    word_length = int(math.ceil(math.log(default_block_num, 26)))
    word_2_cord = {}  # "ABC": cord's index -> one to many
    cord_2_word = {}  # cord's index: "ABC" -> many to one
    index_2_word = {}  # 0: "ABC" -> one to one
    word_2_index = {}  # "ABC": 0 -> one to one
    generate_words(
        word_2_cord, index_2_word, word_2_index, word_length, default_block_num, []
    )

    north, south, west, east = get_boundary(coordinates)
    ver_blk_len = (north - south) / default_block_len
    hor_blk_len = (east - west) / default_block_len

    get_mapping(
        word_2_cord,
        index_2_word,
        word_2_index,
        cord_2_word,
        ver_blk_len,
        hor_blk_len,
        west,
        north,
        default_block_len,
        coordinates,
    )
    for key in list(word_2_cord.keys()):
        cords = word_2_cord[key]
        size = len(cords)
        # ================= constructing =================
        limit = default_block_num * resize_factor
        if size > 4:
            resize(coordinates, cords, cord_2_word, word_2_cord, 2)

    for key in list(word_2_cord.keys()):
        if not word_2_cord.get(key):
            del word_2_cord[key]

    return cord_2_word


def generate_words(
    word_2_cord: dict,
    index_2_word: List[str],
    word_2_index: dict,
    word_length: int,
    block_num: int,
    path: List[int],
) -> None:
    if len(word_2_cord) == block_num:
        return
    if word_length == 0:
        word = "".join(path)
        index_2_word[len(word_2_cord)] = word
        word_2_index[word] = len(word_2_cord)
        word_2_cord[word] = []
        return

    for i in range(26):
        path.append(chr(ord("A") + i))
        generate_words(
            word_2_cord, index_2_word, word_2_index, word_length - 1, block_num, path
        )
        path.pop()


def get_boundary(coordinates: List[List[int]]) -> (int, int, int, int):
    north = float("-inf")
    south = float("inf")
    west = float("inf")
    east = float("-inf")
    for cord in coordinates:
        x = cord[0]  # longitude
        y = cord[1]  # latitude
        north = max(north, y)
        south = min(south, y)
        west = min(west, x)
        east = max(east, x)
    return north, south, west, east


def get_mapping(
    word_2_cord: dict,
    index_2_word: dict,
    word_2_index: dict,
    cord_2_word: dict,
    ver_blk_len: float,
    hor_blk_len: float,
    west: float,
    north: float,
    default_block_len: int,
    coordinates: List[List[int]],
) -> None:
    for i in range(0, len(coordinates)):
        cord = coordinates[i]
        x = cord[0]  # longitude
        y = cord[1]  # latitude
        dis_from_w = x - west
        c = dis_from_w // hor_blk_len
        if c == default_block_len:
            c -= 1
        dis_from_n = north - y
        r = dis_from_n // ver_blk_len
        if r == default_block_len:
            r -= 1
        index = int(r * default_block_len + c)
        word = index_2_word[index]
        word_2_index[word] = index
        word_2_cord[word].append(i)
        cord_2_word[i] = word


def resize(
    coordinates: List[List[int]],
    cords: List[int],
    cord_2_word: dict,
    word_2_cord: dict,
    default_sub_block_len=2,
) -> None:
    # ================= constructing =================
    # if default_sub_block_len is bigger than 5
    # need to add a method to generate appending words
    # ================= constructing =================
    cords_list = [coordinates[i] for i in cords]
    north, south, west, east = get_boundary(cords_list)
    ver_blk_len = (north - south) / default_sub_block_len
    hor_blk_len = (east - west) / default_sub_block_len
    new_words = []
    prev_word = ""
    for i in cords:
        cord = coordinates[i]
        x = cord[0]  # longitude
        y = cord[1]  # latitude
        dis_from_w = x - west
        c = dis_from_w // hor_blk_len
        if c == default_sub_block_len:
            c -= 1

        dis_from_n = north - y
        r = dis_from_n // ver_blk_len
        if r == default_sub_block_len:
            r -= 1
        prev_word = cord_2_word[i]

        index = int(r * default_sub_block_len + c)

        curr_word = "".join([prev_word, "0", chr(ord("A") + index)])
        cord_2_word[i] = curr_word
        if curr_word not in word_2_cord:
            word_2_cord[curr_word] = []
        word_2_cord[curr_word].append(i)
        new_words.append(curr_word)

    if prev_word in word_2_cord:
        word_2_cord[prev_word] = []

    for word in new_words:
        temp_cords = word_2_cord[word]
        size = len(temp_cords)
        # ================= constructing =================
        limit = default_block_num * resize_factor
        if size > 3:
            resize(coordinates, temp_cords, cord_2_word, word_2_cord, 2)


def write_trajactories(trajactories: List[List[List[int]]]) -> None:
    filename = "trajactories.txt"
    with open(filename, "w") as file:
        for t in trajactories:
            file.write(str(t))
            file.write("\n")
