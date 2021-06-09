import uiautomator2 as u2
import PIL.Image as Image
import myImage.ocr as ocr
import myImage.templateMatching as tm
import tool.cropTool.cropTool as ct


d = u2.connect()
print(d.app_current())
print(d.info)
d.screenshot("tmp.png")


# l = ocr.ListWordFile("tmp.png")
# for i in l :
#     print(i)

img = Image.open("tmp.png")

# box = (1528, 1355, 1593, 1381)
# temp = img.crop(box)
# temp.save("temp.png")

# res = tm.Tmatch(img,temp)

# print(res)


# ct.tool_crop(img,1600,900)
app = ct.CropTool(img, 1600, 900)
app.mainloop()


# temp.show()
# print(type(img))
# print(type(temp))
