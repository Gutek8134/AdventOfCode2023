def clamp(n: int, min: int, max: int):
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n


class Point:
    maxX: int = 0
    maxY: int = 0

    def __init__(self, x: int, y: int, value: str) -> None:
        self.x: int = x
        self.y: int = y
        self.value: str = value
        self.added: bool = False

    def __repr__(self) -> str:
        return self.value

    def getSurroundingCoordinates(self) -> list[tuple[int, int]]:
        output: set[tuple[int, int]] = set()

        for x in (self.x - 1, self.x, self.x + 1):
            for y in (self.y - 1, self.y, self.y + 1):
                output.add((clamp(x, 0, Point.maxX), clamp(y, 0, Point.maxY)))

        output.remove((self.x, self.y))
        return list(output)

    def getNumber(self, schematic: list[list["Point"]]) -> int:
        if self.added or not self.value.isnumeric():
            return 0

        self.added = True
        number = self.value
        xCoord: int = self.x - 1
        currentPoint: Point = schematic[self.y][xCoord]
        while currentPoint.value.isnumeric():
            number = currentPoint.value + number
            currentPoint.added = True
            xCoord -= 1
            if not 0 <= xCoord < Point.maxX:
                break
            currentPoint: Point = schematic[self.y][xCoord]

        xCoord: int = self.x + 1
        currentPoint: Point = schematic[self.y][xCoord]
        while currentPoint.value.isnumeric():
            number += currentPoint.value
            currentPoint.added = True
            xCoord += 1
            if not 0 <= xCoord < Point.maxX:
                break
            currentPoint: Point = schematic[self.y][xCoord]

        return int(number)


def main() -> None:
    schematic: list[list[Point]] = []
    symbolCoordinates: list[tuple[int, int]] = []

    with open("./input.txt", "r") as f:
        for y, line in enumerate(f.read().splitlines()):
            temp: list[Point] = []
            for x, c in enumerate(line):
                temp.append(Point(x, y, c))
                if not (c.isnumeric() or c == "."):
                    symbolCoordinates.append((x, y))
            schematic.append(temp)

    Point.maxY = len(schematic)
    Point.maxX = len(schematic[0])

    numberSum = 0
    ratioSum = 0
    for [symbolX, symbolY] in symbolCoordinates:
        partNumbers = []
        for [x, y] in schematic[symbolY][symbolX].getSurroundingCoordinates():
            partNumber = schematic[y][x].getNumber(schematic)
            numberSum += partNumber
            if schematic[symbolY][symbolX].value == "*" and partNumber != 0:
                partNumbers.append(partNumber)
        if len(partNumbers) == 2:
            ratioSum += partNumbers[0] * partNumbers[1]

    print(ratioSum)


if __name__ == "__main__":
    main()
