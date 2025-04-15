# def main():
#   f1 = "code_puzzles.txt"
#   f
from collections import deque
from time import perf_counter
import sys
from heapq import heapify, heappush, heappop


def get_row_col(index, size):
  row = index // size
  col = index % size
  return (row, col)


# def bfs(cube, size, grid):
#   fringe = deque()
#   visited = set()
#   fringe.append((cube, 0))
#   while fringe:
#     cube, moves = fringe.popleft()
#     if (check_goal(cube)):
#       print("the cube is " + str(cube))
#       return moves
#     else:
#       actualCube, newBoard = cube
#       kidlist = get_children(actualCube, size, grid)
#       for child in kidlist:
#         actualCube2, newBoard2 = child
#         cubeStr = cube_to_str(child, newBoard)
#         if cubeStr not in visited:
#           visited.add(cubeStr)
#           fringe.append((child, moves + 1))
#   return None


def taxicab(cube):
  actualCube, board = cube
  estimate = 0
  for charac in board:
    if charac == "@":
      estimate += 1
  return estimate


# def a_star(cube, size, grid):
#   visited = set()
#   fringe = []
#   heapify(fringe)
#   #fringe.append((cube, 0))
#   cubeStr = cube_to_str(cube)
#   heappush(fringe, (taxicab(cube), cubeStr, cube, 0))
#   while fringe:
#     dist, newCubeStr, newCube, moves = heappop(fringe)
#     if (check_goal(newCube)):
#       return moves
#     else:
#       if newCubeStr not in visited:
#         visited.add(newCubeStr)
#         kidlist = get_children(newCube, size, grid)
#         for child in kidlist:
#           cubeStr2 = cube_to_str(child)
#           if cubeStr2 not in visited:
#             newDist = moves + 1 + taxicab(child)
#             heappush(fringe, (newDist, cubeStr2, child, moves + 1))
#   return None

def a_star(cube, size, grid):
    visited = set()
    fringe = []
    cube_data = {}  # store cube and moves for each unique key
    key_counter = 0

    heapify(fringe)
    key_counter += 1
    cube_data[key_counter] = (cube, 0)
    heappush(fringe, (taxicab(cube), key_counter))

    while fringe:
        dist, key = heappop(fringe)
        newCube, moves = cube_data[key]

        if check_goal(newCube):
            return moves
        else:
            newcubeStr = cube_to_str(newCube)
            if newcubeStr not in visited:
                visited.add(newcubeStr)
                kidlist = get_children(newCube, size, grid)
                for child in kidlist:
                    cubeStr2 = cube_to_str(child)
                    if cubeStr2 not in visited:
                        key_counter += 1
                        newDist = moves + 1 + taxicab(child)
                        cube_data[key_counter] = (child, moves + 1)
                        heappush(fringe, (newDist, key_counter))
    return None


