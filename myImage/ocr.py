from typing import List
import easyocr
import PIL.Image
import io
import myImage.convert
import numpy

myReader: any = None


def initReader():
    global myReader
    if myReader is None:
        myReader = easyocr.Reader(['en'],gpu=False)


def ListWord(img: any) -> List:
    img_cv2: numpy.ndarray
    if isinstance(img, PIL.Image.Image):
        img_cv2 = myImage.convert.PilImageToCvImage(img)
    elif isinstance(img, numpy.ndarray):
        img_cv2 = img
    else:
        raise RuntimeError(
            'Tmatch wrong input img , expect numpy.ndarry or PIL.Image.Image, get '+type(img).__name__)
    initReader()
    global myReader
    result = myReader.readtext(img_cv2,detail=0)
    return result
