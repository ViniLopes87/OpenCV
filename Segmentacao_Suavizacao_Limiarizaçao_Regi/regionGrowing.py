import sys
import cv2 as cv2
import numpy as np
from matplotlib import pyplot as plt

def on_mouse(event, x, y, flags, params):
    if event == cv2.CV_EVENT_LBUTTONDOWN:
        print ('Start Mouse Position: ' + str(x) + ', ' + str(y))
        s_box = x, y
        boxes.append(s_box)

def region_growing(img, seed):
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    region_threshold = 0.2
    region_size = 1
    intensity_difference = 0
    neighbor_points_list = []
    neighbor_intensity_list = []

    region_mean = img[seed]

    height, width = img.shape
    image_size = height * width

    segmented_img = np.zeros((height, width, 1), np.uint8)

    while (intensity_difference < region_threshold) & (region_size < image_size):
        for i in range(4):
            x_new = seed[0] + neighbors[i][0]
            y_new = seed[1] + neighbors[i][1]

            check_inside = (x_new >= 0) & (y_new >= 0) & (x_new < height) & (y_new < width)

            if check_inside:
                if segmented_img[x_new, y_new] == 0:
                    neighbor_points_list.append([x_new, y_new])
                    neighbor_intensity_list.append(img[x_new, y_new])
                    segmented_img[x_new, y_new] = 255

        distance = abs(neighbor_intensity_list-region_mean)
        pixel_distance = min(distance)
        index = np.where(distance == pixel_distance)[0][0]
        segmented_img[seed[0], seed[1]] = 255
        region_size += 1

        region_mean = (region_mean*region_size + neighbor_intensity_list[index])/(region_size+1)

        seed = neighbor_points_list[index]

        neighbor_intensity_list[index] = neighbor_intensity_list[-1]
        neighbor_points_list[index] = neighbor_points_list[-1]

    return segmented_img

if __name__ == '__main__':
    boxes = []
    filename = 'vasos.png'
    img = cv2.imread(filename, 0)
    resized = cv2.resize(img,(256,256))
    cv2.namedWindow('input')
    cv2.setMouseCallback('input', on_mouse, 0,)
    cv2.imshow('input', resized)
    cv2.waitKey()
    print ("Starting region growing based on last click")
    seed = boxes[-1]
    cv2.imshow('input', region_growing(resized, seed))
    print ("Done. Showing output now")

    cv2.waitKey()
    cv2.destroyAllWindows()