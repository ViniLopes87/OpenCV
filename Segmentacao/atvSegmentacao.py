from __future__ import print_function
import numpy as np 
import cv2 as cv
import argparse

parser = argparse.ArgumentParser(description='Code for Basic Thresholding Operations tutorial.')
parser.add_argument('--input', help='Path to input image.', default='stuff.jpg')
args = parser.parse_args()
src = cv.imread(cv.samples.findFile(args.input))
if src is None:
    print('Could not open or find the image: ', args.input)
    exit(0)

# Convert the image to Gray
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU) 
cv.imshow('image', thresh)

# Wait until user finishes program
cv.waitKey()

# Remover equenos ruídos brancos na imagem
kernel = np.ones((2, 2), np.uint8) 
closing = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations = 2) 
bg = cv.dilate(closing, kernel, iterations = 1) 
dist_transform = cv.distanceTransform(closing, cv.DIST_L2, 0) 
ret, fg = cv.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0)

cv.imshow('image', fg)

# Wait until user finishes program
cv.waitKey()