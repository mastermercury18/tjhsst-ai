from collections import deque 
from time import perf_counter
import sys

textfilemain = sys.argv[1]

with open(textfilemain) as f:
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

def bi_BFS_steps(line,size):
    fringe_source = deque()
    visited_source = set()
    fringe_source.append((line,0))
    visited_source.add(line)
    source_dict = {}
    source_dict[line] = 0

    fringe_goal = deque()
    visited_goal = set()
    fringe_goal.append((find_goal(line),0))
    visited_goal.add(find_goal(line))
    goal_dict = {}
    goal_dict[find_goal(line)] = 0

    while fringe_source and fringe_goal:
        newLine1, steps1 = fringe_source.popleft()
        newLine2, steps2 = fringe_goal.popleft()

        for child in get_children(newLine1,size):
            if child not in visited_source:
                fringe_source.append((child, steps1 + 1))
                visited_source.add(child)
                source_dict[child] = steps1 + 1
                if newLine1 in visited_goal:
                    #return steps1+steps2 + 1
                    return goal_dict[newLine1] + steps1
                
        for child2 in get_children(newLine2,size):
            if child2 not in visited_goal:
                fringe_goal.append((child2, steps2 + 1))
                visited_goal.add(child2)
                goal_dict[child2] = steps2 + 1
                if newLine2 in visited_source:
                    #return steps2+steps1 + 1
                    return source_dict[newLine2] + steps2
                
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
        moves = bi_BFS_steps(line[2::],size)
        end = perf_counter()
        total_time = end - start
        print("Bi-BFS: " + "Line " + str(index) + ": " + line[2::] + ", " + str(moves) + " moves found in " + str(total_time) + " seconds")
        start2 = perf_counter()
        moves2 = BFS(line[2::],size)
        end2 = perf_counter()
        total_time2 = end2 - start2
        print("BFS: " + "Line " + str(index) + ": " + line[2::] + ", " + str(moves2) + " moves found in " + str(total_time2) + " seconds" + "\n")
main()

# def teaser_five_new():
#     start = perf_counter()
#     end = 0
#     val = 0
#     for index, line in enumerate(four_list):
#         if (end - start > 60):
#             return val
#         val = bi_BFS_steps(line,4)
#         end = perf_counter()
# print("The longest path bi-BFS can run in less than a minute is: " + str(teaser_five_new()))

# def teaser_five():
#     start = perf_counter()
#     end = 0
#     val = 0
#     for index, line in enumerate(four_list):
#         if (end - start > 60):
#             return val
#         val = BFS(line,4)
#         end = perf_counter()
# print("The longest path BFS can run in less than a minute is: " + str(teaser_five()))

# start = perf_counter()
# #word_file = sys.argv[1]
# #puzzle_file = sys.argv[2]

# word_file = "words_06_letters.txt"
# puzzle_file = "puzzles_normal.txt"

# with open(word_file) as f:
#     wordset = set([line.strip() for line in f])
# puzzles_dict = {}

# alpha = "abcdefghijklmnopqrstuvwxyz"

# def get_children(word):
#     myset = set()
#     for i, char in enumerate(word):
#         for letter in alpha:
#             if letter != char:
#                 child = word[:i] + letter + word[i+1:]
#                 if child in wordset:
#                     myset.add(child)
#     return myset

# def create_child_dict():
#     child_dict = {}
#     for word in wordset:
#        child_dict[word] = get_children(word)
#     return child_dict

# child_dict = create_child_dict()

# end = perf_counter()

# #print("Time it took to create data structure: " + str(end - start))

# start = perf_counter()
# start2 = perf_counter() 

# with open(puzzle_file) as f:
#     for line in f:
#         arr = line.split()
#         puzzles_dict[arr[0]] = arr[1]

# def bi_BFS(line,goal):
#     fringe_source = deque()
#     visited_source = set()
#     fringe_source.append((line,[line]))
#     visited_source.add(line)
#     source_dict = {}
#     #source_dict[line] = line

#     fringe_goal = deque()
#     visited_goal = set()
#     fringe_goal.append((goal,[goal]))
#     visited_goal.add(goal)
#     goal_dict = {}
#     #goal_dict[goal] = goal

#     while fringe_source and fringe_goal:
#         newLine1, path1 = fringe_source.popleft()
#         newLine2, path2 = fringe_goal.popleft()

#         for child in child_dict[newLine1]:
#             if child not in visited_source:
#                 fringe_source.append((child, path1 + [child]))
#                 visited_source.add(child)
#                 source_dict[child] = path1
#                 if newLine1 in visited_goal:
#                     print("Length is: " + str(len(path1 + goal_dict[newLine1])))
#                     return "\n".join(path1 + goal_dict[newLine1])
#                     #return path1 + goal_dict[newLine1]
                
#         for child2 in child_dict[newLine2]:
#             if child2 not in visited_goal:
#                 fringe_goal.append((child2, [child2] + path2))
#                 visited_goal.add(child2)
#                 goal_dict[child2] = path2
#                 if newLine2 in visited_source:
#                     print("Length is: " + str(len(source_dict[newLine2] + path2)))
#                     return "\n".join(source_dict[newLine2] + path2)
#                     #return source_dict[newLine2] + path2

# def BFS_path(word,goal):
#     fringe = deque()
#     visited = set()
#     fringe.append((word,[word]))
#     visited.add(word)
#     while fringe:
#         newWord, path = fringe.popleft()
#         if newWord == goal:
#             print("Length is: " + str(len(path)))
#             return "\n".join(path)
#         for child in child_dict[newWord]:
#             if child not in visited:
#                 fringe.append((child, path + [child]))
#                 visited.add(child)
#     return "No solution!"

# def main2():
#     line_num = 0
#     for key in puzzles_dict:
#        print("Line: " + str(line_num))
#        line_num += 1
#        print(bi_BFS(key, puzzles_dict[key]))
#        print("\n")
# main2()

# end = perf_counter()
# print("Bi-BFS time to solve all puzzles: " + str(end - start))

# def main3():
#     line_num = 0
#     for key in puzzles_dict:
#        print("Line: " + str(line_num))
#        line_num += 1
#        print(BFS_path(key, puzzles_dict[key]))
#        print("\n")
# main3()

# end2 = perf_counter()
# print("BFS time to solve all puzzles: " + str(end2 - start2))