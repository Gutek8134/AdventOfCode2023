from collections import Counter
STRENGTHS = "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"
TYPES = "High Card", "Pair", "Two Pairs", "Three of a Kind", "Full House", "Four of a Kind", "Five of a Kind"
JOKE_STRENGTHS = "J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"


class Hand:

    def __init__(self, hand: list[tuple[str, int]], bid: int, cards: str) -> None:
        self.hand: list[tuple[str, int]] = hand
        self.bid = bid
        self._type: tuple[int, int, int | None] | None = None
        self.cards = cards
        self.jokeCount = cards.count("J")

    @property
    def type(self) -> tuple[int, int, int | None]:
        if self._type is not None:
            return self._type
        return self._getType()

    @property
    def typeAsStr(self) -> str:
        return f"{TYPES[self.type[0]-1]} of {JOKE_STRENGTHS[self.type[1]]}{' and '+JOKE_STRENGTHS[(self.type[2] if self.type[2] is not None else 0)] if self.type[0] in (3,5) else ''}"

    def _getType(self) -> tuple[int, int, int | None]:

        if self.isFiveOfAKind():
            self._type = 7, JOKE_STRENGTHS.index(self.hand[0][0]), None
            return 7, JOKE_STRENGTHS.index(self.hand[0][0]), None

        if self.isFourOfAKind():
            self._type = 6, JOKE_STRENGTHS.index(self.hand[0][0]), None
            return 6, JOKE_STRENGTHS.index(self.hand[0][0]), None

        if self.isFullHouse():
            self._type = 5, JOKE_STRENGTHS.index(
                self.hand[0][0]), JOKE_STRENGTHS.index(self.hand[1][0])
            return 5, JOKE_STRENGTHS.index(self.hand[0][0]), JOKE_STRENGTHS.index(self.hand[1][0])

        if self.isThreeOfAKind():
            self._type = 4, JOKE_STRENGTHS.index(self.hand[0][0]), None
            return 4, JOKE_STRENGTHS.index(self.hand[0][0]), None

        if self.isTwoPairs():
            self._type = 3, JOKE_STRENGTHS.index(
                self.hand[0][0]), JOKE_STRENGTHS.index(self.hand[1][0])
            return 3, JOKE_STRENGTHS.index(self.hand[0][0]), JOKE_STRENGTHS.index(self.hand[1][0])

        if self.isPair():
            self._type = 2, JOKE_STRENGTHS.index(self.hand[0][0]), None
            return 2, JOKE_STRENGTHS.index(self.hand[0][0]), None

        self._type = 1, JOKE_STRENGTHS.index(self.hand[0][0]), None
        return 1, JOKE_STRENGTHS.index(self.hand[0][0]), None

    def isFiveOfAKind(self):
        return self.hand[0][1]+self.jokeCount == 5

    def isFourOfAKind(self):
        return self.hand[0][1]+self.jokeCount == 4

    def isFullHouse(self):
        if self.hand[0][1]+self.jokeCount >= 3 and len(self.hand) > 1:
            return self.hand[1][1]+self.jokeCount-self.hand[0][1] >= 2
        return False

    def isThreeOfAKind(self):
        if self.hand[0][1]+self.jokeCount >= 3 and len(self.hand) > 1:
            return self.hand[1][1]+self.jokeCount-self.hand[0][1] < 2
        return False

    def isTwoPairs(self):
        if self.hand[0][1]+self.jokeCount >= 2 and len(self.hand) > 1:
            return self.hand[1][1]+self.jokeCount-self.hand[0][1] >= 2
        return False

    def isPair(self):
        if self.hand[0][1]+self.jokeCount >= 2 and len(self.hand) > 1:
            return self.hand[1][1]+self.jokeCount-self.hand[0][1] < 2
        return False

    def __lt__(self, other) -> bool:
        if not isinstance(other, Hand):
            raise TypeError

        if self.type[0] != other.type[0]:
            return self.type[0] < other.type[0]

        # if self.type[1] != other.type[1]:
        #     return self.type[1] < other.type[1]

        # if self.type[0] in (3,5):
        #     if self.type[2] != other.type[2]:
        #         assert self.type[2] is not None and other.type[2] is not None
        #         return self.type[2] < other.type[2]

        for [lCard, rCard] in zip(self.cards, other.cards):
            if lCard != rCard:
                return JOKE_STRENGTHS.index(lCard) < JOKE_STRENGTHS.index(rCard)
        return False

    def __repr__(self) -> str:
        return f"{self.cards}: {self.typeAsStr}"


def main():
    hands: list[Hand] = []
    with open("./input.txt", "r") as f:
        for line in f.readlines():
            line = line.split()
            hand = Counter(line[0]).most_common()
            hands.append(Hand(hand, int(line[1]), line[0]))

    # print("Sorting...")

    hands.sort(reverse=False)
    with open("ddd.txt", "w") as f:
        for hand in hands:
            f.write(str(hand) + '\n')
    bidSum = 0
    for [rank, hand] in enumerate(hands, start=1):
        bidSum += rank * hand.bid
    print(bidSum)


if __name__ == "__main__":
    main()
