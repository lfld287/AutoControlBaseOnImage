import tkinter as tk
from tkinter.constants import NO
import PIL.Image
import PIL.ImageTk
import numpy
import myImage.convert
import time


def resize(w_box: int, h_box: int, pil_image: PIL.Image.Image) -> tuple:

    f1 = 1.0*w_box/pil_image.width  # 1.0 forces float division in Python2
    f2 = 1.0*h_box/pil_image.height
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(pil_image.width*factor)
    height = int(pil_image.height*factor)
    return pil_image.resize((width, height), PIL.Image.ANTIALIAS), factor


def tool_crop(img, width: int, height: int):

    img_pil: PIL.Image.Image
    if isinstance(img, PIL.Image.Image):
        img_pil = img
    elif isinstance(img, numpy.ndarray):
        img_pil = myImage.convert.CvImageToPilImage(img)
    else:
        raise RuntimeError(
            'Tmatch wrong input img , expect numpy.ndarry or PIL.Image.Image, get '+type(img).__name__)

    app = tk.Tk()
    app.title("cropTool")
    # 裁剪图像，不然直接爆炸
    img_pil_resize, factor = resize(width, height, img_pil)
    photo = PIL.ImageTk.PhotoImage(img_pil_resize)
    print(factor)
    # imageLabel = tk.Label(app, image=photo)
    # imageLabel.pack()
    # 添加一个画布拿来画矩形
    canvas = tk.Canvas(app, height=height, width=width)
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.create_rectangle(0, 0, 200, 200, outline='red', width=3)
    canvas.pack()
    app.mainloop()


class CropTool(tk.Tk):
    def __init__(self: any, img, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.rect = None
        self.factor = None
        self.rectX = None
        self.rectY = None
        self.curX = None
        self.curY = None
        self.img_original = None
        self.img_resize = None
        self.img_crop = None
        self.photo = None
        self.canvas = None
        self.vbar = None
        self.hbar = None
        self.title("cropTool")
        self.__draw_image(img)
        self.__mouse_evnet_init()

    def __draw_image(self, img: any):
        if isinstance(img, PIL.Image.Image):
            self.img_original = img
        elif isinstance(img, numpy.ndarray):
            self.img_original = myImage.convert.CvImageToPilImage(img)
        else:
            raise RuntimeError(
                'Tmatch wrong input img , expect numpy.ndarry or PIL.Image.Image, get '+type(img).__name__)

        self.img_resize, self.factor = self.__resize(
            self.width, self.height, self.img_original)
        self.photo = PIL.ImageTk.PhotoImage(self.img_original)

        frame = tk.Frame(self, height=self.img_original.height,
                         width=self.img_original.width)
        frame.pack(expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(
            frame, height=self.img_original.height, width=self.img_original.width,
            scrollregion=(0, 0, self.img_original.width, self.img_original.height))
        # self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.canvas.xview)
        self.hbar = hbar
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.canvas.yview)
        self.vbar = vbar
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def __mouse_evnet_init(self):
        assert(type(self.canvas) is tk.Canvas)
        self.canvas.bind("<ButtonPress-1>", self.__on_button_press)
        self.canvas.bind("<B1-Motion>", self.__on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.__on_button_release)

    def __resize(self, w_box: int, h_box: int, pil_image: PIL.Image.Image) -> tuple:
        f1 = 1.0*w_box/pil_image.width  # 1.0 forces float division in Python2
        f2 = 1.0*h_box/pil_image.height
        factor = min([f1, f2])
        # print(f1, f2, factor) # test
        # use best down-sizing filter
        width = int(pil_image.width*factor)
        height = int(pil_image.height*factor)
        return pil_image.resize((width, height), PIL.Image.ANTIALIAS), factor

    def __on_button_press(self, event):
        # save mouse drag start position
        top, _ = self.vbar.get()
        left, _ = self.hbar.get()

        self.rectX = event.x + left*self.img_original.width
        self.rectY = event.y + top*self.img_original.height

        self.curX = 0
        self.curY = 0

        print("press")
        if self.rect != None:
            self.canvas.delete(self.rect)

    def __on_move_press(self, event):
        top, _ = self.vbar.get()
        left, _ = self.hbar.get()
        self.curX = event.x + left*self.img_original.width
        self.curY = event.y + top*self.img_original.height

        # expand rectangle as you drag the mouse
        if self.rect != None:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.rectX, self.rectY, 1, 1, outline="red", width=3)
        self.canvas.coords(self.rect, self.rectX,
                           self.rectY, self.curX, self.curY)

    def __on_button_release(self, event):
        if self.curX > self.rectX and self.curY > self.rectY:
            self.img_crop = self.img_original.crop(
                (self.rectX, self.rectY, self.curX, self.curY))
            self.img_crop.save("crop_image/crop_%d.png" % (int(time.time())))
            print((self.rectX, self.rectY, self.curX, self.curY))
        pass
