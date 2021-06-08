import myImage.ocr as ocr
import PIL.Image as Image
import uiautomator2 as u2
import android.arkNights as MRFZ
import android.screenRotation as sr
import time

d = u2.connect()
#d.click(1560,1363)
# d.click(800,600)
print(d.app_current())
print(d.info)

# sr.clickRotation1(d,1560,1363)

session = MRFZ.arkNights(d)
session.checkAndStart()
session.MainToWarehouse()
