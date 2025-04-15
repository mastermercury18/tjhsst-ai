from collections import deque 
from time import perf_counter
import sys

#text_input = sys.argv[1]

with open("slide_puzzle_tests.txt") as f:
    line_list = [line.strip() for line in f]

def get_row_col(line, charac, size):
    row, col = 0, 0
    for index, val in enumerate(line):
        if val == charac:
            return row,col
        if (index+1) % size == 0 and index != 0:
            row += 1
            col = 0
        else:
            col += 1

def get_index(grid_pos, size):
    row,col = grid_pos
    index = row * size + col
    return index

def print_board(line, size):
    grid = ""
    for index, val in enumerate(line):
        if (index+1) % size == 0 and index != 0 and index != size ** 2 - 1:
            grid += val + "\n"
        else:
            grid += val + " "
    return grid

def find_goal(line):
    goal = ''.join(sorted(line.replace(".", ""))) + "."
    return goal

def swap(line, dot_pos, swap_pos, size):
    dot_index = get_index(dot_pos, size)
    swap_index = get_index(swap_pos, size)
    char_list = list(line)
    char_list[dot_index], char_list[swap_index] = char_list[swap_index], char_list[dot_index]
    return "".join(char_list)

def move_down(line, dot_pos, size):
    row, col = dot_pos
    swap_pos = (row+1,col)
    return swap(line, dot_pos, swap_pos, size)

def move_up(line, dot_pos, size):
    row, col = dot_pos
    swap_pos = (row-1,col)
    return swap(line, dot_pos, swap_pos, size)

def move_right(line, dot_pos, size):
    row, col = dot_pos
    swap_pos = (row,col+1)
    return swap(line, dot_pos, swap_pos, size)

def move_left(line, dot_pos, size):
    row, col = dot_pos
    swap_pos = (row,col-1)
    return swap(line, dot_pos, swap_pos, size)

def get_children(line, size):
    children = []
    dot_pos = get_row_col(line, ".", size)
    row, col = dot_pos
    if row != 0:
        children.append(move_up(line, dot_pos, size))
    if row != size-1:
        children.append(move_down(line, dot_pos, size))
    if col != 0:
        children.append(move_left(line, dot_pos, size))
    if col != size-1:
        children.append(move_right(line, dot_pos, size))
    return children

def BFS(line,size):
    fringe = deque()
    visited = set()
    fringe.append((line, 0))
    visited.add(line)
    while fringe:
        newLine, steps = fringe.popleft()
        if newLine == find_goal(line):
            return steps
        for child in get_children(newLine,size):
            if child not in visited:
                fringe.append((child, steps+1))
                visited.add(child)
    return None

def main():
    for index, line in enumerate(line_list):
        start = perf_counter()
        size = int(line[0])
        moves = BFS(line[2::],size)
        end = perf_counter()
        total_time = end - start
        print("Line " + str(index) + ": " + line[2::] + ", " + str(moves) + " moves found in " + str(total_time) + " seconds")
main()