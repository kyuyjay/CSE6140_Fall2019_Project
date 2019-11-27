import random
import math
import time

def nearest_neighbor(params, cities, cutoff):
    start_time = time.time()
    best = float('inf')
    best_path = None
    trace = []

    cities = [tuple(city) for city in cities]

    for city in cities:
        if cutoff > time.time():
            return (trace, best, best_path)
        quality, path = _nearest_neighbor(city, params, cities)
        if quality < best:
            best_path = path
            best = quality
            trace.append([round(time.time() - start_time, 2), best])

    return (trace, best, best_path)

def _nearest_neighbor(start, params, cities):
    visited = set()
    visited.add(start)
    current = start

    path = [current[0]]
    quality = 0
    while len(visited) < len(cities):
        dmin, closest = closest_city(current, cities, visited)
        visited.add(closest)
        path.append(closest[0])
        quality += dmin

    return (quality, path)

def l2_distance(x1, y1, x2, y2):
    return round(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

def closest_city(start, cities, visited):
    dmin = float('inf')

    for city in cities:
        if city in visited:
            continue
        n = city[0]
        x = city[1]
        y = city[2]

        d = l2_distance(start[1], start[2], x, y)
        if d < dmin:
            dmin = d
            closest = city

    return dmin, closest

