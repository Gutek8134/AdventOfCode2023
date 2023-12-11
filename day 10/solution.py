def findNextPosition(Map: list[str], size: int,  currentPosition: tuple[int, int], previousPosition: tuple[int, int]) -> tuple[int, int]:
    # Generate possible moves
    possibleMoves: list[tuple[int, int]] = []
    currentPipe = Map[currentPosition[0]][currentPosition[1]]
    if currentPipe == "S":
        # Can go up?
        if Map[max(currentPosition[0]-1, 0)][currentPosition[1]] in ("|", "7", "F"):
            possibleMoves.append(
                (max(currentPosition[0]-1, 0), currentPosition[1]))

        # down?
        if Map[min(currentPosition[0]+1, size)][currentPosition[1]] in ("|", "J", "L"):
            possibleMoves.append(
                (min(currentPosition[0]+1, size), currentPosition[1]))

        # left?
        if Map[currentPosition[0]][max(currentPosition[1]-1, 0)] in ("-", "F", "L"):
            possibleMoves.append(
                (currentPosition[0], max(currentPosition[1]-1, 0)))

        # right?
        if Map[currentPosition[0]][min(currentPosition[1]+1, size)] in ("-", "J", "7"):
            possibleMoves.append(
                (currentPosition[0], min(currentPosition[1]+1, size)))

    elif currentPipe == "|":
        # Came from bottom
        if previousPosition[0] == currentPosition[0]+1:
            possibleMoves.append((currentPosition[0]-1, currentPosition[1]))
        else:
            possibleMoves.append((currentPosition[0]+1, currentPosition[1]))

    elif currentPipe == "-":
        # Came from right
        if previousPosition[1] == currentPosition[1]+1:
            possibleMoves.append((currentPosition[0], currentPosition[1]-1))
        else:
            possibleMoves.append((currentPosition[0], currentPosition[1]+1))

    elif currentPipe == "L":
        # Came from right
        if previousPosition[1] == currentPosition[1]+1:
            possibleMoves.append((currentPosition[0]-1, currentPosition[1]))
        else:
            possibleMoves.append((currentPosition[0], currentPosition[1]+1))

    elif currentPipe == "J":
        # Came from top
        if previousPosition[0] == currentPosition[0]-1:
            possibleMoves.append((currentPosition[0], currentPosition[1]-1))
        else:
            possibleMoves.append((currentPosition[0]-1, currentPosition[1]))

    elif currentPipe == "7":
        # Came from bottom
        if previousPosition[0] == currentPosition[0]+1:
            possibleMoves.append((currentPosition[0], currentPosition[1]-1))
        else:
            possibleMoves.append((currentPosition[0]+1, currentPosition[1]))

    elif currentPipe == "F":
        # Came from bottom
        if previousPosition[0] == currentPosition[0]+1:
            possibleMoves.append((currentPosition[0], currentPosition[1]+1))
        else:
            possibleMoves.append((currentPosition[0]+1, currentPosition[1]))

    # print(currentPosition, possibleMoves, [
    #       Map[move[0]][move[1]] for move in possibleMoves])
    return possibleMoves[0]


def main() -> None:
    with open("./input.txt", "r") as f:
        Map: list[str] = f.read().splitlines()
        MapSize = len(Map)-1

    startPosition: tuple[int, int] = tuple[int, int]()
    for rowIndex, row in enumerate(Map):
        found = False
        for colIndex, value in enumerate(row):
            if value == "S":
                startPosition = tuple[int, int]((rowIndex, colIndex))
                found = True
                break

        if found:
            break

    currentPosition: tuple[int, int] = startPosition
    previousPosition: tuple[int, int] = currentPosition

    loopLength: int = 1
    currentPosition = findNextPosition(
        Map, MapSize, currentPosition, previousPosition)
    # print(previousPosition, currentPosition)

    while Map[currentPosition[0]][currentPosition[1]] != "S":
        previousPosition, currentPosition = currentPosition, findNextPosition(
            Map, MapSize, currentPosition, previousPosition)
        loopLength += 1
        # print(previousPosition, currentPosition)

    print(loopLength//2)


if __name__ == "__main__":
    main()
