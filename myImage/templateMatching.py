import cv2
import numpy
import PIL.Image
from numpy.core.fromnumeric import size
import myImage.convert


def Tmatch(img, temp) -> tuple:
    img_cv2: numpy.ndarray
    temp_cv2: numpy.ndarray

    if isinstance(img, PIL.Image.Image):
        img_cv2 = myImage.convert.PilImageToCvImage(img)
    elif isinstance(img, numpy.ndarray):
        img_cv2 = img
    else:
        raise RuntimeError(
            'Tmatch wrong input img , expect numpy.ndarry or PIL.Image.Image, get '+type(img).__name__)

    if isinstance(temp, PIL.Image.Image):
        temp_cv2 = myImage.convert.PilImageToCvImage(temp)
    elif isinstance(temp, numpy.ndarray):
        temp_cv2 = temp
    else:
        raise RuntimeError(
            'Tmatch wrong input template , expect numpy.ndarry or PIL.Image.Image , get '+type(temp).__name__)


    # 灰阶 
    img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    temp_cv2 = cv2.cvtColor(temp_cv2, cv2.COLOR_BGR2GRAY)

    # #模糊
    # img_cv2 = cv2.blur(img_cv2, ksize=(3, 3))
    # temp_cv2 = cv2.blur(temp_cv2, ksize=(3, 3))

    # #自适应二值化
    # img_cv2=cv2.adaptiveThreshold(img_cv2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,8)
    # temp_cv2=cv2.adaptiveThreshold(temp_cv2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,8)

    # TODO : find out the best match method
    method = cv2.TM_CCOEFF_NORMED
    resMatrix = cv2.matchTemplate(img_cv2, temp_cv2, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resMatrix)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    # print(max_val)
    # print(max_loc)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        left_top = min_loc
        val = min_val
    else:
        left_top = max_loc
        val = max_val

    size = temp_cv2.shape
    right_bottom = (left_top[0] + size[1], left_top[1] + size[0])
    # print(left_top)
    # print(right_bottom)
    test = cv2.rectangle(img_cv2, left_top, right_bottom, 255, 2)
    cv2.imwrite("catch.png", test)
    print("val",val)

    reliable: bool = False

    if val < 0.95:
        reliable = False
    else:
        reliable = True

    return left_top+right_bottom, reliable
