import cv2
import numpy as np
import os
import time
from src.Methods.threshold import drawRect


def drawRectFromThresholdInImage_new(image: cv2,res_img, args):
    """This function uses the threshold tol to reduce unwanted objects in image and draws a
    rectangle on the largest remaining conture.

    Args:
        image (cv2): cv2 image object
        tol (float): Value for tolerance, how much below the maxium brightness value should be shown

    Returns:
        cv2 image: Image with rectangle above largest conture
    """

    tol, area, area_range_original, area_range, waypoints, i = args
    result = res_img.copy()
    real_img = image.copy()
    # get brigthnes threshold
    thresh = cv2.threshold(image, np.max(image) - 255 * tol, 255, cv2.THRESH_BINARY)[1]
    if i%3000==0 and i > 0:
        cv2.imshow("test", thresh)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # get contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = [contour for contour in contours if contour.shape[0] < 3]
    contour_found = False
    use_contour = None
    for contour in contours:
        contour_mean = np.mean(contour, axis=0)[0]
        if len(area) == 0:
            contour_found = True
            use_contour = contour if use_contour is None or contour.shape[0] >= use_contour.shape[0] else use_contour
        elif (area[0] - area_range[0]) < contour_mean[0] and (area[0] + area_range[0]) > contour_mean[0] and \
                (area[1] - area_range[1]) < contour_mean[1] and (area[1] + area_range[1]) > contour_mean[1]:
            contour_found = True
            use_contour = contour if use_contour is None or contour.shape[0] >= use_contour.shape[0] else use_contour
            break

    if contour_found:
        area = cv2.boundingRect(use_contour)
        area_range = [12,12]
    else:
        area_range[0] += 0.2
        area_range[1] += 0.2

    result = drawRect(real_img, area, 20, 20)

    if len(waypoints) > 1:
        for j, waypoint in enumerate(waypoints):
            if j != len(waypoints) - 1:
                result = cv2.line(result, waypoint, waypoints[j + 1], [255, 0, 0], 2)
            # result = cv2.circle(result, waypoint, radius=2, color=(255, 0, 0), thickness=3)
    if i % 30 == 0:
        waypoints.append((area[0], area[1]))

    return result, area, area_range_original, area_range, waypoints



def applyFuncToImagColl_WithMean(func, path: str, new_path: str, mean_imgs, args:tuple):
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
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    for i, image in enumerate(images):
        image = cv2.imread(path + image, 0)
        mean_img = mean_imgs[int(i/20) if int(i/20) < len(mean_imgs) else -1]
        res_img = np.where(mean_img > image, 0, image-mean_img)
        if i % 3000 == 0 and i > 0:
            cv2.imshow("res", res_img)
            cv2.imshow("img", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        result = func(res_img, args)
        result_img, area, _, waypoints = result
        args = (args[0], area, args[2], waypoints, i)
        cv2.imwrite(f'{new_path}frame{i:06}.jpg', result_img)
    print("[Status] - Finished applyFuncToImagColl")


def applyMeanSubtraction(path:str, tol:float):
    path = path if path[-1] ==  "/" or path[-1] ==  "\\" else path + "/"
    images = [img for img in os.listdir(path) if img.endswith(".jpg")]
    images.sort()
    mean_imgs = []
    mean_img = np.zeros(cv2.imread(path + images[0], 0).shape)
    for i, image in enumerate(images):
        image = cv2.imread(path + image, 0)
        mean_img += image
        if i%59 == 0 and i > 0:
            img = ((mean_img/60)).astype(np.uint8)
            mean_imgs.append(np.where(img > np.max(img)*(1-tol), 50, img).astype(np.uint8))
            mean_img =np.zeros(image.shape)

    return mean_imgs



if __name__ == "__main__":
    tol = 0.1
    a = applyMeanSubtraction("gen/001/", tol)
    applyFuncToImagColl_WithMean(drawRectFromThresholdInImage_new, "gen/001/", "gen/001/func/", a, (tol, [], [12,12], [12,12], [], 0))
