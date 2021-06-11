import myImage.ocr as ocr
import PIL.Image as Image
import uiautomator2 as u2
import android.arkNights as MRFZ
import android.screenRotation as sr
import time

d = u2.connect()
print(d.app_current())
print(d.info)
session = MRFZ.arkNights(d,True)
session.checkAndStart()
session.gotoMainMenu()
