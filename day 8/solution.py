import re
from math import lcm

NODE_FORMAT = re.compile(r"(?P<name>\w+) = \((?P<left>\w+), (?P<right>\w+)\)")


class Node:
    def __init__(self, name: str,  left: str, right: str) -> None:
        self.left = left
        self.right = right
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name} ({self.left}, {self.right})"


class Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}

    def addNode(self, node: Node):
        self.nodes[node.name] = node

    def getNode(self, name: str):
        return self.nodes[name]


def main():
    Map: Graph = Graph()
    traverser: list[Node] = []
    with open("input.txt", "r") as f:
        directions: str = f.readline()[:-1]
        f.readline()
        for line in f.readlines():
            result = NODE_FORMAT.search(line)
            if result is None:
                continue

            node = Node(result.group(1), result.group(2), result.group(3))
            Map.addNode(node)
            if node.name[-1] == "A":
                traverser.append(node)

    # Part 1
    # currentNode: Node = Map.getNode("AAA")
    # stepsNeeded: int = 0
    # nextStepIndex = 0
    # while currentNode.name != "ZZZ":
    #     if directions[nextStepIndex] == "L":
    #         currentNode = Map.getNode(currentNode.left)
    #     elif directions[nextStepIndex] == "R":
    #         currentNode = Map.getNode(currentNode.right)
    #     stepsNeeded += 1
    #     nextStepIndex += 1
    #     if nextStepIndex >= len(directions):
    #         nextStepIndex = 0

    # print(stepsNeeded)

    allStepsNeeded: list[int] = []
    nextStepIndex = 0
    for currentNode in traverser:
        stepsNeeded: int = 0
        nextStepIndex = 0
        while currentNode.name[-1] != "Z":
            if directions[nextStepIndex] == "L":
                currentNode = Map.getNode(currentNode.left)
            elif directions[nextStepIndex] == "R":
                currentNode = Map.getNode(currentNode.right)
            stepsNeeded += 1
            nextStepIndex += 1
            if nextStepIndex >= len(directions):
                nextStepIndex = 0
        allStepsNeeded.append(stepsNeeded)

    print(lcm(*allStepsNeeded))


if __name__ == "__main__":
    main()
