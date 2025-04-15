import sys 
import ast

def activation(x):
    if x <= 0:
        return 0
    else:
        return 1
    
def perceptron(input_vector, weight_vector, bias):
    dot_prod = 0
    for i in range(len(input_vector)):
        dot_prod += input_vector[i] * weight_vector[i]
    dot_prod += bias 
    return activation(dot_prod)

def main(input):
    w_1_3 = (1, 1)
    b3 = -1
    w_1_4 = (1,1)
    b4 = 0
    w_5 = (-1,1)
    b5 = 0
    w_3_5 = perceptron(input, w_1_3, b3)
    w_4_5 = perceptron(input, w_1_4, b4)
    output = perceptron((w_3_5, w_4_5), w_5, b5)
    return output 

input = ast.literal_eval(sys.argv[1])
print(main(input))
