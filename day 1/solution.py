NUMBERS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)


def main() -> None:
    lines: list[str]
    with open("./input.txt", "r") as f:
        lines = f.readlines()
    numbers: list[int] = []

    for line in lines:
        first: int = -1
        last: int = -1

        buffer = ""
        breakFor = False
        for char in line:
            buffer += char
            if char.isnumeric():
                first = int(char)
                break

            for i, number in enumerate(NUMBERS):
                if number in buffer:
                    first = i
                    breakFor = True
                    break

            if breakFor:
                break

        buffer = ""
        breakFor = False
        for char in reversed(line):
            buffer = char + buffer
            if char.isnumeric():
                last = int(char)
                break

            for i, number in enumerate(NUMBERS):
                if number in buffer:
                    last = i
                    breakFor = True
                    break

            if breakFor:
                break

        if first == -1 or last == -1:
            print("not found first or last")
            return
        numbers.append(10 * first + last)

    print(sum(numbers))


if __name__ == "__main__":
    main()
