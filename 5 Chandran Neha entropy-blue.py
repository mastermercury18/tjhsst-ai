from math import log
import sys

#filename = sys.argv[1]
filename = "/Users/neha/Documents/tj/ai/data_files/house-votes-84.csv"
dataset = []
with open(filename) as f:
    for line in f:
        array = line.strip().split(",")
        dataset.append(tuple(array))

def calc_entropy(outcomes):
    outcomes_dict = {}
    for out in outcomes:
        if out not in outcomes_dict:
            outcomes_dict[out] = 1
        else:
            outcomes_dict[out] += 1
    entropy = 0
    for key in outcomes_dict:
        probability = float(outcomes_dict[key]/len(outcomes))
        information_content = log(probability, 2)
        entropy += (probability * information_content)
    return -(entropy)

def calc_total_entropy(dataset):
    outcomes = []
    counter = 0
    for observation in dataset:
        if counter != 0:
            outcomes.append(observation[len(observation)-1])
        counter += 1
    return calc_entropy(outcomes)

total_outcomes = len(dataset)
num_features = len(dataset[0]) -1
total_entropy = calc_total_entropy(dataset)
#print(total_entropy)

def calc_info_gain(dataset, feature, total_outcomes):
    dictionary = {}
    observation_dictionary = {}
    index_of_feature = dataset[0].index(feature)
    counter = 0
    for observation in dataset:
        if counter != 0:
            value = observation[index_of_feature]
            if value not in dictionary:
                observation_dictionary[value] = [observation]
                dictionary[value] = [observation[len(observation) - 1]]
            else:
                observation_dictionary[value] += [observation]
                dictionary[value] += [observation[len(observation) - 1]]
        counter += 1
    value_based_entropy = 0
    for value in dictionary:
        outcomes = dictionary[value]
        entropy = calc_entropy(outcomes)
        value_based_entropy += (entropy * (len(outcomes)/total_outcomes))
    return (total_entropy - value_based_entropy, observation_dictionary)
    
#print(calc_info_gain(dataset, "Wind", 14))

# info_gain, observation_dictionary = calc_info_gain(dataset, "Outlook", total_outcomes)
# print(observation_dictionary)


# def algorithm(data, depth):
#     max_info_gain = float('-inf')
#     max_observation_dictionary = {}
#     max_feature = ""
#     for feature in data[0][0:num_features]:
#         info_gain, observation_dictionary = calc_info_gain(data, feature, total_outcomes)
#         if info_gain > max_info_gain:
#             max_info_gain = info_gain
#             max_feature = feature
#             max_observation_dictionary = observation_dictionary
#     f.write("  " * depth + " * " + max_feature + "?" + "\n")
#     for value in max_observation_dictionary:
#         outcome = max_observation_dictionary[value][-1][-1]
#         split_dataset = []
#         split_dataset.append(dataset[0][0:num_features])
#         split_dataset += max_observation_dictionary[value]
#         if calc_total_entropy(split_dataset) == 0:
#             f.write("  " * (depth+1) + " * " + value + " --> " + outcome + "\n")
#         else:
#             f.write("  " * (depth+1) + " * " + value + "\n")
#             algorithm(split_dataset, depth+2)
#             # recur

def algorithm(trainset, data, depth):
    max_info_gain = float('-inf')
    max_observation_dictionary = {}
    max_feature = ""
    for feature in data[0][0:num_features]:
        info_gain, observation_dictionary = calc_info_gain(data, feature, total_outcomes)
        if info_gain > max_info_gain:
            max_info_gain = info_gain
            max_feature = feature
            max_observation_dictionary = observation_dictionary
    f.write("  " * depth + " * " + max_feature + "?" + "\n")
    for value in max_observation_dictionary:
        outcome = max_observation_dictionary[value][-1][-1]
        split_dataset = []
        split_dataset.append(trainset[0][0:num_features])
        split_dataset += max_observation_dictionary[value]
        if calc_total_entropy(split_dataset) == 0:
            f.write("  " * (depth+1) + " * " + value + " --> " + outcome + "\n")
        else:
            f.write("  " * (depth+1) + " * " + value + "\n")
            algorithm(trainset, split_dataset, depth+2)
            # recur

print(dataset)
f = open("tempout.txt", "w")
algorithm(dataset, dataset, 0)
f.close()
    


