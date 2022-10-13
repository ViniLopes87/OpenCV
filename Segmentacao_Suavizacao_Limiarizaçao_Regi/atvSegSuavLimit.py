import sys
import cv2 as cv
import numpy as np

DELAY_CAPTION = 3000
DELAY_BLUR = 3000
MAX_KERNEL_LENGTH = 30
src = None
dst = None
opt = 1

def SuavLimit(argv):
    imageName = argv[0] if len(argv) > 0 else 'vasos.png'
    global src
    src = cv.imread(cv.samples.findFile(imageName))
    if src is None:
        print ('Error opening image')
        print ('Usage: smoothing.py [image_name -- default ../data/lena.jpg] \n')
        return -1
    global dst

    src = cv.medianBlur(src,5)

    image=cv.cvtColor(src,cv.COLOR_BGR2GRAY)
    se=cv.getStructuringElement(cv.MORPH_RECT , (10,10))
    bg=cv.morphologyEx(image, cv.MORPH_DILATE, se)
    out_gray=cv.divide(image, bg, scale=300)

    ret,src = cv.threshold(out_gray,180,300,cv.THRESH_BINARY)

    result = cv.Canny(src, 30, 300)

    cv.imshow("Result", result)
    cv.waitKey(0)

if __name__ == "__main__":
    SuavLimit(sys.argv[1:])