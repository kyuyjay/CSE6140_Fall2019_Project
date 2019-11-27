The construction heuristic we have chosen to implement is nearest neighbor. The algorithm is simple: Start at any location $c$, it to the path, find the nearest location $c_1$ to $c$, and repeat the process with $c_1$ as the new starting point until there are no locations left to add. The pseudocode is as follows:

```python
let start = c
let visited = set()
let path = []
while len(visited) < len(locations):
    visited.add(start)
    path.append(start)
    let start = find_nearest(start)
return path
```

Where the `find_nearest` routine computes the distance, whichever metric is preferred, between `start` and all other locations and returns the location with the least distance from `start`. This requires looping through all locations. Since we must call `find_nearest` once for each location, we will loop through all locations once for each location. Thus, it is clear that this algorithm runs in $O(n^2)$ time, where $n$ is the number of locations. What remains is the problem of choosing $c$.

The choice of $c$ can impact performance. When experimenting with different starting points, we found several improvements over the location that was listed first in the list of locations. We performed this evaluation by running the above algorithm with each city as a starting point. This, of course, runs an $O(n^2)$ algorithm $n$ times, which would make trying each city as a starting point $O(n^3)$. 

One could also choose a random starting point, which makes no guarantees of finding the most optimal solution (in the context of a nearest-neighbor approximation), but maintains an $O(n^2)$ runtime.