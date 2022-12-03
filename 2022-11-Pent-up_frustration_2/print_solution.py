
from pentagon import Pentagons

sequence = [2, 5, 2, 5, 2, 3, 4, 2, 5, 2, 3, 4, 2, 3, 5]

pents = Pentagons.from_sequence(sequence)
# pents.plot()
pents.save()
