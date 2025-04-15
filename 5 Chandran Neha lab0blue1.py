from time import perf_counter
from heapq import heapify, heappush, heappop
import sys

#f1, f2, f3 = "1mfile1.txt", "1mfile2.txt", "1mfile3.txt"
#f1, f2, f3 = "100kfile1.txt", "100kfile2.txt", "100kfile3.txt"
#f1, f2, f3 = "10kfile1.txt", "10kfile2.txt", "10kfile3.txt"
f1 = sys.argv[1]
f2 = sys.argv[2]
f3 = sys.argv[3]
start = perf_counter()

with open(f1) as f:
    f1_set = set(int(line.strip()) for line in open(f1))
    f1_list = [int(line.strip()) for line in f]
with open(f2) as f:
    f2_set = set(int(line.strip()) for line in open(f2))
    f2_list = [int(line.strip()) for line in f]
with open(f3) as f:
    f3_set = set(int(line.strip()) for line in open(f3))
    f3_list = [int(line.strip()) for line in f]

count = 0
for val in f1_set:
    if val in f2_set:
        count += 1

print("1:" + str(count))

f1_dict = {}
mysum = 0
hun_range = int(len(f1_set) / 100)
for index, val in enumerate(f1_set):
    f1_dict[index] = val
for i in range(hun_range):
    temp_index = 100 * (i+1) - 1
    mysum += f1_dict[temp_index]
print("2: " + str(mysum))

f1_freq_dict = {}
f2_freq_dict = {}
for val in f1_list:
    f1_freq_dict[val] = f1_freq_dict.get(val, 0) + 1
for val in f2_list:
    f2_freq_dict[val] = f2_freq_dict.get(val, 0) + 1
total_freq_count = 0
for val in f3_set:
    total_freq_count += f1_freq_dict.get(val, 0) + f2_freq_dict.get(val, 0)
print("3: " + str(total_freq_count))

smallest = set()
sorted_f1_set = set(sorted(f1_list))
for i in range(10):
    smallest.add(list(sorted_f1_set)[i])
print("4: " + str(smallest))


f2_list_mod = []
f2_dict = {}
for val in f2_list:
    if val in f2_dict.keys():
        f2_dict[val] = f2_dict[val] + 1
    else:
        f2_dict[val] = 1
for val in f2_dict.keys():
    if f2_dict[val] > 1:
        f2_list_mod.append(val)
sorted_list_f2 = sorted(f2_list_mod)
biggest_list = []
for i in range(10):
    biggest_list.append(sorted_list_f2[len(sorted_list_f2) - 1 - i])
print("5: " + str(biggest_list))

sequence = set()
heap = []
heapify(heap)
min_val = float('inf')
for val in f1_list:
    heappush(heap, val)
    if val % 53 == 0:
        min_val = heappop(heap)
        while (min_val in sequence):
            min_val = heappop(heap)
        sequence.add(min_val)
print(sum(sequence))

#All your code goes here, including reading in the files and printing your output
end = perf_counter()
print("Total time:", end - start)