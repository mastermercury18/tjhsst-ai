from collections import deque 
import sys

possible_moves = [(3, 4, 5), (6, 7,8), (7, 8, 9), (10, 11, 12), (11, 12,13), (12,13,14), (0,1,3), (1,3,6),(3,6,10), (0, 2, 5), (2, 5, 9), (5, 9, 14), (2, 4, 7), (4, 7, 11), (5, 8, 12), (1, 4, 8), (4, 8, 13), (3,7,12)]

def create_board(hole_index):
    board = ""
    for i in range(15):
        if i == hole_index:
            board += "0"
        else:
            board += "1"
    return board

pattern = "011"
reverse = "110"

def makeMove(board, move):
    child = ""
    i,j,k = move
    temp = board[i]
    for index in range(15):
        if index == i:
            child += board[k]
        elif index == k:
            child += temp
        elif index == j:
            child += "0"
        else:
            child += board[index]
    return child

def get_children(board):
    children = []
    for move in possible_moves:
        i,j,k = move
        triple = board[i] + board[j] + board[k]
        if triple == pattern or triple == reverse:
            children.append(makeMove(board, move))
    return children

def find_goal(board, hole_index):
    solution = ""
    for i in range(15):
        if i == hole_index:
            solution += "1"
        else:
            solution += "0"
    if board == solution:
        return True
    return False

def print_nice(path):
    for board in path:
        board = "".join(board)
        idx = 0
        for row in range(1,5):
            print(' ' * (5 - row), end='')
            for j in range(row):
                print(board[idx], end=' ')
                idx += 1
            print() 
        print("\n")

def DFS_path(board,hole_index):
    fringe = deque()
    visited = set()
    fringe.append((board,[board]))
    visited.add(board)
    while fringe:
        newBoard, path = fringe.pop()
        if find_goal(newBoard,hole_index):
            print("Length is: " + str(len(path)-1))
            return print_nice(path)
        for child in get_children(newBoard):
            if child not in visited:
                fringe.append((child, path + [child]))
                visited.add(child)
    return "No solution!"

def BFS_path(board,hole_index):
    fringe = deque()
    visited = set()
    fringe.append((board,[board]))
    visited.add(board)
    while fringe:
        newBoard, path = fringe.popleft()
        if find_goal(newBoard,hole_index):
            print("Length is: " + str(len(path)-1))
            return print_nice(path)
        for child in get_children(newBoard):
            if child not in visited:
                fringe.append((child, path + [child]))
                visited.add(child)
    return "No solution!"

#hole_index = 5
hole_index = int(sys.argv[1])
DFS_path(create_board(hole_index),hole_index)
BFS_path(create_board(hole_index),hole_index)

