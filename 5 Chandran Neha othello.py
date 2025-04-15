import sys
def game_over(board):
    if not "." in board:
        return True
    return False

def min_step(board, depth, alpha, beta):
    pos_moves = possible_moves(board, "o")
    results = []
    if depth == 0 or game_over(board):
        return score(board)
    if len(pos_moves) == 0:
        return max_step(board, depth-1, alpha, beta)
    for move in pos_moves:
        new_board = make_move(board, "o", move)
        max_step_stored = max_step(new_board, depth-1, alpha, beta)
        #Alpha Beta Pruning Here
        if max_step_stored < beta:
            beta = max_step_stored
        results.append(max_step_stored)
        if beta <= alpha:
            break
    return min(results)

def max_step(board, depth, alpha, beta):
    pos_moves = possible_moves(board, "x")
    results = []
    if depth == 0 or game_over(board):
        return score(board)
    if len(pos_moves) == 0:
        return min_step(board, depth-1, alpha, beta)
    for move in pos_moves:
        new_board = make_move(board, "x", move)
        min_step_stored = min_step(new_board, depth-1, alpha, beta)
        #Alpha Beta Pruning Here
        if min_step_stored > alpha:
            alpha = min_step_stored
        results.append(min_step_stored)
        if beta <= alpha:
            break

    return max(results)

# def score(board):
#     moves_num = 0
#     score = 0
#     x_token_count = 0
#     o_token_count = 0
#     x_pos_moves = len(possible_moves(board, "x"))
#     o_pos_moves = len(possible_moves(board, "o"))

#     #idx_of_next_to_corners = [12,17,21, 22, 27, 72,77,28,71,78,82,87]
#     #idx_of_edges = [12,13,14,15,16,17,18,31,41,51,61,83,84,85,86, 68,58,48,38]
#     idx_of_edges = [11, 12, 13, 14, 15, 16, 17, 18, 21, 31, 41, 51, 61, 71, 81, 82, 83, 84, 85, 86, 87, 88, 28, 38, 48, 58, 68, 78]

#     dict1 = {11:{12,21,22}, 
#              18:{17, 27, 28},
#             81: {71, 72, 82}, 
#             88: {78, 77, 87} }
#     corners = [11, 18, 81, 88]
#     x_corner_count = 0
#     o_corner_count = 0
#     associated_corner = 0
#     for each_space in range(len(board)):
#         if board[each_space] == "x":
#             x_token_count +=1
#             moves_num +=1
#         elif board[each_space] == "o":
#             o_token_count += 1
#             moves_num +=1

#         if each_space in corners:
#             if board[each_space] == "x":
#                 score += 9999999 #corners 7
#             elif board[each_space] == "o":
#                 score -= 9999999

#         if each_space == 12 or each_space ==21 or each_space == 22:
#             associated_corner = 11
#             if board[each_space] == "x":
#               if board[associated_corner] == "o":
#                   score -= 999999 #adjecent 5
#               elif board[associated_corner] == ".":
#                   score -= 9999
#               elif board[associated_corner] == "x":
#                   score += 99999
#             if board[each_space] == "o":
#               if board[associated_corner] == "x":
#                   score += 999999
#               elif board[associated_corner] == ".":
#                   score += 9999
#               elif board[associated_corner] == "o":
#                   score -= 99999
#         elif each_space == 17 or each_space == 27 or each_space == 28:
#             associated_corner == 18
#             if board[each_space] == "x":
#               if board[associated_corner] == "o":
#                   score -= 999999 #adjecent 5
#               elif board[associated_corner] == ".":
#                   score -= 9999
#               elif board[associated_corner] == "x":
#                   score += 99999
#             if board[each_space] == "o":
#               if board[associated_corner] == "x":
#                   score += 999999
#               elif board[associated_corner] == ".":
#                   score += 9999
#               elif board[associated_corner] == "o":
#                   score -= 99999
#         elif each_space == 71 or each_space == 72 or each_space == 82:
#             associated_corner = 81
#             if board[each_space] == "x":
#               if board[associated_corner] == "o":
#                   score -= 999999 #adjecent 5
#               elif board[associated_corner] == ".":
#                   score -= 9999
#               elif board[associated_corner] == "x":
#                   score += 99999
#             if board[each_space] == "o":
#               if board[associated_corner] == "x":
#                   score += 999999
#               elif board[associated_corner] == ".":
#                   score += 9999
#               elif board[associated_corner] == "o":
#                   score -= 99999
#         elif each_space == 78 or each_space == 77 or each_space == 87:
#             associated_corner = 88
#             if board[each_space] == "x":
#               if board[associated_corner] == "o":
#                   score -= 999999 #adjecent 5
#               elif board[associated_corner] == ".":
#                   score -= 9999
#               elif board[associated_corner] == "x":
#                   score += 99999
#             if board[each_space] == "o":
#               if board[associated_corner] == "x":
#                   score += 999999
#               elif board[associated_corner] == ".":
#                   score += 9999
#               elif board[associated_corner] == "o":
#                   score -= 99999

        

#         elif each_space in idx_of_edges:
#             if board[each_space] == "x":
#                 score += 999999
#             elif board[each_space] == "o":
#                 score -= 999999

#     #mobility            
#     if moves_num <= 25:
#         if x_pos_moves < o_pos_moves:
#             score -= 999999999 #mobility 9
#         elif o_pos_moves < x_pos_moves:
#             score += 999999999
#         elif x_pos_moves == o_pos_moves:
#             score = 0
#         if x_token_count> o_token_count:
#             score -= 999999 #early game penalty
#         elif o_token_count > x_token_count:
#             score+= 99999
#         if o_corner_count > x_corner_count:
#             score -= 9999999
#         elif x_corner_count < o_corner_count:
#             score += 9999999
#     elif moves_num == 64:
#         if x_token_count > o_token_count:
#             if x_token_count >= 60:
#                 score += 99999999999999999999
#             else:
#                 score += 999999999999
#         elif o_token_count> x_token_count:
#             if o_token_count >= 60:
#                 score -= 99999999999999999999
#             else:
#                 score -= 999999999999
#         if x_token_count == o_token_count:
#             score = 0
#     else: #mid_game
#         if x_token_count > o_token_count:
#             score +=999999999999
#         if o_token_count > x_token_count:
#             score -=999999999999

#     return score

def is_early_game(board):
    if board.count(".") >= 48:
        return True
    
def score(board):
    score = 0
    x_count = len(possible_moves(board, "x"))
    o_count = len(possible_moves(board, "o"))
    penalty = 0

    corners = [11, 18, 81, 88]
    edges = [11, 12, 13, 14, 15, 16, 17, 18, 21, 31, 41, 51, 61, 71, 81, 82, 83, 84, 85, 86, 87, 88, 28, 38, 48, 58, 68, 78]
    near_corners_dict = {11: (12, 21, 22), 18: (17, 27, 28), 81: (71, 72, 82), 88: (87, 77, 78)}

   
    if is_early_game(board):
        penalty = 5 * (board.count("x") - board.count("o"))


    for i in range(len(board)):
        if i in corners:
            if board[i] == "x":
                score += 1000
            if board[i] == "o":
                score -= 1000
        if i in edges:
            if board[i] == "x":
                score += 100
            if board[i] == "o":
                score -= 100

        if i in near_corners_dict[11]:
            if board[11] == "." and board[i] == "x":
                score -= 1000
            if board[11] == "." and board[i] == "o":
                score += 1000
        elif i in near_corners_dict[18]:
            if board[18] == "." and board[i] == "x":
                score -= 1000
            if board[18] == "." and board[i] == "o":
                score += 1000
        elif i in near_corners_dict[81]:
            if board[81] == "." and board[i] == "x":
                score -= 1000
            if board[81] == "." and board[i] == "o":
                score += 1000
        elif i in near_corners_dict[88]:
            if board[88] == "." and board[i] == "x":
                score -= 1000
            if board[88] == "." and board[i] == "o":
                score += 1000

    mobility = (x_count - o_count)
    score += mobility
    score -= penalty
    return score


def possible_moves(board, player_token):
    if player_token == "x":
        enemy_token = "o"
    else:
        enemy_token = "x"
    directions = [-1, 1, -10, 10, -11, 11, -9, 9]
    pos_moves = []
    for i in range(len(board)):
        if board[i] == ".":
            for dir in directions:
                newIndex = i + dir
                if board[newIndex] == enemy_token:
                    while board[newIndex] == enemy_token:
                        newIndex = newIndex + dir
                    if board[newIndex] == player_token:
                        pos_moves.append(i)
                        break
    return pos_moves

def make_move(board, player_token, index):
    directions = [-1, 1, -10, 10, -11, 11, -9, 9]
    if player_token == "x":
        enemy_token = "o"
    else:
        enemy_token = "x"
    for dir in directions:
        newIndex = index + dir
        processed_indices = []
        if board[newIndex] == enemy_token:
            while board[newIndex] == enemy_token:
                processed_indices.append(newIndex)
                newIndex = newIndex + dir
            if board[newIndex] == player_token:
                processed_indices
                for x in processed_indices:
                    board = board[:x] + player_token + board[x+1:]

    board = board[:index] + player_token + board[index+1:]
    return board

def find_next_move(board, player, depth):
   best_move = []
   for each_pos in possible_moves(board, player):
        new_board = make_move(board, player, each_pos)
        if player == "x":
            num = min_step(new_board, depth-1, float('-inf'), float('inf'))
            best_move.append([num, each_pos])
        else:
            num = max_step(new_board, depth-1, float('-inf'), float('inf'))
            best_move.append([num, each_pos])
   if player == "x":
       idx = max(best_move)
       num, index_of_move = idx
       return index_of_move
   else:
       idx = min(best_move)
       num, index_of_move = idx
       return index_of_move 

board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
   print(find_next_move(board, player, depth))
   depth += 1

# class Strategy():
#    logging = True  # Optional; see below
#    uses_10x10_board = True  # If you delete this line, the server will give you a 64-character 8x8 board instead
#    uses_10x10_moves = True  # If you delete this line, the server will expect indices on an 8x8 board instead
#    def best_strategy(self, board, player, best_move, still_running):
#        depth = 1
#        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
#            best_move.value = find_next_move(board, player, depth)
#            depth += 1
# import sys 

# directions = [-1, 1, -10, 10, -11, 11, -9, 9]

# def possible_moves(board, player_token):
#     if player_token == "x":
#         enemy_token = "o"
#     elif player_token == "o":
#         enemy_token = "x"
#     pos_moves = []
#     for i in range(len(board)):
#         if board[i] == ".":
#             for dir in directions:
#                 newInd = i + dir
#                 if board[newInd] == enemy_token:
#                     while board[newInd] == enemy_token:
#                         newInd = newInd + dir
#                     if board[newInd] == player_token:
#                         pos_moves.append(i)
#                         break
#     return pos_moves

# def make_move(board, player_token, index):
#     if player_token == "x":
#         enemy_token = "o"
#     elif player_token == "o":
#         enemy_token = "x"
#     for dir in directions:
#         indices_processed = []
#         newInd = index + dir
#         if newInd >= 0 and newInd < len(board) and board[newInd] == enemy_token:
#             while board[newInd] == enemy_token:
#                 indices_processed.append(newInd)
#                 newInd = newInd + dir
#             if board[newInd] == player_token:
#                 # flip every enemy token in indices_processed 
#                 for i in indices_processed:
#                     board = board[:i] + player_token + board[i+1:]
#     board = board[:index] + player_token + board[index+1:]
#     return board

# def game_over(board):
#     for char in board:
#         if char == ".":
#             return False
#     return True

# def is_early_game(board):
#     if board.count(".") >= 48:
#         return True

# def score(board):
#     score = 0
#     x_count = len(possible_moves(board, "x"))
#     o_count = len(possible_moves(board, "o"))
#     penalty = 0

#     corners = [11, 18, 81, 88]
#     edges = [11, 12, 13, 14, 15, 16, 17, 18, 21, 31, 41, 51, 61, 71, 81, 82, 83, 84, 85, 86, 87, 88, 28, 38, 48, 58, 68, 78]
#     near_corners_dict = {11: (12, 21, 22), 18: (17, 27, 28), 81: (71, 72, 82), 88: (87, 77, 78)}

   
#     if is_early_game(board):
#         penalty = 5 * (board.count("x") - board.count("o"))


#     for i in range(len(board)):
#         if i in corners:
#             if board[i] == "x":
#                 score += 1000
#             if board[i] == "o":
#                 score -= 1000
#         if i in edges:
#             if board[i] == "x":
#                 score += 100
#             if board[i] == "o":
#                 score -= 100

#         if i in near_corners_dict[11]:
#             if board[11] == "." and board[i] == "x":
#                 score -= 1000
#             if board[11] == "." and board[i] == "o":
#                 score += 1000
#         elif i in near_corners_dict[18]:
#             if board[18] == "." and board[i] == "x":
#                 score -= 1000
#             if board[18] == "." and board[i] == "o":
#                 score += 1000
#         elif i in near_corners_dict[81]:
#             if board[81] == "." and board[i] == "x":
#                 score -= 1000
#             if board[81] == "." and board[i] == "o":
#                 score += 1000
#         elif i in near_corners_dict[88]:
#             if board[88] == "." and board[i] == "x":
#                 score -= 1000
#             if board[88] == "." and board[i] == "o":
#                 score += 1000

#     mobility = (x_count - o_count)
#     score += mobility
#     score -= penalty
#     return score

# def possible_next_boards(board, current_player):
#     possibles = []
#     new_board = board
#     for i in range(len(new_board)):
#         pos_move = make_move(new_board, current_player, i)
#         possibles.append(pos_move)
#     return possibles

# def max_step(board, depth, alpha, beta):
#     results = []
#     if depth == 0 or game_over(board):
#         return score(board)
#     if len(possible_moves(board, "x")) == 0:
#         return min_step(board, depth - 1)
#     for move in possible_moves(board, "x"):
#         new_board = make_move(board, "x", move)
#         min_step1 = min_step(new_board, depth - 1, alpha, beta)
#         if min_step1 > alpha:
#             alpha = min_step1
#         results.append(min_step1)
#         if beta <= alpha:
#             break
#     return max(results)

# def min_step(board, depth, alpha, beta):
#     results = []
#     if depth == 0 or game_over(board):
#         return score(board)
#     if len(possible_moves(board, "o")) == 0:
#         return max_step(board, depth - 1)
#     for move in possible_moves(board, "o"):
#         new_board = make_move(board, "o", move)
#         max_step1 = max_step(new_board, depth - 1, alpha, beta)
#         if max_step1 < beta:
#             beta = max_step1
#         results.append(max_step1)
#         if beta <= alpha:
#             break
#     return min(results)

# # def min_step(board, depth, alpha, beta):
# #     pos_moves = possible_moves(board, "o")
# #     results = []
# #     if depth == 0 or game_over(board):
# #         return score(board)
# #     if len(pos_moves) == 0:
# #         return max_step(board, depth-1, alpha, beta)
# #     for move in pos_moves:
# #         new_board = make_move(board, "o", move)
# #         max_step_stored = max_step(new_board, depth-1, alpha, beta)
# #         #Alpha Beta Pruning Here
# #         if max_step_stored < beta:
# #             beta = max_step_stored
# #         results.append(max_step_stored)
# #         if beta <= alpha:
# #             break
# #     return min(results)

# # def max_step(board, depth, alpha, beta):
# #     pos_moves = possible_moves(board, "x")
# #     results = []
# #     if depth == 0 or game_over(board):
# #         return score(board)
# #     if len(pos_moves) == 0:
# #         return min_step(board, depth-1, alpha, beta)
# #     for move in pos_moves:
# #         new_board = make_move(board, "x", move)
# #         min_step_stored = min_step(new_board, depth-1, alpha, beta)
# #         #Alpha Beta Pruning Here
# #         if min_step_stored > alpha:
# #             alpha = min_step_stored
# #         results.append(min_step_stored)
# #         if beta <= alpha:
# #             break

# #     return max(results)

# def find_next_move(board, player, depth):
#     if player == "x":
#         best_score = float('-inf')
#         best_move = None
#         for move in possible_moves(board, player):
#             new_board = make_move(board, player, move)
#             score = min_step(new_board, depth-1, float("-inf"), float("inf"))

#             if score > best_score:
#                 best_score = score
#                 best_move = move
#     else:
#         best_score = float('inf')
#         best_move = None

#         for move in possible_moves(board, player):
#             new_board = make_move(board, player, move)
#             score = max_step(new_board, depth-1, float("-inf"), float("inf"))

#             if score < best_score:
#                 best_score = score
#                 best_move = move
#     return best_move

# class Strategy():

#    logging = True  # Optional

#    uses_10x10_board = True  # If you delete this line, the server will give you a 64-character 8x8 board instead

#    uses_10x10_moves = True  # If you delete this line, the server will expect indices on an 8x8 board instead

#    def best_strategy(self, board, player, best_move, still_running):

#        depth = 1

#        for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
#             temp = find_next_move(board, player, depth)
#             best_move.value = find_next_move(board, player, depth)
#             depth += 1

# #print(find_next_move("???????????........??........??........??...ox...??...xo...??........??........??........???????????", "x", 1))
# if __name__ == "__main__":

#     board = sys.argv[1]

#     player = sys.argv[2]

#     depth = 1

#     for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all

#         print(find_next_move(board, player, depth))

#         depth += 1
