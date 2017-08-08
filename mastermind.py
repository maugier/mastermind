from collections import Counter, defaultdict
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

        white = sum(1 for (x,y) in zip(answer, proposal) if x == y)
        black = sum((self.unordered & Counter(proposal)).values()) - white
        self.counter += 1

        if white == len(self.answer):
            self.victory = True
        
        return (white, black)

class Cheater:
    colors = "12345678"
    size = 5
    
    def generate(self, l):
        if l:
            for x in self.colors:
                for rest in self.generate(l - 1):
                    yield rest + (x,)
        else:
            yield ()

    def __init__(self):
        self.colors = type(self).colors
        self.potential = self.generate(type(self).size)

    def propose(self, proposal):

        if len(proposal) != type(self).size:
            raise InvalidProposal()

        uprop = Counter(proposal)

        buffer = defaultdict(lambda: [])
        best = (0, None)
        for answer in self.potential:
            white = sum(1 for (x,y) in zip(answer, proposal) if x == y)
            black = sum((uprop & Counter(answer)).values()) - white
            result = (white, black)

            bucket = buffer[result]
            bucket.append(answer)
            if len(bucket) > best[0]:
                best = (len(bucket), bucket, result)

        self.potential = best[1]
        return best[2]
