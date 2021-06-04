import pyautogui
from PIL import Image

def Capture() -> Image.Image :
    img = pyautogui.screenshot(region=[0,0,1920,1080]) # x,y,w,h
    return img