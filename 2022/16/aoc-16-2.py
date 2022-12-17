#!/usr/bin/env /usr/bin/python3

import sys
import re
import itertools
from itertools import product, islice
import copy
from copy import copy

parse_re = re.compile("^Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)$")

class Valve:
    def __init__(self, valve, flow, routes):
        self.valve = valve
        self.flow = flow
        self.routes = routes

    def __str__(self):
        return f"{{valve = {self.valve}, flow = {self.flow}, routes = {self.routes}}}"

    def __repr__(self):
        return self.__str__()

# Someone in the tunnel system heading to a target
class Actor:
    def __init__(self, id, target, dist):
        self.id = id
        self.target = target
        self.dist = dist

    def __str__(self):
        return f"{{id = {self.id}, target = {self.target}, dist = {self.dist}}}"

    def __repr__(self):
        return self.__str__()

def parse_line(line):
    m = parse_re.match(line)
    if m:
        valve = m.group(1)
        flow = int(m.group(2))
        routes = set(map(str.strip, m.group(3).split(",")))
        return Valve(valve, flow, routes)
    print(f"Couldn't parse line: {line}")
    raise

# return number of steps from src to dest on shortest path
def path(valves, src, dest):
    len = 0
    visited = {src:None}

    again = True
    while again:
        again = False
        len += 1
        for x in visited.copy():
            valve = valves[x]
            for route in valve.routes:
                if route not in visited:
                    again = True
                    visited[route] = x
                if route == dest:
                    return len

    print("Disconnected")
    # If graph is disconnceted we would use a slightly different
    # strategy where we prune it first
    # (might be complicated if graph isn't symmetric
    # - by that I mean every directed edge has a corresponding
    # - return edge)
    raise


# return hash of (src,dest), len)
# I.e to get from src to dest requires len steps
def build_paths(valves):
    for src in valves:
        for dest in valves:
            if src != dest:
                yield ((src, dest), path(valves, src, dest))

# List of all next actor strategies to use
def actor_strategy(paths, unused, actor, actors):
    if actor.dist != None or not actor.target:
        yield actor
    else:
        have_targets = False
        pos = actor.target
        for target in unused:
            if target not in (actor.target for actor in actors):
                yield Actor(actor.id, target, paths[(pos, target)])
                have_targets = True
        if not have_targets:
            # because we're using cross product, need to supply something
            yield Actor(actor.id, None, None)

def actors_strategy(paths, unused, actors):
    x = map(lambda actor: actor_strategy(paths, unused, actor, actors), actors)
    return product(*x)

# our strategy is to pick a next valve to open
# if we're there then open it an then pick another
# if we're not then pick a tunnel that takes us closer
# if we're ever at a valve with more flow than the target
# then abort
def solve(valves, paths, unused, actors, minutes, score):
    # We can't score any more if there are no unused valves
    # or we're in the last minute
    if minutes < 0 or not unused:
        yield score
        return

    for a1, a2 in actors_strategy(paths, unused, actors):
        if a1.target == a2.target:
            # strategy has given same target to both actors (or both stopped)
            continue
        new_actors = [copy(a1), copy(a2)]
        used = set()
        extra_score = 0
        # how many minutes can we tick just by following the current targets?
        mins = min(actor.dist for actor in new_actors if actor.target)
        # don't have time to open another valve
        if minutes - mins - 1 < 0:
            yield score
            return
        for actor in (actor for actor in new_actors if actor.target):
            if actor.dist == mins:
                actor.dist = None
                flow = valves[actor.target].flow
                extra_score += (minutes - mins) * flow
                used.add(actor.target)
            elif actor.dist:
                actor.dist -= mins + 1 # 1 extra step while the other actor opens a valve
        yield from solve(valves, paths, unused - used, new_actors, minutes - mins - 1, score + extra_score)

valves = {x.valve:x for x in map(parse_line, sys.stdin)}
paths = {k:v for k, v in build_paths(valves)}
unused = {k for k, valve in valves.items() if valve.flow > 0}
actors = [Actor(0, "AA", None), Actor(1, "AA", None)]
ans = solve(valves, paths, unused, actors, 25, 0)
print(max(islice(ans, 1000000)))
#print(max(ans))
