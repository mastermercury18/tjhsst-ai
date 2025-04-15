import random
from math import log
import sys

population_size = 500
mutation_rate = 0.8
tournament_size = 20
num_clones = 1
crossover_locs = 5
win_prob = 0.75

freq_dict = {}
with open("ngrams.txt") as f:
    for line in f:
        splt = line.split()
        freq_dict[splt[0]] = splt[1]

#alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpha = "EARIOTNSLCUDPMHGBFYWKVXZJQ"

def decode(message, cipher):
    new_message = ""
    for letter in message:
        #if letter == " " or letter == "," or letter == "." or letter == "!" or letter == "-" or letter == "":
        if letter not in alpha:
            new_message += letter
        else:
            index = cipher.index(letter)
            new_letter = alpha[index]
            new_message += new_letter
    return new_message

def fitness(decoded):
    sum_score = 0
    for i in range(len(decoded)-2):
        subs = decoded[i:i+3]
        if subs in freq_dict.keys():
            freq = int(freq_dict[subs])
            score = log(freq, 2)
            sum_score += score
    return sum_score

ciph_and_fitness_dict = {}
def calculate_all_fitness(population, message):
    for ciph in population: 
        decoded = decode(message, ciph)
        ciph_and_fitness_dict[ciph] = fitness(decoded)

def breed(cipher1, cipher2):
    parent1 = random.choice([cipher1, cipher2])
    if parent1 == cipher1:
        parent2 = cipher2
    else:
        parent2 = cipher1
    child = [None] * len(cipher1)
    for i in range(crossover_locs):
        index = random.randint(0, crossover_locs)
        child[index] = parent1[index]
    for item in parent2:
        if item not in child:
            for i in range(len(parent2)):
                if child[i] is None:  # Look for the next available (None) slot
                    child[i] = item  # Insert the item
                    break
    return "".join(child)

def mutate(child):
    childlist = list(child)
    if random.random() < mutation_rate:
        rand_letter1 = random.choice(childlist)
        index1 = childlist.index(rand_letter1)
        rand_letter2 = random.choice(childlist)
        index2 = childlist.index(rand_letter2)
        childlist[index1] = rand_letter2
        childlist[index2] = rand_letter1
        return "".join(childlist)
    return child

def pick_parents(message, population):
    #pop_set = set(population)
    big_group = random.sample(population, tournament_size*2)
    tournament1 = big_group[0:tournament_size]
    tournament2 = big_group[tournament_size::]

    tournament1.sort(key = lambda ciph: ciph_and_fitness_dict[ciph])
    tournament1.reverse()
    tournament2.sort(key = lambda ciph: ciph_and_fitness_dict[ciph])
    tournament2.reverse()

    counter = 0
    while True:
        num = random.random()
        if num < win_prob:
            parent1 = tournament1[counter]
            parent2 = tournament2[counter]
            return (parent1, parent2)
        else:
            counter += 1

def selection(old_pop, message):
    new_pop = []
    #old_pop.sort(key = lambda cipher: fitness(decode(message, cipher)))
    #old_pop.reverse()
    for i in range(num_clones):
        new_pop.append(old_pop[i])
    #for j in range(population_size - num_clones):
    while len(new_pop) < 500:
        parent1, parent2 = pick_parents(message, old_pop)
        child = breed(parent1, parent2)
        child = mutate(child)
        if child not in new_pop:
            new_pop.append(child)
    return new_pop

def main(message):
    population = []
    for i in range(population_size):
        l = list(alpha)
        random.shuffle(l)
        cipher = ''.join(l)
        if cipher not in population:
            population.append(cipher)
    counter = 0
    while counter <= 500:
        calculate_all_fitness(population, message)
        population.sort(key = lambda ciph: ciph_and_fitness_dict[ciph])
        population.reverse()
        print(decode(message, population[0]))
        population = selection(population, message)
        counter += 1

message = sys.argv[1]
main(message)


# old_population = ["ECGFA", "TRYOP", "KPLEW", "VKNOJ"]
# old_population.sort(key = lambda cipher: fitness(cipher))
# old_population.reverse()
# print(old_population)