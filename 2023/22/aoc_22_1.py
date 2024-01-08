#!/usr/bin/env python3

import sys
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class Block:
    cubes: frozenset[(int, int, int)]

    @classmethod
    def fromends(cls, start, end):
        cubes = set()
        x0, y0, z0 = start
        x1, y1, z1 = end

        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    cubes.add((x, y, z))

        return cls(frozenset(cubes))

    def length(self):
        return len(self.cubes)

    def move_down(self):
        return Block(frozenset((x, y, z - 1) for (x, y, z) in self.cubes))

    def bottom(self):
        return min(z for (_, _, z) in self.cubes)

    def top(self):
        return max(z for (_, _, z) in self.cubes)

    def height(self):
        return self.top() - self.bottom() + 1

def parse(line):
    m = re.match(r"(\d+),(\d+),(\d+)\~(\d+),(\d+),(\d+)", line)
    return Block.fromends((int(m[1]), int(m[2]), int(m[3])), (int(m[4]), int(m[5]), int(m[6])))

def overlap(cubes, before, after):
    if before.height() > 1:
        # remove the current block from cubes before looking for intersection
        # if not a vertical block will overlap with itself
        return cubes.difference(before.cubes).intersection(after.cubes)
    else:
        return cubes.intersection(after.cubes)

def apply_gravity(blocks: list[Block]) -> list[Block]:
    cubes = {c for b in blocks for c in b.cubes}
    moves = True
    while moves:
        moves = False
        for i, b in enumerate(blocks):
            if b.bottom() > 1:
                d = b.move_down()
                if not overlap(cubes, b, d):
                    moves = True
                    cubes.difference_update(b.cubes)
                    blocks[i] = d
                    cubes.update(d.cubes)
    return blocks

def disintegrate_count(blocks):
    cubes = {c for b in blocks for c in b.cubes}
    count = len(blocks)
    for b in blocks:
        # disintegrate block
        cubes.difference_update(b.cubes)
        for o in (x for x in blocks if x != b):
            if o.bottom() > 1:
                d = o.move_down()
                if not overlap(cubes, o, d):
                    count -= 1
                    break
        # reintegrate block
        cubes.update(b.cubes)
    return count

# Could speed some of these up by keeping two maps
# height -> block based on top/bottom
lines = map(str.rstrip, sys.stdin)
blocks = list(map(parse, lines))

blocks = apply_gravity(blocks)

print(disintegrate_count(blocks))
