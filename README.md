## About:

An attempt at making an algorithm that finds the longest path in a given maze

## Current algorithm:

- Find first path using a wave function collapse approach (number of futur moves + inverse manhattan distance)
- Pick two random points on the path
- Try to generate a longer path between those two points using the same path generation (loop to a given depth)

## Possible improvements:

- Pick points of interest instead of random points?
- Replace the points with a sliding window?
