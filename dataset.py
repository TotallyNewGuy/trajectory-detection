import random
from typing import List


def get_data() -> List[List[int]]:
    coordinates = []
    # [[x1, y1], [x2, y2]]
    for _ in range(100):
        x = random.randint(-700, 1000)
        y = random.randint(100, 1200)
        coordinates.append([x, y])
    return coordinates


coordinates = get_data()
trajactories = [get_data() for _ in range(10)]
