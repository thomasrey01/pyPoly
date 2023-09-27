# Design

## Problem description

### Materials

Wood, bridge. Bridge has weight, wood does not (?). Joints also have weight.

## Goal

## Physics


### Collision

Collision matrix:

|           | Ground    | Car   | Bridge    | Wood  | Joint     |
|-----------|-----------|-------|-----------|-------|-----------|
| Ground    |           | X     |           |       | X         |
| Car       | X         | X     | X         |       |           |
| Bridge    |           | X     |           |       |           |
| Wood      |           |       |           |       |           |
| Joint     | X         |       |           |       |           |
