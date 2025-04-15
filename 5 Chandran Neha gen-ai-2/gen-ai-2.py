import numpy as np
import random
import math
import pickle

def activation_tanx(x):
    return np.tanh(x)

def activation_deriv_tanx(x):
    return 1/(np.cosh(x) ** 2)

def softmax(dot, t):
    temp = np.exp(dot/t)
    a_N_F = temp / np.sum(temp)
    return a_N_F

# training_set = []
# testing_set = []
# with open("/Users/neha/Documents/tj/ai/data_files/shakespeare.txt") as f:
#     big_string = ""
#     for line in f:
#         line = line.lower()
#         big_string += line 
#     for i in range(len(big_string) - 21):
#         temp = big_string[i:i+21]
#         input = temp[:20]
#         output = temp[20]
#         if random.random() < 0.18:
#             testing_set.append((input, output))
#         else:
#             training_set.append((input, output))

# character_to_frequency_dict = {}
# character_to_one_hot_dict = {}
# for char in big_string:
#     if char not in character_to_frequency_dict.keys():
#         character_to_frequency_dict[char] = big_string.count(char)

# sorted_char_freq = dict(sorted(character_to_frequency_dict.items(), key=lambda item: item[1], reverse = True))

# with open("training-gen-ai.pkl", "wb") as f:
#     pickle.dump(training_set, f)
# with open("testing-gen-ai.pkl", "wb") as f:
#     pickle.dump(testing_set, f)
# with open("sorted-dict-gen-ai.pkl", "wb") as f:
#     pickle.dump(sorted_char_freq, f)

with open("training-gen-ai-small.pkl", "rb") as f:
    training_set = pickle.load(f)
with open("testing-gen-ai-small.pkl", "rb") as f:
    testing_set = pickle.load(f)
with open("sorted-dict-gen-ai-small.pkl", "rb") as f:
    sorted_char_freq = pickle.load(f)

def one_hot_vector(char):
    sorted_characters = list(sorted_char_freq.keys())
    one_hot_list = []
    for character in sorted_characters:
        if character == char:
            one_hot_list.append([1])
        else:
            one_hot_list.append([0])
    one_hot_vec = np.array(one_hot_list)
    return one_hot_vec

def create_all_one_hot_vecs(x):
    total_list = []
    for char in x:
        total_list.append(one_hot_vector(char))
    return total_list

def make_one_hot_dict(sorted_char_freq):
    letter_to_one_hot_dict = {}
    for char in sorted_char_freq:
        letter_to_one_hot_dict[char] = one_hot_vector(char)
    return letter_to_one_hot_dict

N = 4
F = 21

dot_prods = []
for row in range(N):
    row_list = []
    for col in range(F):
        row_list.append([0])
    dot_prods.append(row_list)

deltas = []
for row in range(N):
    row_list = []
    for col in range(F):
        row_list.append([0])
    deltas.append(row_list)

a1 = []
for row in range(N):
    row_list = []
    for col in range(F):
        row_list.append([0])
    a1.append(row_list)

def sum_deltas(layer, deltas):
    sum = 0
    for step in range(1, F):
        sum += deltas[layer][step]
    return sum

def get_deltas_wl(layer, a1, deltas):
    sum = 0
    for step in range(1, F):
        sum += (deltas[layer][step] @ a1[layer-1][step].T)
    return sum

def get_deltas_ws(layer, a1, deltas):
    sum = 0
    for step in range(2, F):
        sum += (deltas[layer][step] @ a1[layer][step-1].T)
    return sum

def back_prop(rate):

    temp1 =(39+40)/2
    temp2= (40+40)/2
    temp3 = (40+39)/2
    r1 = math.sqrt(3/temp1)
    r2 = math.sqrt(3/temp2)
    r3 = math.sqrt(3/temp3)

    Wl1 = np.random.uniform(-r1, r1, (40, 39))
    Ws1 = np.random.uniform(-r1, r1, (40, 40))
    b1 = np.random.uniform(-r1, r1, (40, 1))

    Wl2 = np.random.uniform(-r2, r2, (40, 40))
    Ws2 = np.random.uniform(-r2, r2, (40, 40))
    b2 = np.random.uniform(-r2, r2, (40, 1))

    Wl3 = np.random.uniform(-r3, r3, (39, 40))
    b3 = np.random.uniform(-r3, r3, (39, 1))

    weights_layer = [None, Wl1, Wl2, Wl3]
    weights_step = [None, Ws1, Ws2]
    biases = [None, b1, b2, b3]

    for epoch in range(1):
        counter = 0
        for x, y in training_set:
            x = create_all_one_hot_vecs(x)
            y = create_all_one_hot_vecs(y)[0]
            for layer in range(1, N):
                a1[layer][0] = np.zeros((len(weights_layer[layer]), 1))
            for step in range(1, F):
                a1[0][step] = x[step-1]
                for layer in range(1, N):
                    if layer == N-1 and step == F-1:
                        dot_prods[layer][step] = weights_layer[layer] @ a1[layer-1][step] + biases[layer]
                        a1[layer][step] = softmax(dot_prods[layer][step])
                    else:
                        if layer < N-1: 
                            dot_prods[layer][step] = weights_layer[layer] @ a1[layer-1][step] + weights_step[layer] @ a1[layer][step-1] + biases[layer]
                            a1[layer][step] = activation_tanx(dot_prods[layer][step])
            deltas[-1][-1] = (np.eye(y.shape[0]) + (-1 * a1[-1][-1])) @ y
            
            for step in range(F-2, 0, -1):
                deltas[-1][step] = deltas[-1][-1] # for a DNN we just save the last recorded step 
            for layer in range(N-2, 0, -1):
                deltas[layer][-1] =  activation_deriv_tanx(dot_prods[layer][-1]) * ((weights_layer[layer + 1]).transpose() @ deltas[layer + 1][-1])
            for step in range(F-2, 0, -1):
                for layer in range(N-2, 0, -1):
                    deltas[layer][step] = activation_deriv_tanx(dot_prods[layer][step]) * (weights_step[layer].T @ deltas[layer][step + 1]) + activation_deriv_tanx(dot_prods[layer][step]) * (weights_layer[layer + 1].T @ deltas[layer + 1][step])
            for layer in range(1, N):
                biases[layer] = biases[layer] + rate * sum_deltas(layer, deltas)
                weights_layer[layer] = weights_layer[layer] + (rate * get_deltas_wl(layer, a1, deltas))
                if layer < N-1:
                    weights_step[layer] = weights_step[layer] + (rate * get_deltas_ws(layer, a1, deltas))

            counter += 1
            if counter % 10000 == 0:
                with open("weights-step-gen-ai" + str(counter) + ".pkl", "wb") as f:
                    pickle.dump(weights_step, f)
                with open("weights-layer-gen-ai" + str(counter) + ".pkl", "wb") as f:
                    pickle.dump(weights_layer, f)
                with open("biases-gen-ai" + str(counter) + ".pkl", "wb") as f:
                    pickle.dump(biases, f)

                a2 = []
                for row in range(N):
                    row_list = []
                    for col in range(F):
                        row_list.append([0])
                    a2.append(row_list)

                cce_total = 0
                for x, y in testing_set:
                    x = create_all_one_hot_vecs(x)
                    y = create_all_one_hot_vecs(y)[0]
                    for layer in range(1, N):
                        a2[layer][0] = np.zeros((len(weights_layer[layer]), 1))
                    for step in range(1, F):
                        a2[0][step] = np.array(x[step-1])
                        for layer in range(1, N):
                            if layer == N-1 and step == F-1:
                                dot_prods[layer][step] = weights_layer[layer] @ a2[layer-1][step] + biases[layer]
                                a2[layer][step] = softmax(dot_prods[layer][step])
                            else:
                                if layer < N-1: 
                                    dot_prods[layer][step] = weights_layer[layer] @ a2[layer-1][step] + weights_step[layer] @ a2[layer][step-1] + biases[layer]
                                    a2[layer][step] = activation_tanx(dot_prods[layer][step])

                    result = a2[-1][-1]
                    cce = 0
                    for i in range(len(result)):
                        cce_temp = (y[i][0]) * math.log(result[i][0])
                        cce += cce_temp
                    cce *= -1
                    cce_total += cce
                print(cce_total/len(testing_set))
#back_prop(0.001)

# 10,000 data points

with open("weights-step-gen-ai-small10000.pkl", "rb") as f:
    weights_step = pickle.load(f)
with open("weights-layer-gen-ai-small10000.pkl", "rb") as f:
    weights_layer = pickle.load(f)
with open("biases-gen-ai-small10000.pkl", "rb") as f:
    biases = pickle.load(f)

deltas = []
for row in range(N):
    row_list = []
    for col in range(F):
        row_list.append([0])
    deltas.append(row_list)

seed = "t"

while len(seed) < 400:
    x = create_all_one_hot_vecs(seed)
    a2 = []
    for row in range(N):
        row_list = []
        for col in range(len(seed) +1):
            row_list.append([0])
        a2.append(row_list)
    for layer in range(1, N):
        a2[layer][0] = np.zeros((len(weights_layer[layer]), 1))
    for step in range(1, len(seed) + 1):
        a2[0][step] = x[step-1]
        for layer in range(1, N):
            if layer == N-1 and step == len(seed):
                dot_prod = weights_layer[layer] @ a2[layer-1][step] + biases[layer]
                a2[layer][step] = softmax(dot_prod, 0.7)
            else:
                if layer < N-1: 
                    dot_prod = weights_layer[layer] @ a2[layer-1][step] + weights_step[layer] @ a2[layer][step-1] + biases[layer]
                    a2[layer][step] = activation_tanx(dot_prod)                        

    result = a2[-1][-1]
    sorted_characters = list(sorted_char_freq.keys())
    probabilities = [result[i][0] for i in range(len(result))]
    next_char = random.choices(sorted_characters, weights=probabilities, k=1)[0]
    seed += next_char
    x.append(one_hot_vector(next_char))
    x.pop(0)
print("Generated text for 10,000 data points:")
print(seed)
print("\n")

#100,000 data points

with open("weights-step-gen-ai-small100000.pkl", "rb") as f:
    weights_step = pickle.load(f)
with open("weights-layer-gen-ai-small100000.pkl", "rb") as f:
    weights_layer = pickle.load(f)
with open("biases-gen-ai-small100000.pkl", "rb") as f:
    biases = pickle.load(f)

deltas = []
for row in range(N):
    row_list = []
    for col in range(F):
        row_list.append([0])
    deltas.append(row_list)

seed = "t"

while len(seed) < 400:
    x = create_all_one_hot_vecs(seed)
    a2 = []
    for row in range(N):
        row_list = []
        for col in range(len(seed) +1):
            row_list.append([0])
        a2.append(row_list)
    for layer in range(1, N):
        a2[layer][0] = np.zeros((len(weights_layer[layer]), 1))
    for step in range(1, len(seed) + 1):
        a2[0][step] = x[step-1]
        for layer in range(1, N):
            if layer == N-1 and step == len(seed):
                dot_prod = weights_layer[layer] @ a2[layer-1][step] + biases[layer]
                a2[layer][step] = softmax(dot_prod, 0.7)
            else:
                if layer < N-1: 
                    dot_prod = weights_layer[layer] @ a2[layer-1][step] + weights_step[layer] @ a2[layer][step-1] + biases[layer]
                    a2[layer][step] = activation_tanx(dot_prod)                        

    result = a2[-1][-1]
    sorted_characters = list(sorted_char_freq.keys())
    probabilities = [result[i][0] for i in range(len(result))]
    next_char = random.choices(sorted_characters, weights=probabilities, k=1)[0]
    seed += next_char
    x.append(one_hot_vector(next_char))
    x.pop(0)
print("Generated text for 100,000 data points:")
print(seed)
print("\n")


# 400,000 data points

with open("weights-step-gen-ai-small400000.pkl", "rb") as f:
    weights_step = pickle.load(f)
with open("weights-layer-gen-ai-small400000.pkl", "rb") as f:
    weights_layer = pickle.load(f)
with open("biases-gen-ai-small400000.pkl", "rb") as f:
    biases = pickle.load(f)

deltas = []
for row in range(N):
    row_list = []
    for col in range(F):
        row_list.append([0])
    deltas.append(row_list)

seed = "t"

while len(seed) < 400:
    x = create_all_one_hot_vecs(seed)
    a2 = []
    for row in range(N):
        row_list = []
        for col in range(len(seed) +1):
            row_list.append([0])
        a2.append(row_list)
    for layer in range(1, N):
        a2[layer][0] = np.zeros((len(weights_layer[layer]), 1))
    for step in range(1, len(seed) + 1):
        a2[0][step] = x[step-1]
        for layer in range(1, N):
            if layer == N-1 and step == len(seed):
                dot_prod = weights_layer[layer] @ a2[layer-1][step] + biases[layer]
                a2[layer][step] = softmax(dot_prod, 0.7)
            else:
                if layer < N-1: 
                    dot_prod = weights_layer[layer] @ a2[layer-1][step] + weights_step[layer] @ a2[layer][step-1] + biases[layer]
                    a2[layer][step] = activation_tanx(dot_prod)                        

    result = a2[-1][-1]
    sorted_characters = list(sorted_char_freq.keys())
    probabilities = [result[i][0] for i in range(len(result))]
    next_char = random.choices(sorted_characters, weights=probabilities, k=1)[0]
    seed += next_char
    x.append(one_hot_vector(next_char))
    x.pop(0)
print("Generated text for 400,000 data points:")
print(seed)
print("\n")
