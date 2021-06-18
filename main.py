import myImage.ocr as ocr
import PIL.Image as Image
import uiautomator2 as u2
import android.arkNights as MRFZ
import android.screenRotation as sr
import time

'''
模板匹配 速度快 分辨率一定情况下 准确率高， 还是首选
各种基于特征的匹配方法，由于人工ui有很多规则的图像 大量相同的配色，还有印刷体文字，都使得基于特征又慢又不准确
后面还是想办法基于模板匹配进行开发。
'''



d = u2.connect()

session = MRFZ.arkNights(d,False)
session.checkAndStart()
session.gotoFight_1_7()

