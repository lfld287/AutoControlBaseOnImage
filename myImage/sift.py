import numpy
import cv2
import PIL.Image
import myImage.convert
import itertools

mySift: any = None

myMatcher: any = None


def initMySift():
    global mySift
    if mySift == None:
        mySift = cv2.SIFT_create()


def initMatcher():
    global myMatcher
    if myMatcher == None:
        myMatcher = cv2.BFMatcher_create(cv2.NORM_L2, crossCheck=True)


def getSiftKeyPoints(img: any):

    global mySift

    img_cv2: numpy.ndarray
    if isinstance(img, PIL.Image.Image):
        img_cv2 = myImage.convert.PilImageToCvImage(img)
    elif isinstance(img, numpy.ndarray):
        img_cv2 = img
    else:
        raise RuntimeError(
            'Tmatch wrong input img , expect numpy.ndarry or PIL.Image.Image, get '+type(img).__name__)

    initMySift()
    # assert(isinstance(mySift, cv2.SIFT))
    # print(type(mySift))
    kp, des = mySift.detectAndCompute(img, None)
    # print(type(kp))
    # print(kp)
    img_res = cv2.drawKeypoints(img, kp, img_cv2)
    cv2.imwrite("sift_test.png", img_res)
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

    # 灰阶

    img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    temp_cv2 = cv2.cvtColor(temp_cv2, cv2.COLOR_BGR2GRAY)

    # #模糊
    img_cv2 = cv2.blur(img_cv2, ksize=(3, 3))
    temp_cv2 = cv2.blur(temp_cv2, ksize=(3, 3))

    # #自适应二值化
    # img_cv2=cv2.adaptiveThreshold(img_cv2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,8)
    # temp_cv2=cv2.adaptiveThreshold(temp_cv2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,8)

    kp_img, des_img = getSiftKeyPoints(img_cv2)
    kp_temp, des_temp = getSiftKeyPoints(temp_cv2)
    initMatcher()

    matches = myMatcher.match(des_temp, des_img)

    matches = sorted(matches, key=lambda x: x.distance)

    img3 = cv2.drawMatches(temp_cv2, kp_temp, img_cv2,
                           kp_img, matches, None, flags=2)

    cv2.imwrite("match_test.png", img3)

    # print(matches)

    return kp_img, matches


def Smatch(img: any, temp: any) -> tuple:

    img_cv2: numpy.ndarray

    if isinstance(img, PIL.Image.Image):
        img_cv2 = myImage.convert.PilImageToCvImage(img)
    elif isinstance(img, numpy.ndarray):
        img_cv2 = img
    else:
        raise RuntimeError(
            'Tmatch wrong input img , expect numpy.ndarry or PIL.Image.Image, get '+type(img).__name__)

    # img_copy = img_cv2.copy()

    kp, matches = brutalMatch(img_cv2, temp)

    i: int = 1
    pList: list = []

    for match in matches:
        pt = kp[match.trainIdx].pt
        # print(pt)
        pList.append([pt[0], pt[1]])
        # img_copy = cv2.circle(
        #     img_copy, (int(pt[0]), int(pt[1])), 2, (255, 0, 0), 2)
        i += 1

    rect, density = getMaxDensityRect(pList, 35, 35)
    print("density", density)
    left, top, right, bottom = rect
    # area = (right-left)*(bottom - top)
    # print(area)
    # img_copy = cv2.rectangle(img_copy, (left, top),
    #                          (right, bottom), (255, 0, 0), 2)
    #cv2.imwrite("rect.png", img_copy)

    reliable: bool = False

    if density < 0.03:
        reliable = False
    else:
        reliable = True

    img_rect = cv2.rectangle(img_cv2, (left, top),
                             (right, bottom), (255, 0, 0), 5)
    cv2.imwrite("sift_rect_res.png", img_rect)

    return rect, reliable


def pointInRect(pt, rect) -> bool:
    x = pt[0]
    y = pt[1]
    left, top, right, bottom = rect
    if x >= left and x <= right and y >= top and y <= bottom:
        return True
    else:
        return False


def caculatePointCountInRect(pList: list, rect) -> int:
    count = 0
    for pt in pList:
        if pointInRect(pt, rect):
            count += 1
    return count


def caculateDenisty(pList: list, rect) -> float:
    # 比较的应该是单位范围内的特征点比例
    count = caculatePointCountInRect(pList, rect)
    left, top, right, bottom = rect
    area = (right - left)*(bottom - top)
    density = count/len(pList)*100/area
    return density


def generateRectByFourPoint(pList: tuple, rectMinWidth: int, rectMinHeight: int) -> tuple:
    minX: int = pList[0][0]
    minY: int = pList[0][1]
    maxX: int = pList[0][0]
    maxY: int = pList[0][1]
    for pt in pList:
        if pt[0] < minX:
            minX = pt[0]
        if pt[0] > maxX:
            maxX = pt[0]
        if pt[1] < minY:
            minY = pt[1]
        if pt[1] > maxY:
            maxY = pt[1]
    if maxX == minX or maxY == minY:
        return None
    # 如果太小 进行扩张到最小矩形 ，中心扩张
    left = minX
    right = maxX
    top = minY
    bottom = maxY
    wGap = rectMinWidth - right + left
    hGap = rectMinHeight - bottom + top
    if wGap > 0:
        left = left - wGap
    if hGap > 0:
        top = top - hGap
    if left < 0:
        left = 0
    if top < 0:
        top = 0
    return(left, top, right, bottom)


# 没有好办法，只能取四个点构成矩形，然后一个个遍历了。
def getMaxDensityRect(pList: list, rectMinHeight, rectMinWidth):

    #   先用最弱智的方法实现，后面看看能不能优化

    for pt in pList:
        # 先化成整形
        pt[0] = int(pt[0])
        pt[1] = int(pt[1])

    maxDensity: float = 0
    maxCount: int = 0
    maxRect: list[int] = [0, 0, 0, 0]

    for combo in itertools.combinations(pList, 4):
        rect = generateRectByFourPoint(
            combo, rectMinWidth, rectMinHeight)
        if rect == None:
            continue
        density = caculateDenisty(pList, rect)
        if density > maxDensity:
            maxDensity = density
            maxRect = list(rect)

    print(maxDensity)
    print(maxRect)

    return tuple(maxRect), maxDensity
