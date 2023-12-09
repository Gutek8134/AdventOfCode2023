def main():
    with open("input.txt", "r") as f:
        readings: list[list[int]] = [
            list(map(int, line.split())) for line in f.readlines()]

    for reading in readings:
        diff: list[int] = [y-x for x, y in zip(reading[:-1], reading[1:])]
        firstValuesOfLevel: list[int] = [reading[0]]
        lastValuesOfLevel: list[int] = [reading[-1]]
        changeSign = True
        while any(value != 0 for value in diff):
            # print(diff)
            lastValuesOfLevel.append(diff[-1])
            firstValuesOfLevel.append(diff[0] if not changeSign else -diff[0])
            changeSign = not changeSign
            diff = [y-x for x, y in zip(diff[:-1], diff[1:])]

        extrapolationForward = sum(lastValuesOfLevel)
        reading.append(extrapolationForward)
        extrapolationBackward = sum(firstValuesOfLevel)
        reading.insert(0, extrapolationBackward)

    # Part 1
    print(sum(x[-1] for x in readings))

    # Part 2
    print(sum(x[0] for x in readings))


if __name__ == "__main__":
    main()
