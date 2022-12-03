from pentagon import Pentagons
from datetime import datetime


if __name__ == "__main__":
    # open file with datetime stamp
    with open(f"pentagons_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w") as f:

        min_distance = float("inf")
        best_sequence = []
        sequence = [2] * 15
        i = -1
        while True:
            i += 1
            if i % 1000 == 0:
                print(f"i = {i} sequence = {sequence}")
            pents = Pentagons.from_sequence(sequence)
            if pents.distance < min_distance:
                min_distance = pents.distance
                best_sequence = pents.sequence
                f.write(f"{min_distance:.7f} ({min_distance})\n{best_sequence}\n\n")
                print(f"\tNew min distance: {min_distance:.7f}")
                print(f"\tSequence: {best_sequence}")
            sequence = pents.next_sequence()
            if sequence is None:
                break
            # pents.plot()

    print(f"New min distance: {min_distance:.7f}")
    print(f"Sequence: {best_sequence}")
