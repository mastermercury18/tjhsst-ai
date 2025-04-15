import math
from math import log
import random
import sys

data_list = []
copy_data_list = []

with open("star_data.csv") as f:
    counter = 0
    for line in f:
        counter += 1
        if counter == 1:
            continue
        array = line.strip().split(",")
        tup = ()
        for i in range(5):
            if i < 3:
                tup += (log(float(array[i])),)
            else:
                tup += (float(array[i]),)
        data_list.append(tup)
        copy_data_list.append(tup)
        #data_list.append(tuple(array[0:5]))
#print(data_list)

def get_error(star, mean):
    temp_error = (mean[0] - star[0]) ** 2
    lum_error = (mean[1] - star[1]) ** 2
    rad_error = (mean[2] - star[2]) ** 2
    mag_error = (mean[3] - star[3]) ** 2
    return temp_error + lum_error + rad_error + mag_error

def calc_average(associated_stars, num):
    the_sum = 0
    for star in associated_stars:
        the_sum += star[num]
    return the_sum / len(associated_stars)

def find_actual_means(mean_and_stars_dict):
    actual_means = []
    for mean in mean_and_stars_dict:
        associated_stars = mean_and_stars_dict[mean]
        avg_temp = calc_average(associated_stars, 0)
        avg_lum = calc_average(associated_stars, 1)
        avg_rad = calc_average(associated_stars, 2)
        avg_mag = calc_average(associated_stars, 3)
        actual_mean = (avg_temp, avg_lum, avg_rad, avg_mag)
        actual_means.append(actual_mean)
    return actual_means

mean_and_stars_dict = {}
num1 = int(sys.argv[1])
num2 = int(sys.argv[2])
num3 = int(sys.argv[3])
num4 = int(sys.argv[4])
num5 = int(sys.argv[5])
num6 = int(sys.argv[6])

def k_means():
    k = 6
    #means_list = random.sample(data_list, 6)
    means_list = [data_list[num1], data_list[num2], data_list[num3], data_list[num4], data_list[num5], data_list[num6]]
    counter = 0
    mean_and_stars_dict = dict()
    while means_list != list(mean_and_stars_dict.keys()) or counter == 0:
        mean_and_stars_dict = {mean: [] for mean in means_list}
        for star in data_list:
            min_error = float('inf')
            min_mean = None
            for mean in means_list:
                error = get_error(star, mean)
                if error < min_error:
                    min_error = error 
                    min_mean = mean 
            mean_and_stars_dict[min_mean].append(star)
        means_list = find_actual_means(mean_and_stars_dict)
        counter += 1 
    for mean in mean_and_stars_dict:
        print("Mean: " + str(mean) + "\n")
        for star in mean_and_stars_dict[mean]:
            print(star)
            print("Star type: " + str(star[4]))
        print("\n\n")
        #print(str(mean_and_stars_dict[mean]) + "\n\n")
    print("Number of generations: " + str(counter))

k_means()



