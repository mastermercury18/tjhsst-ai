import sys
import itertools
from itertools import product
import random
import ast 

# part 1
q_val_dict = {}
size = 4
for state in range(size ** 2):
    q_val_dict[state] = 0
    
def create_all_q_values_round1(grid_length, possible_moves, size, q_val_dict, goal_states):
    total_q_val_list = []
    for state in range(grid_length):
        if state not in goal_states:
            q_val_list_per_square = []
            for move in possible_moves:
                if move == "left" and state % size != 0:
                    new_pos = state - 1 
                    temp = -1 + q_val_dict[new_pos]
                    q_val_list_per_square.append(temp)
                elif move == "right" and state % size != size -1:
                    new_pos = state+1
                    temp = -1 + q_val_dict[new_pos]
                    q_val_list_per_square.append(temp)
                elif move == "up" and state + 1 > size:
                    new_pos = state - size
                    temp = -1 + q_val_dict[new_pos]
                    q_val_list_per_square.append(temp)
                elif move == "down" and grid_length - state > size:
                    new_pos = state + size
                    temp = -1 + q_val_dict[new_pos]
                    q_val_list_per_square.append(temp)
            q_val_dict[state] = max(q_val_list_per_square)
            total_q_val_list.append(q_val_dict[state])
    return total_q_val_list

# part 2

q_val_dict = {}
size = 4
for state in range(size ** 2):
    q_val_dict[state] = 0
    
def create_all_q_values_round2(grid_length, possible_moves, size, q_val_dict, goal_states, quicksand):
    total_q_val_list = []
    for state in range(grid_length):
        if state not in goal_states:
            q_val_list_per_square = []
            for move in possible_moves:
                if move == "left" and state % size != 0:
                    new_pos = state - 1 
                    if state in quicksand:
                        temp = -100 + q_val_dict[new_pos]
                    else:
                        temp = -1 + q_val_dict[new_pos]
                    q_val_list_per_square.append(temp)
                elif move == "right" and state % size != size -1:
                    new_pos = state+1
                    if state in quicksand:
                        temp = -100 + q_val_dict[new_pos]
                    else:
                        temp = -1 + q_val_dict[new_pos]
                    q_val_list_per_square.append(temp)
                elif move == "up" and state + 1 > size:
                    new_pos = state - size
                    if state in quicksand:
                        temp = -100 + q_val_dict[new_pos]
                    else:
                        temp = -1 + q_val_dict[new_pos]
                    q_val_list_per_square.append(temp)
                elif move == "down" and grid_length - state > size:
                    new_pos = state + size
                    if state in quicksand:
                        temp = -100 + q_val_dict[new_pos]
                    else:
                        temp = -1 + q_val_dict[new_pos]
                    q_val_list_per_square.append(temp)
            q_val_dict[state] = max(q_val_list_per_square)
            total_q_val_list.append(q_val_dict[state])
    return total_q_val_list

# part 3
    
def generate_boolean_states(length):
    return list(product([False, True], repeat=length))
    
def make_q_val_dict(magic_list, size):
    length = len(magic_list)
    bool_list = (False, ) * length
    length = len(magic_list)
    q_val_dict = {}
    all_boolean_combinations = generate_boolean_states(length)
    for state in range(0, size ** 2):
        for bool_list in all_boolean_combinations:
            q_val_dict[(state, bool_list)] = 0
    return q_val_dict
    
def create_all_q_values_round3(grid_length, possible_moves, size, q_val_dict, goal_states, quicksand, num_magic, magic_list):
    total_q_val_list = []
    count = 0
    for state, curr_bool_list in q_val_dict:
        count += 1
        if state not in goal_states:
            q_val_list_per_square = []
            if state in magic_list:
                index = magic_list.index(state)
                list_bool_list = list(curr_bool_list)
                list_bool_list[index] = True
                curr_bool_list = tuple(list_bool_list)
            
            for move in possible_moves:
                if move == "left" and state % size != 0:
                    new_pos = state - 1                        
                elif move == "right" and state % size != size - 1:
                    new_pos = state + 1
                elif move == "up" and state >= size:
                    new_pos = state - size
                elif move == "down" and state + size < grid_length:
                    new_pos = state + size
                else:
                    continue
                
                if new_pos in magic_list:
                    index = magic_list.index(new_pos)
                    list_bool_list = list(curr_bool_list)
                    list_bool_list[index] = True
                    new_bool_list = tuple(list_bool_list)
                else:
                    new_bool_list = curr_bool_list

                if new_pos in goal_states:
                    if curr_bool_list.count(True) >= num_magic:
                        if state in quicksand:
                            temp = -100 + q_val_dict[(new_pos, new_bool_list)]
                        else:
                            temp = -1 + q_val_dict[(new_pos, new_bool_list)]
                    else:
                        temp = -10000000000
                else:
                    if state in quicksand:
                        temp = -100 + q_val_dict[(new_pos, new_bool_list)]
                    else:
                        temp = -1 + q_val_dict[(new_pos, new_bool_list)]                
                q_val_list_per_square.append(temp)

            q_val_dict[(state, curr_bool_list)] = max(q_val_list_per_square)
            total_q_val_list.append(q_val_dict[(state, curr_bool_list)])
    return total_q_val_list

# part 4

def generate_boolean_states(length):
    return list(product([False, True], repeat=length))
    
def make_q_val_dict(magic_list, size):
    length = len(magic_list)
    bool_list = (False, ) * length
    length = len(magic_list)
    q_val_dict = {}
    all_boolean_combinations = generate_boolean_states(length)
    for state in range(0, size ** 2):
        for bool_list in all_boolean_combinations:
            q_val_dict[(state, bool_list)] = 0
    return q_val_dict

def get_warp_list(warps):
    warp_list = []
    for warp in warps:
        warp_list.append(warp[0])
    return warp_list
    
def create_all_q_values_round4(grid_length, possible_moves, size, q_val_dict, goal_states, quicksand, num_magic, magic_list, warps):
    total_q_val_list = []
    count = 0
    warp_list = get_warp_list(warps)
    for state, curr_bool_list in q_val_dict:
        count += 1
        if state not in goal_states:
            q_val_list_per_square = []

            if state in magic_list:
                index = magic_list.index(state)
                list_bool_list = list(curr_bool_list)
                list_bool_list[index] = True
                curr_bool_list = tuple(list_bool_list)
            
            for move in possible_moves:
                if move == "left" and state % size != 0:
                    new_pos = state - 1                        
                elif move == "right" and state % size != size - 1:
                    new_pos = state + 1
                elif move == "up" and state >= size:
                    new_pos = state - size
                elif move == "down" and state + size < grid_length:
                    new_pos = state + size
                else:
                    continue
                
                if new_pos in magic_list:
                    index = magic_list.index(new_pos)
                    list_bool_list = list(curr_bool_list)
                    list_bool_list[index] = True
                    new_bool_list = tuple(list_bool_list)
                else:
                    new_bool_list = curr_bool_list

                if new_pos in warp_list:
                    warp = warps[warp_list.index(new_pos)]
                    prob = warp[2]
                    tunneled_new_pos = warp[1]
                    if tunneled_new_pos in magic_list:
                        index = magic_list.index(tunneled_new_pos)
                        list_bool_list = list(curr_bool_list)
                        list_bool_list[index] = True
                        tunnel_bool_list = tuple(list_bool_list)
                    else:
                        tunnel_bool_list = curr_bool_list

                if new_pos in goal_states:
                    if curr_bool_list.count(True) >= num_magic:
                        if state in quicksand:
                            if new_pos in warp_list:
                                temp = -100 + (prob * q_val_dict[(tunneled_new_pos, tunnel_bool_list)] + (1-prob) * q_val_dict[(new_pos, new_bool_list)])
                            else:
                                temp = -100 + q_val_dict[(new_pos, new_bool_list)]
                        else:
                            if new_pos in warp_list:
                                temp = -1 + (prob * q_val_dict[(tunneled_new_pos, tunnel_bool_list)] + (1-prob) * q_val_dict[(new_pos, new_bool_list)])
                            else:
                                temp = -1 + q_val_dict[(new_pos, new_bool_list)]
                    else:
                        if new_pos in warp_list:
                            temp = -10000000000
                        else:
                            temp = -10000000000
                else:
                    if state in quicksand:
                        if new_pos in warp_list:
                            temp = -100 + (prob * q_val_dict[(tunneled_new_pos, tunnel_bool_list)] + (1-prob) * q_val_dict[(new_pos, new_bool_list)])
                        else:
                            temp = -100 + q_val_dict[(new_pos, new_bool_list)]
                    else:
                        if new_pos in warp_list:
                            temp = -1 + (prob * q_val_dict[(tunneled_new_pos, tunnel_bool_list)] + (1-prob) * q_val_dict[(new_pos, new_bool_list)])
                        else:
                            temp = -1 + q_val_dict[(new_pos, new_bool_list)]                
                q_val_list_per_square.append(temp)

            q_val_dict[(state, curr_bool_list)] = max(q_val_list_per_square)
            total_q_val_list.append(q_val_dict[(state, curr_bool_list)])
    return total_q_val_list

size = int(sys.argv[1])
goal_squares = ast.literal_eval(sys.argv[2])
quicksand_pits = ast.literal_eval(sys.argv[3])
num_magic = int(sys.argv[4])
magic_list = ast.literal_eval(sys.argv[5])
warps = ast.literal_eval(sys.argv[6])

if num_magic == 0 and magic_list == [] and quicksand_pits == [] and warps == []:
    total_q_val_list = create_all_q_values_round1(size ** 2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares)
    new_total_q_val_list = ["b"]
    while total_q_val_list != new_total_q_val_list:
        new_total_q_val_list = create_all_q_values_round1(size ** 2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares)
        total_q_val_list = create_all_q_values_round1(size ** 2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares)
    print_list = []
    for key in q_val_dict:
        print_list.append(q_val_dict[key])
elif num_magic == 0 and magic_list == [] and warps == []:
    total_q_val_list = create_all_q_values_round2(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits)
    new_total_q_val_list = ["b"]
    while total_q_val_list != new_total_q_val_list:
        new_total_q_val_list = create_all_q_values_round2(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits)
        total_q_val_list = create_all_q_values_round2(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits)
    print_list = []
    for key in q_val_dict:
        print_list.append(q_val_dict[key])
elif num_magic > 0 and len(magic_list) > 0 and warps == []:
    q_val_dict = make_q_val_dict(magic_list, size)
    total_q_val_list = create_all_q_values_round3(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits, num_magic, magic_list)
    new_q_val_list = ["b"]
    while new_q_val_list != total_q_val_list:
        new_q_val_list = create_all_q_values_round3(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits, num_magic, magic_list)
        total_q_val_list = create_all_q_values_round3(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits, num_magic, magic_list)
    print_list = []
    for state in range(0, size**2):
        key = (state, (False,) * len(magic_list))
        if key[0] in magic_list:
            temp_bool = (False,) * len(magic_list)
            index = magic_list.index(key[0])
            list_bool_list = list(temp_bool)
            list_bool_list[index] = True
            true_bool = tuple(list_bool_list)
            print_list.append(q_val_dict[(state, true_bool)])
        elif key in q_val_dict:
            print_list.append(q_val_dict[key])
elif len(warps) > 0:
    q_val_dict = make_q_val_dict(magic_list, size)
    total_q_val_list = create_all_q_values_round4(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits, num_magic, magic_list, warps)
    new_q_val_list = ["b"]
    while new_q_val_list != total_q_val_list:
        new_q_val_list = create_all_q_values_round4(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits, num_magic, magic_list, warps)
        total_q_val_list = create_all_q_values_round4(size**2, ["left", "right", "up", "down"], size, q_val_dict, goal_squares, quicksand_pits, num_magic, magic_list, warps)
    print_list = []
    for state in range(0, size**2):
        key = (state, (False,) * len(magic_list))
        if key[0] in magic_list:
            temp_bool = (False,) * len(magic_list)
            index = magic_list.index(key[0])
            list_bool_list = list(temp_bool)
            list_bool_list[index] = True
            true_bool = tuple(list_bool_list)
            print_list.append(q_val_dict[(state, true_bool)])
        elif key in q_val_dict:
            print_list.append(q_val_dict[key])
final_list = []
for q_val in print_list:
    if q_val == 0:
        final_list.append("x")
    else:
        final_list.append(q_val)
for i in range(size):
    for j in range(size):
        print(final_list[i * size + j], end=' ')
    print()