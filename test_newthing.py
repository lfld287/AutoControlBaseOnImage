from PIL.Image import blend
import cv2
import numpy as np
import myImage.sift
import uiautomator2 as u2

d = u2.connect()
print(d.app_current())
print(d.info)
d.screenshot("tmp.png")

#打开一张图片
img = cv2.imread("tmp.png")
temp = cv2.imread("resource/arkNights/terminal/action/evil_time_2.png")


rect,reliable = myImage.sift.Smatch(img,temp)

l,t,r,b = rect

if not reliable:
    print("not reliable")

img = cv2.rectangle(img,(l,t),(r,b),(255,0,0),5)

cv2.imwrite("new_res.png",img)

# img_gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

# # cv2.imshow("123",img_gray)

# img_blur = cv2.blur(img_gray,ksize=(3,3))

# # adaptiveThreshold

# img_out=cv2.adaptiveThreshold(img_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,5,5)

# sobel_x = cv2.Sobel(img_blur, cv2.CV_64F, dx = 1, dy = 0, ksize = 5)
# sobel_y = cv2.Sobel(img_blur, cv2.CV_64F, dx = 0, dy = 1, ksize = 5)
# blended = cv2.addWeighted(src1=sobel_x, alpha=0.5, src2=sobel_y,
#                           beta=0.5, gamma=0)
# laplacian = cv2.Laplacian(img_blur, cv2.CV_64F)

# # cv2.imshow("123",img_out)

# k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))

# e=cv2.erode(img_gray,k)

# #canny edge

# img_canny = cv2.Canny(img_blur,100,200)

# cv2.xfeatures2d.SURF_create()

# cv2.imwrite("img_at.png",img_canny)


