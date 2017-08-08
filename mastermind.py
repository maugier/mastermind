from collections import Counter
import random

class InvalidProposal(Exception):
    pass

class Game:
    colors = "12345678"
    size = 5

    def __init__(self):
        typ = type(self)
        self.answer = [random.choice(typ.colors) for _ in range(typ.size)]
        self.counter = 0
        self.unordered = Counter(self.answer)
        self.victory = False

    def propose(self, proposal):
        if len(proposal) != len(self.answer):
            raise InvalidProposal()

        white = sum(1 for (x,y) in zip(self.answer, proposal) if x == y)
        black = sum((self.unordered & Counter(proposal)).values()) - white
        
        self.counter += 1

        if white == len(self.answer):
            self.victory = True
        
        return (white, black)

