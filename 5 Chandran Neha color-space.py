from PIL import Image
import random 
from time import perf_counter
import sys

#filename = sys.argv[1]

filename = "/Users/neha/Documents/tj/ai/data_files/batman.jpeg"

img = Image.open(filename) # Just put the local filename in quotes.
img.show() # Send the image to your OS to be displayed as a temporary file
print(img.size) # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.

#naive 27 color quantization
for i in range(img.size[0]):
    for j in range(img.size[1]):
        new_nums = ()
        for col in range(3):
            if pix[i,j][col] < 255 // 3:
                new_nums += (0,)
            elif pix[i,j][col] > 255 * 2 // 3:
                new_nums += (255, ) 
            else:
                new_nums += (127,)
        pix[i,j] = new_nums

#naive 8 color quantization
# for i in range(img.size[0]):
#     for j in range(img.size[1]):
#         new_nums = ()
#         for col in range(3):
#             if pix[i,j][col] < 128:
#                 new_nums += (0,)
#             else:
#                 new_nums += (255,)
#         pix[i,j] = new_nums
    
# img.show() # Now, you should see a single white pixel near the upper left corner
# img.save("my_image.png") # Save the

pixel_list = []
for x in range(img.size[0]):
    for y in range(img.size[1]):
        pixel = pix[x, y]
        pixel_list.append(pixel)

def get_error(pixel, mean):
    red_error = (mean[0] - pixel[0]) ** 2
    green_error = (mean[1] - pixel[1]) ** 2
    blue_error = (mean[2] - pixel[2]) ** 2
    return red_error + green_error + blue_error

def calc_average(associated_pixels, num):
    the_sum = 0
    for star in associated_pixels:
        the_sum += star[num]
    return the_sum / len(associated_pixels)

def find_actual_means(mean_and_pixels_dict):
    actual_means = []
    for mean in mean_and_pixels_dict:
        associated_pixels = mean_and_pixels_dict[mean]
        avg_red = calc_average(associated_pixels, 0)
        avg_green = calc_average(associated_pixels, 1)
        avg_blue = calc_average(associated_pixels, 2)
        actual_mean = (avg_red, avg_green, avg_blue)
        actual_means.append(actual_mean)
    return actual_means

def k_means(k):
    means_list = []
    while len(means_list) != k:
        i = random.randint(0,img.size[0]-1)
        j = random.randint(0,img.size[1]-1)
        mean = pix[i, j]
        if mean not in means_list:
            means_list.append(mean)
    counter = 0
    mean_and_pixels_dict = dict()
    pixel_to_mean_dict = {}
    while means_list != list(mean_and_pixels_dict.keys()) or counter == 0:
        mean_and_pixels_dict = {mean: [] for mean in means_list}
        for pixel in pixel_list:
            #if pixel not in pixel_to_mean_dict:
            min_error = float('inf')
            min_mean = None
            for mean in means_list:
                error = get_error(pixel, mean)
                if error < min_error:
                    min_error = error 
                    min_mean = mean 
            pixel_to_mean_dict[pixel] = min_mean
            mean_and_pixels_dict[min_mean].append(pixel)
        means_list = find_actual_means(mean_and_pixels_dict)
        counter += 1 
    # Now, loop through each pixel in the image
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            current_pixel = pix[i, j]
            mean = pixel_to_mean_dict[current_pixel]
            pix[i, j] = (round(mean[0]), round(mean[1]), round(mean[2]))

start = perf_counter()
# k = 27
# k_means(k)
# end = perf_counter()
# print(end - start)

img.show() # Now, you should see a single white pixel near the upper left corner
img.save("kmeansout.png") # Save the
