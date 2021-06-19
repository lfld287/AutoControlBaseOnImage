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
只靠模板匹配不现实，应该是大量的模板匹配，配合少量特征检测（主要为图片）,可能还需要ocr，
但是目前ocr性能太屎，看看有没有其他选择
'''



d = u2.connect()

session = MRFZ.arkNights(d,False)
session.checkAndStart()
session.gotoFight(1,"1-7",1000)
#session.gotoFight(3,"s3-4")


