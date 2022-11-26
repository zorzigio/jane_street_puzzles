from pentagon import Pentagons
from itertools import product
from datetime import datetime
x = [2, 3, 4, 5]


problematic_sequences = [
    [2, 3, 3, 2]
]


def contains(sequence: list[int] | tuple[int], sub_sequence: list[list[int]]) -> bool:
    def to_string(sequence: list[int] | tuple[int]) -> str:
        return "".join(map(str, sequence))
    s = to_string(sequence)
    for sub in sub_sequence:
        if to_string(sub) in s:
            return True
    return False


if __name__ == "__main__":
    # pents = Pentagons.from_sequence([3, 2])
    # pents.plot()
    # pents = Pentagons.from_sequence([2, 2, 2, 2, 4])
    # pents.plot()

    # open file with datetime stamp
    with open(f"pentagons_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w") as f:

        min_distance = float("inf")
        sequence = []
        for i, perm in enumerate(product(x, repeat=15)):
            if i % 1000 == 0:
                print(i)
            if contains(perm, problematic_sequences):
                continue
            pents = Pentagons.from_sequence(list(perm))
            if pents.has_collisions:
                continue
            if pents.distance < min_distance:
                min_distance = pents.distance
                sequence = pents.sequence
                f.write(f"{min_distance:.7f} {sequence}")
                print(f"New min distance: {min_distance:.7f}")
                print(f"Sequence: {sequence}")

            # pents.plot()
        # pents.plot()
    print(f"New min distance: {min_distance:.7f}")
    print(f"Sequence: {sequence}")
