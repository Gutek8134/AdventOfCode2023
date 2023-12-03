import re
from typing import Literal


def main() -> None:
    games: list[list[dict[str, int]]] = []
    with open("./input.txt", "r") as f:
        for line in f.readlines():
            games.append(
                list(
                    map(
                        lambda x: dict(
                            map(lambda y: (y.split()[1], int(y.split()[0])), x)
                        ),
                        map(
                            lambda x: x.split(", "),
                            line[line.find(":") + 1 :].split(";"),
                        ),
                    )
                )
            )

    idSum = 0
    powerSum = 0
    for id, game in enumerate(games, start=1):
        possible: bool = True
        reds = greens = blues = 0
        for grab in game:
            for [color, number] in grab.items():
                if (
                    (color == "red" and number > 12)
                    or (color == "green" and number > 13)
                    or (color == "blue" and number > 14)
                ):
                    possible = False

                if color == "red":
                    reds = max(reds, number)
                elif color == "green":
                    greens = max(greens, number)
                elif color == "blue":
                    blues = max(blues, number)

            # if not possible:
            #     break

        if possible:
            idSum += id

        powerSum += reds * greens * blues

    print(powerSum)


if __name__ == "__main__":
    main()
