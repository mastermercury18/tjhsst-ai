import numpy as np 
import random
import sys

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

def p_net(weights, biases, input):
    a = []
    a.append(input)
    n = len(weights)
    for i in range(1,n):
        a.append(np.tanh(weights[i] @ a[i-1] + biases[i]))
    return a[n-1]

training_set = []
for i in range(7000):
    training_set.append(generate_time_series(51))
#print(testing_set[0])
    
testing_set = []
for i in range(2000):
    testing_set.append(generate_time_series(51))

if sys.argv[1] == "N":
    total_error = 0
    for time_series in testing_set:
        predicted = time_series[49]
        real = time_series[50]
        error = (real - predicted) ** 2
        total_error += error
    print(total_error/2000)

if sys.argv[1] == "D":

    input_output_list_testing = []
    for time_series in testing_set:
        input_list = []
        for num in time_series[:50]:
            input_list.append([num])
        input_array = np.array(input_list)
        output_array = np.array([[time_series[50]]])
        input_output_list_testing.append((input_array, output_array))

    input_output_list_training = []
    for time_series in training_set:
        input_list = []
        for num in time_series[:50]:
            input_list.append([num])
        input_array = np.array(input_list)
        output_array = np.array([[time_series[50]]])
        input_output_list_training.append((input_array, output_array))

    weights_list = []
    for i in range(50):
        weights_list.append(random.uniform(-1, 1))
    layer_one_weights = np.array([weights_list])
    weights = [None]
    weights.append(layer_one_weights)

    biases = [None]
    layer_one_bias = np.array([[random.uniform(-1, 1)]])
    biases.append(layer_one_bias)

    dot_prods = [0, 0]
    deltas = [np.array([0,0])] * 2
    a2 = [0, 0]

    def back_prop_DNN(rate, input_output_list):
        for epoch in range(100):
            for x, y in input_output_list:
                a2[0] = x
                for layer in range(1, 2):
                    dot_prods[layer] =  weights[layer] @ a2[layer - 1]  + biases[layer]
                    a2[layer] = activation_tanx(dot_prods[layer])
                deltas[-1] = activation_deriv_tanx(dot_prods[-1]) * (y - a2[-1])
                for layer in range(0, 0, -1):
                    deltas[layer] = activation_deriv_tanx(dot_prods[layer]) * ((weights[layer+1]).transpose() @ deltas[layer+1])
                for layer in range(1, len(deltas)):
                    biases[layer] = biases[layer] + (deltas[layer]* rate)
                    weights[layer] = weights[layer] + rate * (deltas[layer] @ a2[layer - 1].transpose()) 
            # total_error = 0
            # for tup in input_output_list:
            #     input, expected_output = tup
            #     result = p_net(weights, biases, input)
            #     #print(result)
            #     error = (result[0][0] - expected_output[0][0]) ** 2
            #     total_error += error
            # print(total_error/7000)

    back_prop_DNN(0.1, input_output_list_training)

    def evaluate_model(input_output_list):
        total_error = 0
        for tup in input_output_list:
            input, expected_output = tup
            result = p_net(weights, biases, input)
            error = (result[0][0] - expected_output[0][0]) ** 2
            total_error += error
        print("Testing error:", total_error / len(input_output_list))
    evaluate_model(input_output_list_testing)

#RNN

if sys.argv[1] == "R":
    training_input_output_list2 = []
    for time_series in training_set:
        input_list = time_series[:50]
        output = time_series[50]
        training_input_output_list2.append((input_list, output))
    
    testing_input_output_list2 = []
    for time_series in testing_set:
        input_list = time_series[:50]
        output = time_series[50]
        testing_input_output_list2.append((input_list, output))

    dot_prods = [0] * 50
    deltas = [0] * 50
    a1 = []
    a2 = []

    def get_deltas_wl(deltas, x):
        sum = 0
        for step in range(50):
            sum += deltas[step] * x[step]
        return sum

    def get_deltas_ws(deltas, a1):
        sum = 0
        for step in range(1, 50):
            sum += deltas[step] * a1[step - 1]
        return sum

    def back_prop(rate):
        wl2 = random.uniform(-1, 1)
        ws2 = random.uniform(-1, 1)
        b2 = random.uniform(-1, 1)
        for epoch in range(100):
            for x, y in training_input_output_list2:
                a1 = [0] * 50
                for step in range(1, 50):
                    dot_prods[step] = wl2 * x[step] + ws2 * a1[step-1] + b2
                    a1[step] = activation_tanx(dot_prods[step])
                deltas[-1] = (y - a1[-1]) * activation_deriv_tanx(dot_prods[-1])
                for step in range(48, 0, -1):
                    deltas[step] = deltas[step + 1] * ws2 * activation_deriv_tanx(dot_prods[step])
                b2 = b2 + rate * sum(deltas)
                wl2 = wl2 + rate * get_deltas_wl(deltas, x) 
                ws2 = ws2 + rate * get_deltas_ws(deltas, a1) 
            total_error = 0
            for x, y in testing_input_output_list2:
                a = [0]
                for step in range(50):
                    dot = wl2 * x[step] + ws2 * a[-1] + b2
                    a.append(activation_tanx(dot))
                result = a[-1]
                error = (y - result) ** 2
                total_error += error
            print(total_error/2000)
            
    back_prop(0.001)








