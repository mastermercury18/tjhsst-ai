import numpy as np
import random
import math

def generate_time_series(n_steps):
    freq1, freq2, offsets1, offsets2 = np.random.rand(4)
    time = np.linspace(0, 1, n_steps)
    series = 0.5 * np.sin((time - offsets1) * (freq1 * 10 + 10))
    series += 0.2 * np.sin((time - offsets2) * (freq2 * 20 + 20))
    series += 0.1 * (np.random.rand(n_steps) - 0.5)
    return series

def activation_tanx(x):
    return np.tanh(x)

def activation_deriv_tanx(x):
    return 1/(np.cosh(x) ** 2)

training_set = []
for i in range(7000):
    training_set.append(generate_time_series(51))

testing_set = []
for i in range(2000):
    testing_set.append(generate_time_series(51))

input_output_list2_training = []
for series in training_set:
    inputList = []
    for num in range(0, len(series)-1):
        inputList.append([series[num]])
    inputVec = np.array(inputList)
    outputList = [series[50]]
    outputVec = np.array([outputList])
    data = [inputVec, outputVec]
    input_output_list2_training.append(data)

input_output_list2 = []
for series in testing_set:
    inputList = []
    for num in range(0, len(series)-1):
        inputList.append([series[num]])
    inputVec = np.array(inputList)
    outputList = [series[50]]
    outputVec = np.array([outputList])
    data = [inputVec, outputVec]
    input_output_list2.append(data)

dot_prods = []
for row in range(3):
    row_list = []
    for col in range(51):
        row_list.append([0])
    dot_prods.append(row_list)

deltas = []
for row in range(3):
    row_list = []
    for col in range(51):
        row_list.append([0])
    deltas.append(row_list)

a1 = []
for row in range(3):
    row_list = []
    for col in range(51):
        row_list.append([0])
    a1.append(row_list)
    

def sum_deltas(layer, deltas):
    sum = 0
    for step in range(1, 51):
        sum += deltas[layer][step]
    return sum

def get_deltas_wl(layer, a1, deltas):
    sum = 0
    for step in range(1, 51):
        #print(deltas)
        #print(deltas[layer][step])
        sum += (deltas[layer][step] @ a1[layer-1][step].T)
    return sum

def get_deltas_ws(layer, a1, deltas):
    sum = 0
    for step in range(2, 51):
        sum += (deltas[layer][step] @ a1[layer][step-1].T)
    return sum

def back_prop(rate):
    1 - 6 - 1
    temp1 = (1 + 12)/2
    temp2 = (6 + 2)/2
    r1 = math.sqrt(3/temp1)
    r2 = math.sqrt(3/temp2)
    wl1 = np.random.uniform(-r1, r1, (6, 1))
    ws1 = np.random.uniform(-r1, r1, (6, 6))
    b1 = np.random.uniform(-r1, r1, (6, 1))

    wl2 = np.random.uniform(-r2, r2, (1, 6))
    ws2 = np.random.uniform(-r2, r2, (1, 1))
    b2 = np.random.uniform(-r2, r2, (1, 1))

    weights_layer = [None, wl1, wl2]
    weights_step = [None, ws1, ws2]
    biases= [None, b1, b2]

    for epoch in range(100):
        for x, y in input_output_list2_training:
            for layer in range(1, 3):
                a1[layer][0] = np.zeros((len(weights_step[layer]), 1))
            for step in range(1, 51):
                a1[0][step] = np.array([x[step-1]])
                for layer in range(1, 3):
                    dot_prods[layer][step] = weights_layer[layer] @ a1[layer-1][step] + weights_step[layer] @ a1[layer][step-1] + biases[layer]
                    a1[layer][step] = activation_tanx(dot_prods[layer][step])
            deltas[-1][-1] = activation_deriv_tanx(dot_prods[-1][-1]) * (y - a1[-1][-1])
            for step in range(49, 0, -1):
                deltas[-1][step] = activation_deriv_tanx(dot_prods[-1][step]) * ((weights_step[-1]).transpose() @ deltas[-1][step + 1])
            for layer in range(1, 0, -1):
                deltas[layer][-1] =  activation_deriv_tanx(dot_prods[layer][-1]) * ((weights_layer[layer + 1]).transpose() @ deltas[layer + 1][-1])
            for step in range(49, 0, -1):
                for layer in range(1, 0, -1):
                    deltas[layer][step] = activation_deriv_tanx(dot_prods[layer][step]) * (weights_step[layer].T @ deltas[layer][step + 1]) + activation_deriv_tanx(dot_prods[layer][step]) * (weights_layer[layer + 1].T @ deltas[layer + 1][step])
            for layer in range(1, 3):
                biases[layer] = biases[layer] + rate * sum_deltas(layer, deltas)
                weights_layer[layer] = weights_layer[layer] + (rate * get_deltas_wl(layer, a1, deltas))
                weights_step[layer] = weights_step[layer] + (rate * get_deltas_ws(layer, a1, deltas))
        total_error = 0
        #a = [[np.zeros((6, 1)) for _ in range(51)] for _ in range(3)]
        a = []
        for row in range(3):
            row_list = []
            for col in range(51):
                row_list.append([0])
            a.append(row_list)
        for x, y in input_output_list2:
            for layer in range(1, 3):
                a[layer][0] = np.zeros((len(weights_step[layer]), 1))
            for step in range(1, 51):
                a[0][step] = np.array([x[step-1]])
                for layer in range(1, 3):
                    dot = weights_layer[layer] @ a[layer-1][step] + weights_step[layer] @ a[layer][step-1] + biases[layer]
                    a[layer][step] = activation_tanx(dot)
            result = a[-1][-1]
            error = (y - result) ** 2
            total_error += error
        print(total_error/2000)
        
back_prop(0.01)