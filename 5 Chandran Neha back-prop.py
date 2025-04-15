import numpy as np 
import random
import sys 
import ast

def activation_sigmoid(x):
    return float(1/(1 + np.exp(-x)))
new_activation_sigmoid = np.vectorize(activation_sigmoid)

def activation_sigmoid_deriv(x):
    return activation_sigmoid(x) * (1 - activation_sigmoid(x))
new_activation_sigmoid_deriv = np.vectorize(activation_sigmoid_deriv)

def activation_step(x):
    if x <= 0.5:
        return 0
    else:
        return 1
new_activation_step = np.vectorize(activation_step)

layer_one_weights = np.array([[1, 1], [-0.5, 0.5]])
layer_one_bias = np.array([[1], [-1]])
layer_two_weights = np.array([[1,-1], [2, -2]])
layer_two_bias = np.array([[-0.5], [0.5]])
weights = [None, layer_one_weights, layer_two_weights]
biases = [None, layer_one_bias, layer_two_bias]

def p_net(A_vec, weights, biases, input):
    a = []
    a.append(input)
    n = len(weights)
    for i in range(1,n):
        a.append(A_vec(weights[i] @ a[i-1] + biases[i]))
    return a[n-1]

def error(output_vec, a):
    return 0.5 *np.linalg.norm(output_vec - a)**2

# output = p_net(new_activation, weights, biases, input_vec)
# a_5 = output[0][0]
# a_6 = output[1][0]
# y_5 = 0.8
# y_6 = 1
# error = 0.5 * ((y_5 - a_5) ** 2 + (y_6 - a_6) ** 2)

# input_vec = np.array([[2], [3]])
# output_vec = np.array([[0.8], [1]])
# dot_prods = [0, 0, 0]
# deltas = [0, 0, 0]
# a = [0, 0, 0]


# def back_prop(rate):
#     for epoch in range(2):
#         a[0] = input_vec
#         for layer in range(1, 3):
#             dot_prods[layer] =  weights[layer]@ a[layer - 1]  + biases[layer]
#             a[layer] = new_activation_sigmoid(dot_prods[layer])
#         print(error(output_vec, a[-1]))
#         deltas[-1] = new_activation_sigmoid_deriv(dot_prods[-1]) * (output_vec - a[-1])
#         for layer in range(1, 0, -1):
#             deltas[layer] = new_activation_sigmoid_deriv(dot_prods[layer]) * ((weights[layer+1]).transpose() @ deltas[layer+1])
#         for layer in range(1, len(deltas)):
#             biases[layer] = biases[layer] + (deltas[layer]* rate)
#             weights[layer] = weights[layer] + rate * (deltas[layer] @ a[layer - 1].transpose())
#     print(output_vec)
#     print("last: " + str(error(output_vec, a[-1])))
# back_prop(0.1)


if sys.argv[1] == "S":
    layer_one_random_weight = np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]])
    layer_two_random_weight = np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]])
    weights = [None, layer_one_random_weight, layer_two_random_weight]
    layer_one_bias = np.array([[random.uniform(-1, 1)], [random.uniform(-1, 1)]])
    layer_two_bias =  np.array([[random.uniform(-1, 1)], [random.uniform(-1, 1)]])
    biases = [None, layer_one_bias, layer_two_bias]

    input_one = np.array([[0], [0]])
    input_two = np.array([[0], [1]])
    input_three = np.array([[1], [0]])
    input_four = np.array([[1], [1]])

    output_one = np.array([[0], [0]])
    output_two = np.array([[0], [1]])
    output_three = np.array([[0], [1]])
    output_four = np.array([[1], [0]])

    dot_prods = [0, 0, 0]
    deltas = [np.array([0,0])] * 3
    a2 = [0, 0, 0]

    input_output_list = [(input_one, output_one), (input_two, output_two), (input_three, output_three), (input_four, output_four)]

    def back_prop_chall_two(rate):
        for epoch in range(2000):
            for x, y in input_output_list:
                a2[0] = x
                for layer in range(1, 3):
                    dot_prods[layer] =  weights[layer]@ a2[layer - 1]  + biases[layer]
                    a2[layer] = new_activation_sigmoid(dot_prods[layer])
                deltas[-1] = new_activation_sigmoid_deriv(dot_prods[-1]) * (y - a2[-1])
                for layer in range(1, 0, -1):
                    deltas[layer] = new_activation_sigmoid_deriv(dot_prods[layer]) * ((weights[layer+1]).transpose() @ deltas[layer+1])
                for layer in range(1, len(deltas)):
                    biases[layer] = biases[layer] + (deltas[layer]* rate)
                    weights[layer] = weights[layer] + rate * (deltas[layer] @ a2[layer - 1].transpose()) 
    back_prop_chall_two(0.1)

    for tup in input_output_list:
        input, output = tup
        result = p_net(new_activation_sigmoid, weights, biases, input)
        result = new_activation_step(result)
        print(result)

if sys.argv[1] == "C":
    # layer_one_weights = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
    # layer_one_bias = np.array([[1], [1], [1], [1]])
    # layer_two_weights = np.array([[1, 1, 1, 1]])
    # layer_two_bias = np.array([[-2.77]])
    
    layer_one_weights = np.array([[np.random.uniform(-1, 1), np.random.uniform(-1, 1)], [np.random.uniform(-1, 1), np.random.uniform(-1, 1)], [np.random.uniform(-1, 1), np.random.uniform(-1, 1)], [np.random.uniform(-1, 1), np.random.uniform(-1, 1)]])
    layer_one_bias = np.array([[np.random.uniform(-1, 1)], [np.random.uniform(-1, 1)], [np.random.uniform(-1, 1)], [np.random.uniform(-1, 1)]])
    layer_two_weights = np.array([[np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(-1, 1)]])
    layer_two_bias = np.array([[np.random.uniform(-1, 1)]])

    weights = []
    weights.append(None)
    weights.append(layer_one_weights)
    weights.append(layer_two_weights)
    biases = []
    biases.append(None)
    biases.append(layer_one_bias)
    biases.append(layer_two_bias)

    dot_prods = [0, 0, 0]
    deltas = [np.array([0,0])] * 3
    a2 = [0, 0, 0]

    training_set = []
    with open("10000_pairs.txt") as f:
        for line in f:
            arr = line.strip().split()
            input = np.array([[float(arr[0])], [float(arr[1])]])
            if (input[0] ** 2 + input[1] ** 2) ** 1/2 < 1:
                expected_output = np.array([[1]])
            else:
                expected_output = np.array([[0]])
            training_set.append((input, expected_output))

    def back_prop_chall_three(rate):
        for epoch in range(300):
            for x, y in training_set:
                a2[0] = x
                for layer in range(1, 3):
                    dot_prods[layer] =  weights[layer] @ a2[layer - 1]  + biases[layer]
                    a2[layer] = new_activation_sigmoid(dot_prods[layer])
                deltas[-1] = new_activation_sigmoid_deriv(dot_prods[-1]) * (y - a2[-1])
                for layer in range(1, 0, -1):
                    deltas[layer] = new_activation_sigmoid_deriv(dot_prods[layer]) * ((weights[layer+1]).transpose() @ deltas[layer+1])
                for layer in range(1, len(deltas)):
                    biases[layer] = biases[layer] + (deltas[layer]* rate)
                    weights[layer] = weights[layer] + rate * (deltas[layer] @ a2[layer - 1].transpose()) 
            num_wrongs = 0
            counter = 0
            for tup in training_set:
                input, expected_output = tup
                result = p_net(new_activation_sigmoid, weights, biases, input)
                result = round(float(result[0][0]))
                if result != int(expected_output[0][0]):
                    num_wrongs += 1
            print(num_wrongs)
    back_prop_chall_three(0.1)
            





    # back_prop(0.3)
