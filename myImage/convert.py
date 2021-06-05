import cv2
import numpy
import PIL.Image



def PilImageToCvImage(img_pil: PIL.Image.Image) -> numpy.ndarray:
    img_cv2 = cv2.cvtColor(numpy.asarray(img_pil), cv2.COLOR_RGB2BGR)
    return img_cv2


def CvImageToPilImage(img_cv2: numpy.ndarray) -> PIL.Image.Image:
    img_pil = cv2.cvtColor(numpy.asarray(img_cv2), cv2.COLOR_RGB2BGR)
    return img_pil
    