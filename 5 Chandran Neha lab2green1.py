from collections import deque 
from time import perf_counter

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

#print(csp_backtracking([None, None, None, None, None, None, None, None, None,None], 0))
mylist = 33*[None]
start = perf_counter()
state = csp_backtracking(mylist,0)
end = perf_counter()
total_time = end - start

mylisttwo = 51*[None]
start2 = perf_counter()
state_two = csp_backtracking(mylisttwo,0)
end2 = perf_counter()
total_time_two = end2 - start2
print("For a 33 x 33 sized board, the solution state is: " + str(state) + " the algorithm solved it in " + str(total_time) + " seconds.")
print("For a 35 x 35 sized board, the solution state is: " + str(state_two) + " the algorithm solved it in " + str(total_time_two) + " seconds.")

print("33x33 is verified: " + str(test_solution(state)))
print("35x35 is verified: " + str(test_solution(state_two)))