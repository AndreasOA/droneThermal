import cv2
import numpy as np
import os
import time


def drawRect(image, area, width, height):
    cv2.rectangle(image,(area[0] - width,area[1] - height),(area[0]+width+5,area[1]+height+5),(255,0,0),2)

    return image

def drawRectFromThresholdInImage(image: cv2, args):
    """This function uses the threshold tol to reduce unwanted objects in image and draws a
    rectangle on the largest remaining conture.

    Args:
        image (cv2): cv2 image object
        tol (float): Value for tolerance, how much below the maxium brightness value should be shown

    Returns:
        cv2 image: Image with rectangle above largest conture
    """
    tol, area, area_range, waypoints, i = args
    #image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    result = image.copy()
    # get brigthnes threshold
    thresh =cv2.threshold(image,np.max(image) - 255 * tol,255, cv2.THRESH_TOZERO)[1]
    #cv2.imwrite('test.jpg', thresh)
    #thresh = cv2.threshold(image,np.max(image) - 255 * tol,255,cv2.THRESH_BINARY)[1]
    # get contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
   
    if len(area) != 0:
        countours_in_range = []
        for contour in contours:
            contour_mean = np.mean(contour, axis=0)[0]
            if (area[0] - area_range[0]) < contour_mean[0] and (area[0] + area_range[0]) > contour_mean[0] and \
                        (area[1] - area_range[1]) < contour_mean[1] and (area[1] + area_range[1]) > contour_mean[1]:
                countours_in_range.append(contour)

    
        contours = countours_in_range
    if len(contours) != 0:
        contour = max(contours, key = cv2.contourArea)
        area = cv2.boundingRect(contour)
    
    result = drawRect(result, area, 20, 20)

    
    if len(waypoints) > 1:
        for j, waypoint in enumerate(waypoints):
            if j != len(waypoints) -1:
                result = cv2.line(result, waypoint, waypoints[j + 1], [255, 0, 0], 2)
            #result = cv2.circle(result, waypoint, radius=2, color=(255, 0, 0), thickness=3)
    if i % 30 == 0:
        waypoints.append((area[0], area[1]))

    return result, area, area_range, waypoints

def applyFuncToImagColl(func, path: str, new_path: str, args:tuple):
    """_summary_

    Args:
        func (function): function with should be applied on images
        path (str): path to images as string
        new_path (str): path for new images
        args (tuple): Attributes needed for function
    """
    print("[Status] - Applying Function on Collection.")
    path = path if path[-1] ==  "/" or path[-1] ==  "\\" else path + "/"
    new_path = new_path if new_path[-1] ==  "/" or new_path[-1] ==  "\\" else new_path + "/"

    images = [img for img in os.listdir(path) if img.endswith(".jpg")]
    images.sort()
    # last_area = [0, 0]
    # same_area_cnt = 0
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    #img_t = cv2.imread(path + images[0], 0)
    #img_t = cv2.normalize(img_t, None, 0, 255, cv2.NORM_MINMAX)
    #img_t = cv2.blur(img_t, (7, 7))
    for i, image in enumerate(images):
        image = cv2.imread(path + image, 0)
        #image = np.where(image > img_t, image - img_t, 0).astype(np.uint8)
        result = func(image, args)
        result_img, area, area_range, waypoints = result
        # ths = 15
        # if last_area[0] + ths > area[0] and  last_area[1] + ths > area[1] and \
        #    last_area[0] - ths < area[0] and  last_area[1] - ths < area[1]:
        #     same_area_cnt += 1
        # else:
        #     last_area = [area[0], area[1]]
        #     same_area_cnt = 0
        
        # if same_area_cnt == 120:
        #     last_area = [0, 0]
        #     area = []
        #     same_area_cnt = 0

        args = (args[0], area, args[2], waypoints, i)
        cv2.imwrite(f'{new_path}frame{i:06}.jpg', result_img)
    print("[Status] - Finished applyFuncToImagColl")


if __name__ == "__main__":
    tol = 0.25
    applyFuncToImagColl(drawRectFromThresholdInImage, "gen/001/", "gen/001/func/", (tol, [], [20,20], []))