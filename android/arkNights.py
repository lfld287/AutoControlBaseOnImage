import myImage.sift as sift
import PIL.Image
import uiautomator2 as u2
import os
import myImage.ocr as ocr
import myImage.templateMatching as tm
import time

# constatns

# 资源文件

RESOURCE_PATH = "resource/arkNights"

GLOBAL_INTERVAL = 1

MISSION_NAMA = "1-7"

SCREEN_LIST = ["start", "login", "event", "supply",
               "checkin", "main", "DragonBoatFestival"]


def getCenter(pos: tuple):
    print(pos)
    left, top, right, bottom = pos
    x = left+(right-left)/2
    y = top+(bottom-top)/2
    return int(x), int(y)


class arkNights():
    def __init__(self, device: u2.Device, useSift: bool) -> None:
        self.d = device
        self.ss = None
        self.sift = useSift
        self.screenList = []
        g = os.listdir(RESOURCE_PATH)
        for f in g:
            m = os.path.join(RESOURCE_PATH, f)
            if(os.path.isdir(m)):
                self.screenList.append(f)
        print(self.screenList)

    def Match(self, img, temp):
        if self.sift:
            return sift.Smatch(img, temp)
        else:
            return tm.Tmatch(img, temp)

    def updateScreen(self):
        while True:
            self.ss = self.d.screenshot()
            if self.ss != None:
                break
            time.sleep(1)

    def checkAndStart(self):
        """
        检查当前app是不是mrfz，不是的话启动
        """
        if self.d.app_current().get("package") != "com.hypergryph.arknights":
            self.d.app_start("com.hypergryph.arknights",
                             "com.u8.sdk.U8UnityContext")

    # TODO 一个界面特征有多种可能，
    def checkScreen(self, screen: str, shouldUpdate: bool = True) -> bool:
        if shouldUpdate:
            self.updateScreen()
        if not os.path.exists(RESOURCE_PATH+"/"+screen+"/feature"):
            return False
        g = os.walk(RESOURCE_PATH+"/"+screen+"/feature")
        for root, _, files in g:
            for file in files:
                feature_img = PIL.Image.open(os.path.join(root, file))
                _, reliable = self.Match(self.ss, feature_img)
                if not reliable:
                    print(file+" mismatch")
                    return False
                else:
                    return True
        return False

    def actionFound(self, screen: str, element: str, interval: int = 1, shouldUpdate: bool = True) -> bool:
        if shouldUpdate:
            self.updateScreen()
        g = os.walk(RESOURCE_PATH+"/"+screen+"/action")
        result: bool
        for root, _, files in g:
            if element+".png" in files:
                element_img = PIL.Image.open(
                    os.path.join(root, element+".png"))
                _, reliable = self.Match(self.ss, element_img)
                if not reliable:
                    print(element+" not found in screeShot")
                    result = False
                else:
                    print(element+" found")
                    result = True
            else:
                print(element+" not found in action folder")
                result = False
        time.sleep(interval)
        return result

    def actionClick(self, screen: str, element: str, interval: int = 1, shouldUpdate: bool = True) -> bool:
        if shouldUpdate:
            self.updateScreen()
        g = os.walk(RESOURCE_PATH+"/"+screen+"/action")
        result: bool
        for root, _, files in g:
            if element+".png" in files:
                element_img = PIL.Image.open(
                    os.path.join(root, element+".png"))
                pos, reliable = self.Match(self.ss, element_img)
                if not reliable:
                    print(element+" not found in screeShot")
                    result = False
                else:
                    x, y = getCenter(pos)
                    self.d.click(x, y)
                    print("click "+element)
                    result = True
            else:
                print(element+" not found in action folder")
                result = False
        time.sleep(interval)
        return result

    def actionSwipe(self, fxp, fyp, txp, typ):
        width, height = self.d.window_size()
        fx = fxp*width
        fy = fyp*height
        tx = txp*width
        ty = typ*height
        self.d.swipe(fx, fy, tx, ty)

    def detectCurrentScreen(self) -> str:
        self.updateScreen()
        for scr in self.screenList:
            print("detect "+scr)
            if self.checkScreen(scr, shouldUpdate=False):
                return scr
        return "unknown"

    def gotoMainMenu(self):
        if self.checkScreen("main"):
            return
        while True:
            if self.actionClick("main", "home"):
                time.sleep(0.5)
                if self.actionClick("main", "mainpage"):
                    break
            scr = self.detectCurrentScreen()
            if scr == "main":
                print("alredy in MainMenu")
                break
            elif scr == "start":
                self.actionClick("start", "start_button")
            elif scr == "login":
                self.actionClick("login", "login_button")
            elif scr == "event":
                self.actionClick("event", "event_close")
            elif scr == "supply":
                self.actionClick("supply", "confirm_button")
            elif scr == "checkin":
                self.actionClick("checkin", "close_button")
            elif scr == "DragonBoatFestival":
                if not self.actionClick("DragonBoatFestival", "checkIn_button"):
                    self.actionClick("DragonBoatFestival", "close_button")

            else:
                print("unknown screen")

    def takeMaterial(self) -> bool:
        if not self.checkScreen("material_get"):
            return False
        return self.actionClick("material_get", "confirm_button")

    def startFight(self) -> bool:
        errorCount = 0
        while True:
            if errorCount >= 5:
                return False
            self.updateScreen()
            if self.actionFound("fight", "start_operation", shouldUpdate=False):
                if self.actionFound("fight", "agent_check", shouldUpdate=False):
                    self.actionClick(
                        "fight", "start_operation", shouldUpdate=False)
                    continue
                else:
                    self.actionClick("fight", "agent_uncheck",
                                     shouldUpdate=False)
                    continue
            elif self.actionFound("fight","start_final",shouldUpdate=False):
                self.actionClick("fight","start_final",shouldUpdate=False)
                continue
            elif self.actionFound("fight","takeover",shouldUpdate=False):
                print("fighting .... ")
                time.sleep(5)
            elif self.actionFound("fight","over",shouldUpdate=False):
                print("fight over ,return")
                self.actionClick("fight","over",shouldUpdate=False)
                return True 
            else:
                errorCount+=1


    def gotoMission(self):
        while not self.checkScreen("mission"):
            self.gotoMainMenu()
            time.sleep(GLOBAL_INTERVAL)
            self.actionClick("main", "mission")
            time.sleep(GLOBAL_INTERVAL)
            self.updateScreen()

    def clearMission(self):
        '''
        点完任务,每日，每周
        好像没得做 不懂 再说
        '''
        # 起点都是主菜单
        self.gotoMission()
        self.actionClick("mission", "daily_mission_uncheck")
        while True:
            if self.actionFound("mission", "daily_mission_check"):
                if not self.actionClick("mission", "take_button"):
                    break
            else:
                self.takeMaterial()

        return

    def gotoTerminal(self):
        while not self.checkScreen("terminal"):
            self.gotoMainMenu()
            time.sleep(GLOBAL_INTERVAL)
            self.actionClick("main", "terminal")
            time.sleep(GLOBAL_INTERVAL)
            self.updateScreen()
        return

    def gotoEpisode1(self):
        while not self.checkScreen("episode1"):
            self.gotoTerminal()
            while not self.actionFound("terminal", "main_theme_check"):
                self.actionClick("terminal", "main_theme_uncheck")
            while not self.actionFound("terminal", "awaken_check"):
                self.actionClick("terminal", "awaken_uncheck")
            self.actionClick("terminal", "evil_time_2")
        return

    def gotoFight_1_7(self) -> bool:
        self.gotoEpisode1()

        # 滑动搜索1-7
        if not self.actionClick("episode1", "1-7"):
            self.d.swipe_ext("right")
            self.d.swipe_ext("right")
            self.d.swipe_ext("right")
        while not self.actionClick("episode1", "1-7"):
            self.actionSwipe(0.6, 0.5, 0.4, 0.5)
            time.sleep(1.5)

        if not self.startFight():
            print("gotoFight_1_7 failed ...")
