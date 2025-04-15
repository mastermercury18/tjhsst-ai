from collections import deque 
from time import perf_counter
import sys

start = perf_counter()
#word_file = sys.argv[1]
#puzzle_file = sys.argv[2]

word_file = "words_06_letters.txt"
puzzle_file = "puzzles_normal.txt"

with open(word_file) as f:
    wordset = set([line.strip() for line in f])
puzzles_dict = {}

alpha = "abcdefghijklmnopqrstuvwxyz"

def get_children(word):
    myset = set()
    for i, char in enumerate(word):
        for letter in alpha:
            if letter != char:
                child = word[:i] + letter + word[i+1:]
                if child in wordset:
                    myset.add(child)
    return myset

def create_child_dict():
    child_dict = {}
    for word in wordset:
       child_dict[word] = get_children(word)
    return child_dict

child_dict = create_child_dict()

end = perf_counter()

print("Time it took to create data structure: " + str(end - start))

start = perf_counter()
with open(puzzle_file) as f:
    for line in f:
        arr = line.split()
        puzzles_dict[arr[0]] = arr[1]

def bi_BFS(line,goal):
    fringe_source = deque()
    visited_source = set()
    fringe_source.append((line,[line]))
    visited_source.add(line)
    source_dict = {}
    #source_dict[line] = line

    fringe_goal = deque()
    visited_goal = set()
    fringe_goal.append((goal,[goal]))
    visited_goal.add(goal)
    goal_dict = {}
    #goal_dict[goal] = goal

    while fringe_source and fringe_goal:
        newLine1, path1 = fringe_source.popleft()
        newLine2, path2 = fringe_goal.popleft()

        for child in child_dict[newLine1]:
            if child not in visited_source:
                fringe_source.append((child, path1 + [child]))
                visited_source.add(child)
                source_dict[child] = path1
                if newLine1 in visited_goal:
                    print("Length is: " + str(len(path1 + goal_dict[newLine1])))
                    return "\n".join(path1 + goal_dict[newLine1])
                    #return path1 + goal_dict[newLine1]
                
        for child2 in child_dict[newLine2]:
            if child2 not in visited_goal:
                fringe_goal.append((child2, [child2] + path2))
                visited_goal.add(child2)
                goal_dict[child2] = path2
                if newLine2 in visited_source:
                    print("Length is: " + str(len(source_dict[newLine2] + path2)))
                    return "\n".join(source_dict[newLine2] + path2)
                    #return source_dict[newLine2] + path2

def BFS_path(word,goal):
    fringe = deque()
    visited = set()
    fringe.append((word,[word]))
    visited.add(word)
    while fringe:
        newWord, path = fringe.popleft()
        if newWord == goal:
            print("Length is: " + str(len(path)))
            return "\n".join(path)
        for child in child_dict[newWord]:
            if child not in visited:
                fringe.append((child, path + [child]))
                visited.add(child)
    return "No solution!"

def main():
    line_num = 0
    for key in puzzles_dict:
       print("Line: " + str(line_num))
       line_num += 1
       #print(BFS_path(key, puzzles_dict[key]))
       print(bi_BFS(key, puzzles_dict[key]))
       print("\n")
main()

end = perf_counter()
print("Time to solve all puzzles: " + str(end - start))

start = perf_counter()
bigset = set()
def BFS(word):
    fringe = deque()
    visited = set()
    fringe.append((word,0))
    visited.add(word)
    bigset.add(word)
    while fringe:
        newWord, steps = fringe.popleft()
        for child in child_dict[newWord]:
            if child not in visited:
                fringe.append((child, steps+1))
                visited.add(child)
                bigset.add(child)
    return visited

def BFS_steps(word):
    fringe = deque()
    visited = set()
    steps_dict = {}
    fringe.append((word,1))
    visited.add(word)
    while fringe:
        newWord, steps = fringe.popleft()
        steps_dict[newWord] = steps
        for child in child_dict[newWord]:
            if child not in visited:
                fringe.append((child, steps + 1))
                visited.add(child)
    return steps_dict

def count_singletons():
    singletons = 0
    tempbool = True
    for word in wordset:
        for child in child_dict[word]:
            if child in wordset:
                tempbool = False
        if tempbool == True:
            singletons += 1
        tempbool = True
    return singletons
print("1) There are " + str(count_singletons()) + " singletons.")

bigset = set()
clumplist = []

def largest_clump_and_count():
    max_len = 0
    for word in wordset:
        if word not in bigset:
            clump = BFS(word)
            if len(clump) > max_len:
                max_len = len(clump)
            if len(clump) > 1:
                clumplist.append(clump)
    return max_len, len(clumplist)

largest_size, clump_count = largest_clump_and_count()
print("2) The biggest subcomponent has " + str(largest_size) + " words.")
print("3) There are " + str(clump_count) + " 'clumps' (subgraphs with at least two words).")


def longest_path():
    maxval = 0
    max_start = ""
    max_end = ""
    for clump in clumplist:
        source = list(clump)[1]
        steps_dict = BFS_steps(source)
        farthest_node = max(steps_dict, key = steps_dict.get)

        steps_dict = BFS_steps(farthest_node)
        temp_max = max(steps_dict.values())
        farthest_node_two = max(steps_dict, key = steps_dict.get)

        if temp_max > maxval:
            maxval = temp_max
            max_start = farthest_node
            max_end = farthest_node_two
        
    print(BFS_path(max_start, max_end))
longest_path()

end = perf_counter()
print("Time for brain teasers: " + str(end - start))


