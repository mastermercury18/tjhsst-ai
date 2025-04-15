import sys 

sys.setrecursionlimit(10000)

def partial_a_x(pair):
    x, y = pair
    return 8 * x - 3 * y + 24

def partial_a_y(pair):
    x, y = pair
    return -3 * x + 4 * y - 20

def partial_b_x(pair):
    x, y = pair
    return 2 * (x - y ** 2)

def partial_b_y(pair):
    x, y = pair
    #return -2 * (1 - y) - 4 * y * (x - y ** 2)
    return 2 * (-2 * x * y + 2 * y ** 3 + y - 1)

def gradient_a(pair):
    return (partial_a_x(pair), partial_a_y(pair))

def gradient_b(pair):
    return (partial_b_x(pair), partial_b_y(pair))

def gradient_descent_a(pair, rate):
    x, y = pair
    gradient_x = partial_a_x(pair)
    gradient_y = partial_a_y(pair)
    print("Location: " + str(pair))
    print("Gradient: " + str((gradient_x, gradient_y)))
    print("\n")
    if (gradient_x ** 2 + gradient_y ** 2) ** 0.5  < 10 ** -8:
        print("Reached.")
    else:
        new_x = x - rate * partial_a_x(pair) 
        new_y = y - rate * partial_a_y(pair)
        new_pair = (new_x, new_y)
        gradient_descent_a(new_pair, rate)
#gradient_descent_a((0,0), 0.01)

def gradient_descent_b(pair, rate):
    x, y = pair
    gradient_x = partial_b_x(pair)
    gradient_y = partial_b_y(pair)
    print("Location: " + str(pair))
    print("Gradient: " + str((gradient_x, gradient_y)))
    print("\n")
    if (gradient_x ** 2 + gradient_y ** 2) ** 0.5  < 10 ** -8:
        print("Reached.")
    else:
        new_x = x - rate * gradient_x 
        new_y = y - rate * gradient_y
        new_pair = (new_x, new_y)
        gradient_descent_b(new_pair, rate)
#gradient_descent_b((0,0), 0.01)

if sys.argv[1] == "A":
    gradient_descent_a((0,0), 0.01)
if sys.argv[1] == "B":
    gradient_descent_b((0,0), 0.01)