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

pixel_list = []
for x in range(img.size[0]):
    for y in range(img.size[1]):
        pixel = pix[x, y]
        pixel_list.append(pixel)

# #naive 27 color quantization
# for i in range(img.size[0]):
#     for j in range(img.size[1]):
#         new_nums = ()
#         for col in range(3):
#             if pix[i,j][col] < 255 // 3:
#                 new_nums += (0,)
#             elif pix[i,j][col] > 255 * 2 // 3:
#                 new_nums += (255, ) 
#             else:
#                 new_nums += (127,)
#         pix[i,j] = new_nums

# #naive 8 color quantization
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

def k_means_plus_plus(k):
    i = random.randint(0, img.size[0]-1)
    j = random.randint(0, img.size[1]-1)
    center = pix[i, j]
    means_list = [center]
    min_distances = {pixel: float('inf') for pixel in pixel_list}
    while len(means_list) < k:
        for pixel in pixel_list:
            cent = means_list[-1]
            distance = get_error(cent, pixel)
            if distance < min_distances[pixel]:
                min_distances[pixel] = distance
        total_distance = sum(min_distances.values())
        weights = [min_distances[pixel] / total_distance for pixel in pixel_list]
        new_center = random.choices(pixel_list, weights=weights, k=1)[0]
        means_list.append(new_center)  
    return k_means(means_list)

def k_means(means_list):
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
    rounded_means = []
    for mean in means_list:
        rounded_means.append((round(mean[0]), round(mean[1]), round(mean[2])))
    return rounded_means
    
def find_closest_mean(pixel, k_means_list):
    err_list = []
    for mean in k_means_list:
        err_list.append(get_error(pixel, mean))
    smallest_error = min(err_list)
    corresponding_index = err_list.index(smallest_error)
    return k_means_list[corresponding_index]

def floyd_steinberg(k_means_list):
    w, h = img.size
    for y in range(h-1):
        for x in range(w-1):
            old_pixel = pix[x,y]
            new_pixel = find_closest_mean(old_pixel, k_means_list)

            old_red, old_green, old_blue = old_pixel
            new_red, new_green, new_blue = new_pixel

            pix[x,y] = (new_red, new_green, new_blue)

            error_red = old_red - new_red
            error_green = old_green - new_green
            error_blue = old_blue - new_blue

            if x < w - 1:
                red1, green1, blue1 = pix[x+1, y]
                red1 = int(red1 + error_red * (7/16))
                green1 = int(green1 + error_green * (7/16))
                blue1 = int(blue1 + error_blue * (7/16))
                pix[x+1, y] = (red1, green1, blue1)
        
            if x > 0 and y < h - 1:
                red2, green2, blue2 = pix[x-1, y+1]
                red2 = int(red2 + error_red * (3/16))
                green2 = int(green2 + error_green * (3/16))
                blue2 = int(blue2 + error_blue * (3/16))
                pix[x-1, y+1] = (red2, green2, blue2)
            
            if y < h - 1:
                red3, green3, blue3 = pix[x, y+1]
                red3 = int(red3 + error_red * (5/16))
                green3 = int(green3 + error_green * (5/16))
                blue3 = int(blue3 + error_blue * (5/16))
                pix[x, y+1] = (red3, green3, blue3)

            if x < w - 1 and y < h - 1:
                red4, green4, blue4 = pix[x+1, y+1]
                red4 = int(red4 + error_red * (1/16))
                green4 = int(green4 + error_green * (1/16))
                blue4 = int(blue4 + error_blue * (1/16))
                pix[x+1, y+1] = (red4, green4, blue4)

def add_palette_with_pix(image, k_means_list, palette_height=50):
    original_width, original_height = image.size
    color_width = original_width // len(k_means_list)
    new_img = Image.new("RGB", (original_width, original_height + palette_height), "white")
    new_img.paste(image, (0, 0))
    pix = new_img.load()
    for i, color in enumerate(k_means_list):
        for x in range(i * color_width, (i + 1) * color_width):
            for y in range(original_height, original_height + palette_height):
                pix[x, y] = color
    return new_img

k_means_list_27 = [(r, g, b) for r in [0, 127, 255] for g in [0, 127, 255] for b in [0, 127, 255]]
k_means_list_8 = [(r, g, b) for r in [0, 255] for g in [0, 255] for b in [0, 255]]

#k = int(sys.argv[2])

k = 6

start = perf_counter()
k_means_list = k_means_plus_plus(k)
#print(k_means_list)
floyd_steinberg(k_means_list)
img2 = add_palette_with_pix(img, k_means_list, palette_height=50)
img2.show() # Now, you should see a single white pixel near the upper left corner
img2.save("kmeansout.png") # Save the
