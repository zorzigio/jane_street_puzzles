from enum import Enum


class TipType(Enum):
    front = "front"
    back = "back"
    left = "left"
    right = "right"


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Board:
    def __init__(self) -> None:
        self.board = [
            [57,    33,    132,   268,   492,   732],
            [81,    123,   240,   443,   353,   508],
            [186,   42,    195,   704,   452,   228],
            [-7,    2,     357,   452,   317,   395],
            [5,     23,    -4,    592,   445,   620],
            [0,     77,    32,    403,   337,   452],
        ]
        self.xlen = len(self.board[0])
        self.ylen = len(self.board)

    def value_at(self, point: Point) -> int:
        # one indexed
        x_index = point.x - 1
        y_index = self.ylen - point.y
        return self.board[y_index][x_index]


board = Board()


class Die:
    def __init__(self) -> None:
        self.value = 0
        self.round = 0
        # position
        self.tip: TipType | None = None
        self.x = 1
        self.y = 1
        # initialize faces to Nan
        self.up: int | None = None
        self.down: int | None = None
        self.left: int | None = None
        self.right: int | None = None
        self.front: int | None = None
        self.back: int | None = None
        #
        self.is_valid = True

    def tipDie(self, tip: TipType) -> "Die":
        die = self.copy()
        die.tip = tip
        # move die
        match tip:
            case TipType.front:
                die.back, die.up, die.front, die.down = die.down, die.back, die.up, die.front
                die.y += 1
            case TipType.back:
                die.back, die.up, die.front, die.down = die.up, die.front, die.down, die.back
                die.y -= 1
            case TipType.left:
                die.right, die.up, die.left, die.down = die.down, die.right, die.up, die.left
                die.x -= 1
            case TipType.right:
                die.right, die.up, die.left, die.down = die.up, die.left, die.down, die.right
                die.x += 1
        # get value of square in new point
        square_value = board.value_at(Point(die.x, die.y))
        die.round += 1
        if die.up is None:
            # if up side is not set yet, compute it
            up = (square_value - die.value) / die.round
            if not up.is_integer():
                die.is_valid = False
                return die
            die.up = int(up)
            die.value = die.up * die.round + die.value
        else:
            # if the up side is already set, compute the die new value
            value = die.up * die.round + die.value
            if value != square_value:
                die.is_valid = False
                return die
            die.value = value
        return die

    def copy(self) -> "Die":
        new_die = Die()
        #
        new_die.value = self.value
        new_die.round = self.round
        # position
        new_die.tip = self.tip
        new_die.x = self.x
        new_die.y = self.y
        #
        new_die.up = self.up
        new_die.down = self.down
        new_die.left = self.left
        new_die.right = self.right
        new_die.front = self.front
        new_die.back = self.back
        new_die.is_valid = self.is_valid
        return new_die

    @property
    def p(self) -> Point:
        return Point(self.x, self.y)

    def __repr__(self) -> str:
        return f"Die({self.x}, {self.y}) value {self.value} at round {self.round}"


def get_movements(p: Point) -> list[TipType]:
    movements: list[TipType] = []
    if p.x != 1:
        movements.append(TipType.left)
    if p.x != board.xlen:
        movements.append(TipType.right)
    if p.y != 1:
        movements.append(TipType.back)
    if p.y != board.ylen:
        movements.append(TipType.front)
    return movements


def move_die(die: Die) -> list[Point] | None:
    # get list of possible movements
    movements = get_movements(die.p)
    for movement in movements:
        # move the die
        new_die = die.tipDie(movement)
        # check if the movement is valid
        if new_die.is_valid:
            # check if we are at the end of the board
            if new_die.x == board.xlen and new_die.y == board.ylen:
                # we are at the end of the board
                return [die.p, new_die.p]
            else:
                points = move_die(new_die)
                if points is not None:
                    points.insert(0, die.p)
                    return points


if __name__ == "__main__":
    die = Die()
    res = move_die(die)
    if res is not None:
        # all the squares on the board
        allSquares: set[tuple[int, int]] = set()
        for x in range(1, board.xlen + 1):
            for y in range(1, board.ylen + 1):
                allSquares.add((x, y))
        # all the squares on the path
        points = [(p.x, p.y) for p in res]
        unique = set(points)
        # all unvisited squares
        unvisited = allSquares - unique
        total_unvisited = sum(board.value_at(Point(x, y)) for x, y in unvisited)
        print(f"Total unvisited squares: {total_unvisited}")

        # print("Found Solution")
        # print(f"Visited points: {res}")
        # print(f"Unique Points: {unique}")
        # squares = board.xlen * board.ylen
        # unvisited = squares - len(unique)
        # print(f"unvisited squares: {unvisited}")
