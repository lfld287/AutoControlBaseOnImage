import numpy
import cv2
import PIL.Image
import myImage.convert

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

    rect, density = getMaxDensityRect(pList, 4, 4)
    print("density",density)
    # left, top, right, bottom = rect
    #area = (right-left)*(bottom - top)
    # print(area)
    # img_copy = cv2.rectangle(img_copy, (left, top),
    #                          (right, bottom), (255, 0, 0), 2)
    #cv2.imwrite("rect.png", img_copy)

    reliable: bool = False

    if density < 0.04:
        reliable = False
    else:
        reliable = True

    return rect, reliable


def pointInRect(pt, rect) -> bool:
    x = pt[0]
    y = pt[1]
    left, top, right, bottom = rect
    if x >= left and x <= right and y >= top and y <= bottom:
        return True
    else:
        return False


def getMaxDensityRect(pList: list, rectMinHeight, rectMinWidth):

    #   先用最弱智的方法实现，后面看看能不能优化

    for pt in pList:
        # 先化成整形
        pt[0] = int(pt[0])
        pt[1] = int(pt[1])

    maxDensity: float = 0
    rect: list[int] = [0, 0, 0, 0]

    for pt1 in pList:
        for pt2 in pList:
            # 如果x坐标或者y坐标相同就无法组成矩形
            # 有重复，要保证一号电在二号点左上方
            if pt2[0]-pt1[0] >= rectMinWidth and pt2[1]-pt1[1] >= rectMinHeight:
                # 计算矩形里面有几个点
                top = pt1[1]
                left = pt1[0]
                right = pt2[0]
                bottom = pt2[1]
                pointInclude = 0
                area = (right - left)*(bottom - top)
                for pt3 in pList:
                    if pointInRect(pt3, [left, top, right, bottom]):
                        pointInclude += 1
                density = float(pointInclude)/float(area)
                # print(area,pointInclude,density)
                if density > maxDensity:
                    print(density)
                    maxDensity = density
                    rect = [left, top, right, bottom]

    print(maxDensity)
    print(rect)

    return tuple(rect), maxDensity
