import cv2
import numpy
import PIL.Image


def PilImageToCvImage(img_pil: PIL.Image.Image) -> numpy.ndarray:
    img_cv2 = cv2.cvtColor(numpy.asarray(img_pil), cv2.COLOR_RGB2BGR)
    return img_cv2


def CvImageToPilImage(img_cv2: numpy.ndarray) -> PIL.Image.Image:
    img_pil = cv2.cvtColor(numpy.asarray(img_cv2), cv2.COLOR_RGB2BGR)
    return img_pil


def CvImageCrop(img_cv2: numpy.ndarray, rect, fixSize=None) -> numpy.ndarray:
    left, top, right, bottom = rect
    if fixSize is not None:
        width, height = fixSize
        wGap = width - right+left
        hGap = height - bottom + top
        if wGap > 0:
            right = int(right+wGap)
        if hGap > 0:
            bottom = int(bottom + hGap)

    crop_img = img_cv2[top:bottom, left:right]
    return crop_img


def CvImageSize(img_cv2: numpy.ndarray):
    sp = img_cv2.shape
    height = sp[0]
    width = sp[1]
    return width, height
