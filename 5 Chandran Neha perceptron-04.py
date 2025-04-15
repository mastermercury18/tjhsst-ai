import numpy as np 
import sys 
import ast

def activation(x):
    if x <= 0:
        return 0
    else:
        return 1
new_activation = np.vectorize(activation)

def p_net(A_vec, weights, biases, input):
    a = []
    a.append(input)
    n = 2
    for i in range(0,n):
        a.append(A_vec(weights[i] @ a[i] + biases[i]))
    return a[n]

#XOR HAPPENS HERE
if len(sys.argv) == 2:
    print('in')
    layer_one_weights = np.array([[1, 1], [1, 1]])
    layer_one_bias = np.array([[-1], [0]])
    layer_two_weights = np.array([[-1, 1]])
    layer_two_bias = 0
    weights = [layer_one_weights, layer_two_weights]
    biases = [layer_one_bias, layer_two_bias]
    input = ast.literal_eval(sys.argv[1])
    input_vec = np.array([[int(input[0])], [int(input[1])]])
    print(input_vec)
    output = p_net(new_activation, weights, biases, input_vec)
    print(output)

# input = ast.literal_eval(sys.argv[1])
# print(p_net(input))

# diamond challenge 
if len(sys.argv) == 3:
    layer_one_weights = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
    layer_one_bias = np.array([[1], [1], [1], [1]])
    layer_two_weights = np.array([[1, 1, 1, 1]])
    layer_two_bias = np.array([[-3]])
    weights = []
    weights.append(layer_one_weights)
    weights.append(layer_two_weights)
    biases = []
    biases.append(layer_one_bias)
    biases.append(layer_two_bias)
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    input_vec = np.array([[x], [y]])
    output = p_net(new_activation, weights, biases, input_vec)
    if output[0][0] == 1:
        print("The point is inside the diamond.")
    else:
        print("The point is outside the diamond.")

# circle challenge
    
def activation_sigmoid(x):
    return float(1/(1 + np.exp(-x)))
new_activation_sigmoid = np.vectorize(activation_sigmoid)

if len(sys.argv) == 1:
    layer_one_weights = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
    layer_one_bias = np.array([[1], [1], [1], [1]])
    layer_two_weights = np.array([[1, 1, 1, 1]])
    layer_two_bias = np.array([[-2.77]])
    weights = []
    weights.append(layer_one_weights)
    weights.append(layer_two_weights)
    biases = []
    biases.append(layer_one_bias)
    biases.append(layer_two_bias)
    #input_vec = np.array([[-0.5], [-0.5]])

    #input_vec = ast.literal_eval(sys.argv[1])
    num_trues = 0
    counter = 0
    for x in range(-100, 100):
        for y in range(-100, 100):
            x = float(x/100)
            y = float(y/100)
            #print((x, y))
            input_vec = np.array([[x], [y]])
            output = p_net(new_activation_sigmoid, weights, biases, input_vec)
            output = round(output[0][0])
            if (x ** 2 + y ** 2) ** 1/2 < 1:
                expected_output = 1
            else:
                expected_output = 0
            if output == expected_output:
                num_trues += 1
            else:
                print(input_vec)
            counter += 1
    print(num_trues/counter)



