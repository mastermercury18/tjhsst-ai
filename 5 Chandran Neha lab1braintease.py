from collections import deque 
from time import perf_counter
from time import perf_counter

with open("slide_puzzle_tests.txt") as f:
    line_list = [line.strip() for line in f]

with open("15_puzzles.txt") as f:
    four_list = [line.strip() for line in f]

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

def BFS_backwards(goal,size):
    fringe = deque()
    visited = set()
    total_solvable_puzzles = 1
    fringe.append(goal)
    visited.add(goal)
    while fringe:
        newLine = fringe.popleft()
        for child in get_children(newLine,size):
            if child not in visited:
                fringe.append(child)
                visited.add(child)
                total_solvable_puzzles += 1
    return total_solvable_puzzles

def BFS_ten(goal,size):
    fringe = deque()
    visited = set()
    num_ten_space_boards = 0
    fringe.append((goal, 0))
    visited.add(goal)
    while fringe:
        newLine, steps = fringe.popleft()
        if steps == 10:
            num_ten_space_boards += 1
        for child in get_children(newLine,size):
            if child not in visited:
                fringe.append((child, steps+1))
                visited.add(child)
    return num_ten_space_boards

def BFS_hardest(goal,size):
    fringe = deque()
    visited = set()
    steps_dict = {}
    fringe.append((goal, 0))
    visited.add(goal)
    while fringe:
        newLine, steps = fringe.popleft()
        steps_dict[newLine] = steps
        for child in get_children(newLine,size):
            if child not in visited:
                fringe.append((child, steps+1))
                visited.add(child)
    return steps_dict

def BFS_four_by_four(line,size):
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

def BFS_path(line,size):
    fringe = deque()
    visited = set()
    fringe.append((line, 0))
    visited.add(line)
    depth = -1
    while fringe:
        newLine, steps = fringe.popleft()
        if steps > depth:
            depth = steps
        if newLine == find_goal(line):
            return newLine
        for child in get_children(newLine,size):
            if child not in visited:
                fringe.append((child, steps+1))
                visited.add(child)
    return None

def main():
    for index, line in enumerate(line_list):
        start = perf_counter()
       # print("Line " + str(index) + " start state:")
        size = int(line[0])
        #print(print_board(line[2::], size))
       # print("Line " + str(index) + " goal state:" + find_goal(line[2::]))
        #print("Line " + str(index) + " children:" + str(get_children(line[2::], size)) + "\n")
        moves = BFS(line[2::],size)
        end = perf_counter()
        total_time = end - start
        print("Line " + str(index) + ": " + line[2::] + ", " + str(moves) + " moves found in " + str(total_time) + " seconds")
#main()

def teaser_1():
    goal_two_by_two = "ABC."
    goal_three_by_three = "ABCDEFGH."
    total = BFS_backwards(goal_two_by_two, 2) + BFS_backwards(goal_three_by_three, 3)
    print(str(total))
#teaser_1()

def teaser_2():
    print("21345678.")
#teaser_2()

def teaser_3():
    print(BFS_ten("ABCDEFGH.", 3))
#teaser_3()

def teaser_4():
    steps_dict = BFS_hardest("ABCDEFGH.", 3)
    max_steps = max(steps_dict.values())
    corres_keys = []
    for key in steps_dict:
        if steps_dict[key] == max_steps:
            corres_keys.append(key)
    #print("The maximum number of steps are: " + str(max_steps) + " the puzzles that take this many steps are: " + str(corres_keys) + " which has a length of: " + str(len(corres_keys)))
    #BFS_path("HFGBEDC.A", 3)
    print(BFS_path("FDGHE.CBA", 3))
#teaser_4()

def teaser_five():
    start = perf_counter()
    end = 0
    val = 0
    for index, line in enumerate(four_list):
        if (end - start > 60):
            return val
        #val = BFS(line,4)
        val = BFS(line,4)
        #print(val)
        end = perf_counter()
print(teaser_five())




