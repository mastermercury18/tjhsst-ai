import numpy as np
import random
import sys
import pickle
from scipy.ndimage import rotate

def activation_sigmoid(x):
    return float(1 / (1 + np.exp(-x)))
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

def p_net(A_vec, weights, biases, input):
    a = []
    a.append(input)
    n = len(weights)
    for i in range(1, n):
        a.append(A_vec(weights[i] @ a[i - 1] + biases[i]))
    return a[n - 1]

def jitter_image(image):
    image = image.reshape(28, 28)
    technique = random.choice(["no change", "up", "down", "left", "right", "rotate left", "rotate right"])
    if technique == "up":
        jittered_img = np.roll(image, -1, axis=0)
        jittered_img[-1, :] = 0
    elif technique == "down":
        jittered_img = np.roll(image, 1, axis=0)
        jittered_img[0, :] = 0
    elif technique == "left":
        jittered_img = np.roll(image, -1, axis=1)
        jittered_img[:, -1] = 0
    elif technique == "right":
        jittered_img = np.roll(image, 1, axis=1)
        jittered_img[:, 0] = 0
    elif technique == "rotate left":
        jittered_img = rotate(image, 15, reshape=False, mode='nearest')
    elif technique == "rotate right":
        jittered_img = rotate(image, -15, reshape=False, mode='nearest')
    else:
        jittered_img = image
    return jittered_img.flatten().reshape(784, 1)

test_set = []
with open("mnist_test.csv") as f:
    for line in f:
        array = line.strip().split(",")
        test_set.append(array)

train_set = []
with open("mnist_train.csv") as f:
    for line in f:
        array = line.strip().split(",")
        train_set.append(array)

training_set = []
for data in train_set:
    modified_data = data[1:]
    input_list = []
    for input in modified_data:
        input_list.append([float(input)/255])
    input_vec = np.array(input_list)
    output_lst = []
    output_index = int(data[0])
    for i in range(10):
        if i == output_index:
            output_lst.append([1])
        else:
            output_lst.append([0])
    output_vec = np.array(output_lst)
    training_set.append((input_vec, output_vec))

testing_set = []
for data in test_set:
    modified_data = data[1:]
    input_list = []
    for input in modified_data:
        input_list.append([float(input)/255])
    input_vec = np.array(input_list)
    output_lst = []
    output_index = int(data[0])
    for i in range(10):
        if i == output_index:
            output_lst.append([1])
        else:
            output_lst.append([0])
    output_vec = np.array(output_lst)
    testing_set.append((input_vec, output_vec))

layer_one_weights = np.random.uniform(-1, 1, (300, 784))
layer_two_weights = np.random.uniform(-1, 1, (100, 300))
layer_three_weights = np.random.uniform(-1, 1, (10, 100))

layer_one_bias = np.random.uniform(-1, 1, (300, 1))
layer_two_bias = np.random.uniform(-1, 1, (100, 1))
layer_three_bias = np.random.uniform(-1, 1, (10, 1))

weights = [None, layer_one_weights, layer_two_weights, layer_three_weights]
biases = [None, layer_one_bias, layer_two_bias, layer_three_bias]

dot_prods = [0, 0, 0, 0]
deltas = [0, 0, 0, 0]
a2 = [0, 0, 0, 0]

for epoch in range(12):
    for x, y in training_set:
        x_jittered = jitter_image(x)
        a2[0] = x_jittered
        for layer in range(1, 4):
            dot_prods[layer] = weights[layer] @ a2[layer - 1] + biases[layer]
            a2[layer] = new_activation_sigmoid(dot_prods[layer])
        deltas[-1] = new_activation_sigmoid_deriv(dot_prods[-1]) * (y - a2[-1])
        for layer in range(2, 0, -1):
            deltas[layer] = new_activation_sigmoid_deriv(dot_prods[layer]) * (weights[layer + 1].T @ deltas[layer + 1])
        for layer in range(1, len(deltas)):
            biases[layer] = biases[layer] + (deltas[layer] * 0.1)
            weights[layer] = weights[layer] + 0.1 * (deltas[layer] @ a2[layer - 1].T)

    with open("weights", "wb") as f:
        pickle.dump(weights, f)
    with open("biases", "wb") as f:
        pickle.dump(biases, f)

    num_wrongs = 0
    for tup in training_set:
        input, expected_output = tup
        result = p_net(new_activation_sigmoid, weights, biases, input)
        index_max_val = np.argmax(result)
        expected_index = np.argmax(expected_output)
        if index_max_val != expected_index:
            num_wrongs += 1
    print("Training set: Epoch", epoch, (num_wrongs / len(training_set)) * 100)

weights, biases = 0, 0
with open("weights", "rb") as f:
    weights = pickle.load(f)
with open("biases", "rb") as f:
    biases = pickle.load(f)

num_wrongs = 0
for tup in testing_set:
    input, expected_output = tup
    result = p_net(new_activation_sigmoid, weights, biases, input)
    index_max_val = np.argmax(result)
    expected_index = np.argmax(expected_output)
    if index_max_val != expected_index:
        num_wrongs += 1
print("Testing set: Epoch", 12, (num_wrongs / len(testing_set)) * 100)

arch = [784, 300, 100, 10]
print("Architecture", arch)
print("I used 12 epochs.")