import ocr.ocr as ocr
import PIL.Image as Image
import uiautomator2 as u2
import android.arkNights as MRFZ
import time

d = u2.connect()
print(d.app_current())
MRFZ.checkAndStartMRFZ(d)
time.sleep(5)
# MRFZ.testList(d)
while True:
    if MRFZ.goToMainMenu(d) :
        break

d.app_stop("com.hypergryph.arknights")