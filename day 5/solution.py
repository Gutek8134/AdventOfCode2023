import re

MAP_REGEX = re.compile(r"(?P<dest>\d+) (?P<source>\d+) (?P<range>\d+)\s*\n?$")
TRANSLATIONS = ("seeds", "soil", "fertilizer", "water",
                "light", "temperature", "humidity", "location")


class MyRange:
    """Start and end inclusive."""

    def __init__(self, start, length) -> None:
        self.beginning = start
        self.end = start+length-1

    @property
    def length(self):
        return self.end - self.beginning + 1

    def remap(self, cluster: "MapperCluster"):
        self.beginning = cluster[self.beginning]
        self.end = cluster[self.end]

    def overlap(self, otherRanges: set["MyRange"]) -> set["MyRange"]:
        """Produces ranges created by overlapping ranges with this one"""
        outcome: set[MyRange] = {self}
        for otherRange in otherRanges:
            toAdd: set[MyRange] = set()
            toDelete: set[MyRange] = set()

            for range in outcome:
                beginningIncluded = False
                temp = MyRange(0, 0)
                # Beginning happens to be within (one of) the original range(s) - split it into two
                if range.beginning <= otherRange.beginning <= range.end:
                    temp = MyRange(otherRange.beginning,
                                   range.end - otherRange.beginning+1)
                    toAdd.update(
                        {MyRange(range.beginning, otherRange.beginning-range.beginning),
                         MyRange(otherRange.beginning, range.end - otherRange.beginning+1)}
                    )
                    toDelete = {range}
                    beginningIncluded = True

                # End happens to be within original range
                if range.beginning <= otherRange.end <= range.end:
                    # Beginning is not - just split
                    if not beginningIncluded:
                        toAdd.update(
                            {MyRange(range.beginning, otherRange.end-range.beginning),
                             MyRange(otherRange.end, range.end - otherRange.end+1)}
                        )
                        toDelete = {range}

                    # Beginning is too - split the second range (temp)
                    else:
                        toAdd.update(
                            {MyRange(temp.beginning, otherRange.end-temp.beginning+1),
                             MyRange(otherRange.end+1, temp.end - otherRange.end)}
                        )
                        toDelete.update({temp})

            outcome.update(toAdd)
            outcome.difference_update(toDelete)

        return outcome

    @staticmethod
    def joinSet(jointSet: set["MyRange"]) -> set["MyRange"]:
        outcome = set()
        for el in jointSet:
            skip = False
            for other in jointSet.difference({el}):
                # Ranges can be

                # one enclosed into another - skip smaller one
                if other.beginning < el.beginning and el.end < other.end:
                    skip = True
                    break

                # intersected - add their concatenation
                # left-side
                if el.contains(other.end) and other.contains(el.beginning):
                    el.beginning = other.beginning
                # right-side
                elif el.contains(other.beginning) and other.contains(el.end):
                    el.end = other.end

                # # one next to another
                # # on the left
                # elif other.end == el.beginning-1:
                #     el.beginning = other.beginning
                # # on the right
                # elif other.beginning == el.end+1:
                #     el.end = other.end

            if not skip:
                outcome.add(el)
        return outcome

    def __hash__(self) -> int:
        return (self.beginning, self.end).__hash__()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MyRange):
            return False
        return __value.beginning == self.beginning and __value.end == self.end

    def __repr__(self) -> str:
        return f"[{self.beginning}..{self.end}]"

    def contains(self, value: int) -> bool:
        return self.beginning <= value <= self.end


class Mapper:
    def __init__(self, sourceStart: int, destinationStart: int, ranges: int) -> None:
        self.source = MyRange(sourceStart, ranges)
        self.destination = MyRange(destinationStart, ranges)
        self.ranges = ranges

    def containsSource(self, source: int) -> bool:
        return self.source.beginning <= source <= self.source.end

    def containsDestination(self, destination: int) -> bool:
        return self.destination.beginning <= destination <= self.destination.end

    def __getitem__(self, key: int) -> int:
        """
        Converts source to destination in this mapper
        """
        if not isinstance(key, int):
            raise TypeError("source must be an int")

        if not self.containsSource(key):
            raise IndexError

        return (key-self.source.beginning)+self.destination.beginning

    @property
    def difference(self):
        return self.destination.beginning - self.source.beginning


class MapperCluster:
    def __init__(self, mappers: list[Mapper] | tuple[Mapper, ...] | None = None) -> None:
        if mappers == None:
            self.mappers: list[Mapper] = []

        elif isinstance(mappers, tuple):
            self.mappers: list[Mapper] = list(mappers)

        else:
            self.mappers: list[Mapper] = mappers

    def __getitem__(self, source: int) -> int:
        """
        Converts source to destination from any of the mappers
        """
        for mapper in self.mappers:
            if mapper.containsSource(source):
                return mapper[source]
        return source

    def addMapper(self, mapper: Mapper) -> None:
        self.mappers.append(mapper)

    def convertMyRange(self, range: MyRange):
        tLen = range.length
        range.beginning = self[range.beginning]
        range.end = range.beginning + tLen-1

    def getRanges(self) -> set[MyRange]:
        outcome = set()
        for mapper in self.mappers:
            outcome.add(mapper.source)
        return outcome


def main():

    MapperClusters: list[MapperCluster] = []

    with open("./input.txt", "r") as f:
        firstLine: str = f.readline()
        seeds: list[int] = [
            int(x) for x in firstLine[firstLine.index(":")+2:-1].split()]
        seedsP2: set[MyRange] = {MyRange(x, y)
                                 for [x, y] in zip(seeds[::2], seeds[1::2])}
        currentMapperCluster = MapperCluster()
        for line in f.readlines()[1:]:
            if line[:-1] == "":
                MapperClusters.append(currentMapperCluster)
                currentMapperCluster = MapperCluster()
                continue

            match = re.match(MAP_REGEX, line)
            if match is None:

                continue

            currentMapperCluster.addMapper(Mapper(int(match.group("source")), int(
                match.group("dest")), int(match.group("range"))))
        MapperClusters.append(currentMapperCluster)

    # Part 1
    # locations: list[int] = []
    # for seed in seeds:
    #     for cluster in MapperClusters:
    #         # print(seed, end="->")
    #         seed = cluster[seed]
    #     # print(seed)
    #     locations.append(seed)

    # print(min(locations))

    # Part 2
    # i = 0
    for cluster in MapperClusters:
        # print(TRANSLATIONS[i], seedsP2, cluster.getRanges())
        # i += 1
        temp: set[MyRange] = set()
        for _range in seedsP2:
            temp.update(_range.overlap(cluster.getRanges()))
        for _range in temp:
            cluster.convertMyRange(_range)
        seedsP2 = temp

    # print(TRANSLATIONS[i], seedsP2)

    outcome: list[int] = []
    for _range in seedsP2:
        outcome.extend((_range.beginning, _range.end))

    print(min(outcome)+1)


if __name__ == "__main__":
    main()
