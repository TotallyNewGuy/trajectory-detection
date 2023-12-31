import random
import copy
from typing import List
from config import abnormal_factor


def get_normal_cord() -> List[List[int]]:
    coordinates = []
    # [[x1, y1], [x2, y2]]
    pre_x = random.randint(-700, 1000)
    pre_y = random.randint(100, 1200)

    for _ in range(120):
        x = pre_x + random.randint(-20, 20)
        y = pre_y + random.randint(-20, 20)
        coordinates.append([x, y])
        pre_x = x
        pre_y = y
        # x = random.randint(-700, 1000)
        # y = random.randint(100, 1200)
        # coordinates.append([x, y])
    return coordinates


def get_abnormal_traj(normal_traj: List[List[int]], factor=0.1) -> List[List[int]]:
    abnormal_traj = copy.deepcopy(normal_traj)
    memo = [[] for _ in range(len(abnormal_traj))]
    index = 0
    for t in abnormal_traj:
        length = int(len(t) * factor)
        start_index = random.randint(0, len(t) - length)
        for i in range(start_index, start_index + length):
            memo[index].append(i)
            cords = t[i]
            turbulence = random.randint(1, 30)
            if i < length // 2:
                cords[0] += turbulence
                cords[1] += turbulence
            else:
                cords[0] -= turbulence
                cords[1] -= turbulence
        index += 1

    write_down_outlier(memo, "../test_data/ab/memo.txt")

    return abnormal_traj


def write_down_outlier(memo: List[List[int]], filename: str) -> None:
    with open(filename, "w") as file:
        for m in memo:
            file.write(str(m))
            file.write("\n")


normal_traj = [get_normal_cord() for _ in range(10)]
abnormal_traj = get_abnormal_traj(normal_traj, abnormal_factor)
