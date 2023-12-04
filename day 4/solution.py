def main() -> None:
    scratchcards: list[tuple[set[int], set[int]]] = []
    totalCards: list[int] = []
    with open("./input.txt", "r") as f:
        for line in f.readlines():
            temp = line[line.index(":")+2:].split("|")
            scratchcards.append(
                (set(map(int, temp[0].split())), set(map(int, temp[1].split()))))
            totalCards.append(1)

    pointSum = 0
    for [i, [winningNumbers, numbers]] in enumerate(scratchcards):
        matches = len(numbers) - len(numbers.difference(winningNumbers))
        if matches > 0:
            pointSum += 2**(matches-1)
            for j in range(1, matches+1):
                totalCards[i+j] += totalCards[i]

    print(pointSum)
    print(sum(totalCards))


if __name__ == "__main__":
    main()
