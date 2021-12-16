from itertools import dropwhile
from dataclasses import dataclass
from pprint import pprint
from enum import Enum
from math import prod


HEX_TO_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"}

with open("./input.txt", "r") as f:
    binary = [HEX_TO_BIN[c] for c in f.read().strip()]

binary_stream = "".join(binary)
binary_stream = "".join( # trim trailing zeros
    reversed(list(dropwhile(lambda s: s == "0", reversed(binary_stream)))))

@dataclass
class Header():
    version : int
    type_id : "TypeId"


@dataclass
class Literal():
    header: Header
    value: int


@dataclass
class Operator():
    header: Header
    subpackets: list


class Parser():
    def __init__(self, binary_stream):
        self.binary_stream = binary_stream
        self.p = 0
    
    def get_n(self, n : int):
        dat = self.binary_stream[self.p:self.p+n]
        self.p += n
        return dat

    def __iter__(self):
        return self

    def literal(self, header):
        p = self.p
        groups = []
        while self.binary_stream[p] == "1":
            groups.append(self.binary_stream[p+1:p+5])
            p += 5
        # now we handle the last group which is prefixed by 0
        groups.append(self.binary_stream[p+1:p+5])
        p += 5
        value = int("".join(groups), base=2)
        self.p = p
        return Literal(header, value)

    def operator(self, header):
        package = None
        p = self.p
        length_type_id = int(self.binary_stream[p])
        p += 1
        match length_type_id:
            case 0:
                total_length = int(self.binary_stream[p : p+15], base=2)
                p += 15
                self.p = p
                # we now know how long all our subpackages are so we
                # read subpackages until we've moved p that far.
                subpackets = []
                while self.p - p < total_length:
                    subpackets.append(self.parse_package())
                package = Operator(header, subpackets)
            case 1:
                number_of_subpackets = int(self.binary_stream[p : p+11], base=2)
                p += 11
                self.p = p
                subpackets = [self.parse_package() for _ in range(number_of_subpackets)]
                package = Operator(header, subpackets)
        return package

    def parse_package(self):
        if all(c == "0" for c in self.binary_stream[self.p:]):
            return None
        p = self.p
        package = None  
        version = int(self.binary_stream[p:p+3], base=2)
        p += 3
        type_id = TypeId(int(self.binary_stream[p:p+3], base=2))
        p += 3
        header = Header(version, type_id)
        self.p = p
        match type_id:
            case TypeId.LITERAL: # literal
                package = self.literal(header)
            case _: # operator
                package = self.operator(header)
        return package

    def __next__(self):
        if (pack := self.parse_package()) is not None:
            return pack
        else:
            raise StopIteration


class TypeId(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


def eval(package):
    match package:
        case Literal(value=v):
            return v
        case Operator(header=Header(type_id=TypeId.SUM), subpackets=subpackets):
            return sum(eval(sub) for sub in subpackets)
        case Operator(Header(type_id=TypeId.PRODUCT), subpackets):
            return prod(eval(sub) for sub in subpackets)
        case Operator(Header(type_id=TypeId.MINIMUM), subpackets):
            return min(eval(sub) for sub in subpackets)
        case Operator(Header(type_id=TypeId.MAXIMUM), subpackets):
            return max(eval(sub) for sub in subpackets)
        case Operator(Header(type_id=TypeId.GREATER_THAN), subpackets):
            assert(len(subpackets) == 2)
            return int(eval(subpackets[0]) > eval(subpackets[1]))
        case Operator(Header(type_id=TypeId.LESS_THAN), subpackets):
            assert(len(subpackets) == 2)
            return int(eval(subpackets[0]) < eval(subpackets[1]))
        case Operator(Header(type_id=TypeId.EQUAL_TO), subpackets):
            assert(len(subpackets) == 2)
            return int(eval(subpackets[0]) == eval(subpackets[1]))
        case _:
            raise ValueError("Invalid package: ", package)    


def version_sum(package):
    vs = 0
    match package:
        case Header(version, _) \
          | Literal(header=Header(version, _)):
            vs += version
        case Operator(header=Header(version, _), subpackets=subpackets):
            vs += version
            for p in subpackets:
                vs += version_sum(p)
        case _:
            raise NotImplementedError()
    return vs


def total_version_sum(packages): # not really necessary as there is only one package but yeah
    return sum(version_sum(p) for p in packages)


parser = Parser(binary_stream)
packages = list(iter(parser))

pprint(packages[0])
print(eval(packages[0]))