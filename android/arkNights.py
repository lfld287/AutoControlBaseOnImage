from re import X
import uiautomator2 as u2
import time
import ocr.ocr as ocr


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
    list = ocr.ListWord(img)
    checkAndPassStartScreen(d, list)
    return False


def checkAndPassStartScreen(d: u2.Device, list: list):
    for i in list:
        print(i[1])
        print(i[1].find("START"))
        print(type(i[1]))
        s = i[1].strip()
        if s.find("START") != -1:
            x: int = i[0][0][0]-i[0][1][0]+i[0][0][0]
            y: int = i[0][2][1]-i[0][1][1]+i[0][2][1]
            print("clicking!!!!")
            d.click(x, y)


def testList(d: u2.Device):
    img = d.screenshot()
    list = ocr.ListWord(img)
    for i in list:
        print(type(i))
        print(i)
        print(type(i[0]))
        print(i[1])
    img.show()
