import argparse
import cv2
import numpy as np

refPt = []
cropping = False
type = 0

def click_and_crop(event, x, y, flags, param):
    global refPt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(refPt) < type:
            refPt.append((x, y))
        else:
            print("Ultrapassou o limite de pontos!")
    elif event == cv2.EVENT_LBUTTONUP:
        for i in range(len(refPt)):
            cv2.line(image, refPt[i],  refPt[i+1],  (0, 255, 0), 2)
            cv2.imshow("image", image)

print('1 | 4-conectividade')
print('2 | 8-conectividade')
print('3 | m-conectividade')
esc = int(input('Escolha uma opção: '))

if esc == 1:
    type = 5
elif esc == 2:
    type = 9
else:
    type = 99

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
while True:
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("r"):
		image = clone.copy()
	elif key == ord("c"):
		break

pts = np.array(refPt)
rect = cv2.boundingRect(pts)
x,y,w,h = rect
croped = image[y:y+h, x:x+w].copy()

pts = pts - pts.min(axis=0)

mask = np.zeros(croped.shape[:2], np.uint8)
cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

dst = cv2.bitwise_and(croped, croped, mask=mask)

bg = np.ones_like(croped, np.uint8)*255
cv2.bitwise_not(bg,bg, mask=mask)
dst2 = bg+ dst

cv2.imshow("dst.png", dst)
cv2.waitKey(0)

cv2.destroyAllWindows()