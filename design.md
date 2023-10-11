# Design

## Problem description

### Materials

Wood, bridge. Bridge has weight, wood does not (?). Joints also have weight.

## Goal

## Physics


### Collision

Collision matrix:

0: Ground
1: Car
2: Bridge / asphalt
3: Wood
4: Joint


|           | Ground    | Car   | Bridge    | Wood  | Joint     |
|-----------|-----------|-------|-----------|-------|-----------|
| Ground    |           | X     |           |       | X         |
| Car       | X         | X     | X         |       |           |
| Bridge    |           | X     |           |       |           |
| Wood      |           |       |           |       |           |
| Joint     | X         |       |           |       |           |
