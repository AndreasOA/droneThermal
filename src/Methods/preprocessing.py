import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def convertImg8bitNorm(img):
    gray8_image = np.zeros((120, 160), dtype=np.uint8)
    gray8_image = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    gray8_image = np.uint8(gray8_image)

    plt.imshow(gray8_image, cmap='gray')
    plt.show()


def normalizeImgTEST(img_1, img_2):

    #x, y, w, h = 400, 338, 30, 32
    x, y, w, h = 0, 0, 630, 510
    ROI = img_1[y:y+h, x:x+w]

    # Calculate mean and STD of target area
    mean, STD  = cv2.meanStdDev(ROI)

    # Clip frame to lower and upper STD
    offset = 0.05
    clipped = np.clip(img_1, mean - offset*STD, mean + offset*STD).astype(np.uint8)
    clipped_bright = np.clip(img_2, mean - offset*STD, mean + offset*STD).astype(np.uint8)

    # Normalize to range
    result = cv2.normalize(clipped, clipped, 0, 255, norm_type=cv2.NORM_MINMAX)
    result_bright = cv2.normalize(clipped_bright, clipped_bright, 0, 255, norm_type=cv2.NORM_MINMAX)

    return result, result_bright



def setThresholdImage(img, tol: float):
    return cv2.threshold(img,np.max(img) - 255 * tol,255,cv2.THRESH_BINARY)[1]



if __name__ == "__main__":
    image = cv2.imread('gen/010/frame106.jpg', 0)
    image_bright = cv2.imread('gen/020/frame72.jpg', 0)

    f, axarr = plt.subplots(2,2) 
    # use the created array to output your multiple images. In this case I have stacked 4 images vertically
    axarr[0, 0].imshow(image, cmap='gray')
    axarr[0, 1].imshow(setThresholdImage(image, 0.25), cmap='gray')
    axarr[1, 0].imshow(image_bright, cmap='gray')
    axarr[1, 1].imshow(setThresholdImage(image_bright, 0.25), cmap='gray')
    plt.show()

