from math import sqrt, floor, ceil


def main():
    with open("./input.txt", "r") as f:
        times = list(map(int, f.readline().split()[1:]))
        distances = list(map(int, f.readline().split()[1:]))

    # Part 1
    output = 1
    for [time, distance] in zip(times, distances):
        deltaRoot = sqrt(time**2 - 4*distance)
        v1: int = ceil((time-deltaRoot)/2) if not ((time-deltaRoot) /
                                                   2).is_integer() else int((time-deltaRoot)//2)+1
        v2: int = floor((time+deltaRoot)/2) if not ((time+deltaRoot) /
                                                    2).is_integer() else int((time+deltaRoot)//2)-1
        output *= v2-v1+1

    print(output)
    # Part 2
    time = int("".join(map(str, times)))
    distance = int("".join(map(str, distances)))
    deltaRoot = sqrt(time**2 - 4*distance)
    v1: int = ceil((time-deltaRoot)/2) if not ((time-deltaRoot) /
                                               2).is_integer() else ceil((time-deltaRoot)/2)+1
    v2: int = floor((time+deltaRoot)/2) if not ((time+deltaRoot) /
                                                2).is_integer() else floor((time+deltaRoot)/2)-1
    print(v2-v1+1)


if __name__ == "__main__":
    main()
