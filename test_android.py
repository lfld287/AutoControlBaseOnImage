import uiautomator2 as u2
import PIL.Image as Image
import ocr.ocr as ocr



# d = u2.connect()
# d.screenshot("tmp.png")




# l = ocr.ListWordFile("tmp.png")
# for i in l :
#     print(i)

img = Image.open("tmp.png")
box = (1528, 1355, 1593, 1381)
c = img.crop(box)
c.show()

