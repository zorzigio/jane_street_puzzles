
from main import Die, TipType


steps: list[TipType] = [
    TipType.front,
    TipType.right,
    TipType.right,
    TipType.back,
    TipType.left,
    TipType.front,
]

die = Die()
print(die)
for step in steps:
    die = die.tipDie(step)
    print(die)
