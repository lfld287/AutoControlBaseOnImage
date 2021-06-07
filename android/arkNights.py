import PIL.Image
import uiautomator2 as u2
import time
import myImage.ocr as ocr
import myImage.templateMatching as tm
import android.screenRotation as sr

# constatns

RESOURCE_PATH = "resource/arkNights"


def getCenter(pos: tuple):
    print(pos)
    left,top,right,bottom = pos
    x = left+(right-left)/2
    y = top+(bottom-top)/2
    return int(x), int(y)


def checkAndStartMRFZ(d: u2.Device):
    """
    检查当前app是不是mrfz，不是的话启动
    :param device:
    """
    if d.app_current().get("package") != "com.hypergryph.arknights":
        d.app_start("com.hypergryph.arknights", "com.u8.sdk.U8UnityContext")
        # 启动之后要等待一会
        time.sleep(4)


def goToMainMenu(d: u2.Device) -> bool:
    img = d.screenshot()
    if checkIsStartScreen(d, img):
        checkAndPassStartScreen(d)
    return False


def checkIsStartScreen(d: u2.Device, img: PIL.Image.Image) -> bool:
    temp = PIL.Image.open(RESOURCE_PATH+"/start_menu_start.png")
    _, val = tm.Tmatch(img, temp)
    if val < 0.85:
        print("is not like start screen")
        return False
    else:
        print("is like start screen")
        return True


def checkAndPassStartScreen(d: u2.Device) -> bool:
    img = d.screenshot()
    temp = PIL.Image.open(RESOURCE_PATH+"/start_menu_start.png")
    pos, val = tm.Tmatch(img, temp)
    print(pos, val)
    if val < 0.85:
        return False
    print("found start,clicking")
    x, y = getCenter(pos)
    print(x)
    print(y)
    d.click(x, y)
    return True


def testList(d: u2.Device):
    img = d.screenshot()
    list = ocr.ListWord(img)
    for i in list:
        print(type(i))
        print(i)
        print(type(i[0]))
        print(i[1])
    img.show()
