import cv2
import numpy
import myImage
import PIL.Image

myOrb: any = None

myMatcher: any = None

def initMyOrb():
    global myOrb
    if myOrb == None:
        myOrb = cv2.ORB_create()


def initMatcher():
    global myMatcher
    if myMatcher == None:
        myMatcher = cv2.BFMatcher_create(cv2.NORM_HAMMING)

def getOrbKeyPoints(img: any):
    
    global myOrb

    initMyOrb()

    kp, des = myOrb.detectAndCompute(img, None)

    return kp, des

def brutalMatch(img: any, temp: any):
    
    global myMatcher

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
            'Tmatch wrong input img , expect numpy.ndarry or PIL.Image.Image, get '+type(temp).__name__)

    # 灰阶''

    img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    temp_cv2 = cv2.cvtColor(temp_cv2, cv2.COLOR_BGR2GRAY)

    # #模糊
    # img_cv2 = cv2.blur(img_cv2, ksize=(9, 9))
    # temp_cv2 = cv2.blur(temp_cv2, ksize=(9, 9))

    # #自适应二值化
    # img_cv2=cv2.adaptiveThreshold(img_cv2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,8)
    # temp_cv2=cv2.adaptiveThreshold(temp_cv2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,8)

    kp_img, des_img = getOrbKeyPoints(img_cv2)
    kp_temp, des_temp = getOrbKeyPoints(temp_cv2)
    initMatcher()

    matches = myMatcher.match(des_temp, des_img)

    matches = sorted(matches, key=lambda x: x.distance)

    img3 = cv2.drawMatches(temp_cv2, kp_temp, img_cv2,
                           kp_img, matches[:20], None, flags=2)

    cv2.imwrite("match_test.png", img3)

    # print(matches)

    return kp_img, kp_temp, matches