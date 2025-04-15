from collections import deque 
from time import perf_counter
import random

def inside_out(board):
    inside_out = sorted(range(len(board)), key=lambda x:abs(x-len(board)/2))
    return inside_out

def get_next_unassigned_var(board, counter):
    # returns the row to process next according to inside out order 
    temp = inside_out(board)
    val = temp[counter]
    return val

def get_sorted_vals(board, row):
    possibles = []
    for i in range(len(board)):
        good = True
        for r, col in enumerate(board):
            if col is not None and r != row:
                # there is a conflict:
                if abs(row - r) == abs(col - i) or col == i:
                    good = False
                    break
        # okay, so we've gotten here without conflict
        if good == True:
            possibles.append(i)
    # returns the possible positions for the queen in the order we want
    returnList = []
    temp = inside_out(board)
    for c in reversed(temp):
        if c in possibles:
            returnList.append(c)
    return returnList

def goal_test(board):
    if None in board:
        return False
    return True

def csp_backtracking(state, count):
    # if all rows are filled, then we have reached our goal
    if goal_test(state): 
        return state
    # check which row to process next
    var = get_next_unassigned_var(state, count)
    # populate the row with the position of the queen 
    for val in get_sorted_vals(state, var):
        #create new_state by assigning val to var
        new_state = state.copy()
        new_state[var] = val
        # recursive call when there are conflicts 
        result = csp_backtracking(new_state, count+1)
        if result is not None:
            return result
    return None

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True

def make_initial(board):
    total_num_conflicts = 0
    for row in inside_out(board):
        conflict_dict = {}
        for i in range(len(board)):
            conflicts = 0
            for r, col in enumerate(board):
                if col is not None and r!= row:
                    if abs(row - r) == abs(col - i) or col == i:
                        conflicts += 1
            conflict_dict[i] = conflicts 
        min_val = min(conflict_dict.values())
        total_num_conflicts += min_val
        pos_keys = []
        for key in conflict_dict:
            if conflict_dict[key] == min_val:
                pos_keys.append(key)
        real_key = random.choice(pos_keys)
        board[row] = real_key
    return board

def find_queen_with_max_conflict(board):
    total_conflict_dict = {}
    for row in range(len(board)):
        i = board[row]
        conflicts = 0
        for r, col in enumerate(board):
            if col is not None and r!= row:
                if abs(row - r) == abs(col - i) or col == i:
                    conflicts += 1
        total_conflict_dict[row] = conflicts 
    max_val = max(total_conflict_dict.values())
    pos_keys = []
    for key in total_conflict_dict:
        if total_conflict_dict[key] == max_val:
            pos_keys.append(key)
    real_key = random.choice(pos_keys)
    return real_key, sum(total_conflict_dict.values())

def init_conflicts(board):
    key, confs = find_queen_with_max_conflict(board)
    return confs

def find_space_with_min_conflict(board, row):
    conflict_dict = {}
    for i in range(len(board)):
        conflicts = 0
        for r, col in enumerate(board):
            if col is not None and r!= row:
                if abs(row - r) == abs(col - i) or col == i:
                    conflicts += 1
        conflict_dict[i] = conflicts
    min_val = min(conflict_dict.values())
    pos_keys = []
    for key in conflict_dict:
        if conflict_dict[key] == min_val:
            pos_keys.append(key)
    col = random.choice(pos_keys)
    return col

def inc_repair(board):
    conflicts = -1 
    while conflicts != 0:
        row, conflicts = find_queen_with_max_conflict(board)
        print(conflicts)
        col = find_space_with_min_conflict(board, row)
        board[row] = col
    return board

start = perf_counter()

board = [None] * 100
init_board = make_initial(board)
init_confs = init_conflicts(init_board)
print("The initial flawed board is: " + str(init_board) + " it has " + str(init_confs) + " total conflicts.")
solution = inc_repair(init_board)
print("The solution to a 100 x 100 board: " + str(solution))
print(test_solution(solution))

board2 = [None] * 150
init_board2 = make_initial(board2)
init_confs2 = init_conflicts(init_board2)
print("The initial flawed board is: " + str(init_board2) + " it has " + str(init_confs2) + " total conflicts.")
solution2 = inc_repair(init_board2)
print("The solution to a 100 x 100 board: " + str(solution2))
print(test_solution(solution2))

end = perf_counter()
print("The total time to solve N-Queens using incremental repair on a 100 x 100 board and a 150 x 150 board: " + str(end - start))



