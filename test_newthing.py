from PIL.Image import blend
import cv2
import numpy as np
from numpy.lib.ufunclike import fix
import myImage.sift
import myImage.templateMatching
import myImage.orb
import myImage.ocr
import myImage.convert
import uiautomator2 as u2

d = u2.connect()
print(d.app_current())
print(d.info)
d.screenshot("tmp.png")

# 打开一张图片
img = cv2.imread("tmp.png")
temp = cv2.imread("resource/arkNights/fight/action/start_operation.png")


rect, reliable = myImage.templateMatching.Tmatch(img, temp)

print(reliable, rect)

