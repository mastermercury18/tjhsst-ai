import sys 
import ast

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
    for i in range(2 ** n):
        binary_to_output_dict[bin_list[i]] = outputs[i]
    return binary_to_output_dict
map_binary_to_output(2, 9)

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

def classify(binary_to_output_dict, weight_vector, bias):
    num_sames = 0
    for binary in binary_to_output_dict.keys():
        classification = perceptron(binary, weight_vector, bias)
        if str(classification) == str(binary_to_output_dict[binary]):
            num_sames += 1
    return num_sames / len(binary_to_output_dict.keys())

number = int(sys.argv[1])
weight_vector = ast.literal_eval(sys.argv[2])
bias = float(sys.argv[3])


binary_to_output_dict = map_binary_to_output(len(weight_vector), number)
pretty_print_tt(binary_to_output_dict)
print(classify(binary_to_output_dict, weight_vector, bias))