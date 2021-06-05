import tkinter as tk
import PIL.Image
import PIL.ImageTk
import numpy
import myImage.convert


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
    img_pil_resize, factor = resize(width, height, img_pil)
    photo = PIL.ImageTk.PhotoImage(img_pil_resize)
    print(factor)
    imageLabel = tk.Label(app, image=photo)
    imageLabel.pack()
    app.mainloop()
