import matplotlib.pyplot as plt

def convert_to_binary(x):
    return bin(x).replace("0b", "")

def activation(x):
    if x <= 0:
        return 0
    else:
        return 1

def truth_table(n):
    num_inputs = 2 ** n 
    input_list = []
    for i in range(num_inputs - 1,-1,-1):
        binary = convert_to_binary(i)
        if len(binary) < n:
            difference = n - len(binary)
            binary = ("0" * difference) + binary
        input_tuple = ()
        for digit in binary:
            input_tuple += (int(digit),)
        input_list.append(input_tuple)
    return input_list
truth_table(3)

def map_binary_to_output(n, number):
    binary_to_output_dict = {}
    bin_list = truth_table(n)
    outputs = convert_to_binary(number)
    if len(outputs) < (2 ** n):
        difference = (2 ** n) - len(outputs)
        outputs = ("0" * difference) + outputs
    for i in range(2 ** n):
        binary_to_output_dict[bin_list[i]] = outputs[i]
    return binary_to_output_dict
#print(map_binary_to_output(2, 112))

def pretty_print_tt(binary_to_output_dict):
    n = len(list(binary_to_output_dict.keys())[0])
    for i in range(n): print("I" + str(i+1) + " ", end = '')
    print("  |  out")
    for i in range(n+2): print(" - ", end = '')
    print("\n")
    for key in binary_to_output_dict.keys():
        str_key = ""
        for digit in key:
            str_key += str(digit) + "  "
        print(str_key + "  |  " + binary_to_output_dict[key])

    
def perceptron(input_vector, weight_vector, bias):
    dot_prod = 0
    for i in range(len(input_vector)):
        dot_prod += input_vector[i] * weight_vector[i]
    dot_prod += bias 
    return activation(dot_prod)

def train_perceptron(num_epochs, binary_to_output_dict, n_bits):
    weight = ()
    for i in range(n_bits):
        weight += (0, )
    bias = 0
    saved_weight = weight
    saved_bias = bias 
    for epoch in range(num_epochs):
        for x in binary_to_output_dict.keys():
            f_star = perceptron(x, weight, bias)
            difference = (int(binary_to_output_dict[x]) - f_star) 
            new_weight = ()
            for i in range(n_bits):
                vect_i = difference * x[i]
                new_elem = weight[i] + vect_i
                new_weight += (new_elem, )
            weight = new_weight
            bias = bias + difference 
        if weight == saved_weight and bias == saved_bias:
            break
        else:
            saved_weight = weight
            saved_bias = bias 
    return (saved_weight, saved_bias)

#binary_to_output_dict = {(1,1): '0', (1,0): '0', (0,1): '0', (0,0): '1'}
#print(train_perceptron(10, binary_to_output_dict))

def every_truth_table(n_bits):
    canonical_range = 2 ** (2 ** n_bits)
    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    axes = axes.flatten()
    
    for index, number in enumerate(range(canonical_range)):
        
        binary_to_output_dict = map_binary_to_output(n_bits, number)
        weight_vector, bias = train_perceptron(100, binary_to_output_dict, n_bits)

        ax = axes[index]
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.grid(True)
        ax.set_title(f'Truth Table {number}')

        for i in range(-20, 21):
            for j in range(-20, 21):
                x = float(i / 10)
                y = float(j / 10)
                input = (x, y)
                output = perceptron(input, weight_vector, bias)
                color = 'red' if output == 0 else 'green'
                ax.plot(x, y, marker="o", markersize=1, color=color)

        for input_vec in binary_to_output_dict.keys():
            output = binary_to_output_dict[input_vec]
            x, y = input_vec
            color = 'red' if output == '0' else 'green'
            ax.plot(x, y, 'o', markersize=5, color=color)
    plt.tight_layout()
    plt.show()

every_truth_table(2)
