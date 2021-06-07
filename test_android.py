import uiautomator2 as u2
import PIL.Image as Image
import myImage.ocr as ocr
import myImage.templateMatching as tm
import tool.cropTool.cropTool as ct


# d = u2.connect()
# d.screenshot("tmp.png")




# l = ocr.ListWordFile("tmp.png")
# for i in l :
#     print(i)

img = Image.open("tmp.png")
# ct.tool_crop(img,1600,900)
app = ct.CropTool(img,1600,900)
app.mainloop()
box = (1528, 1355, 1593, 1381)
temp = img.crop(box)
temp.save("temp.png")

# temp.show()
# print(type(img))
# print(type(temp))

res = tm.Tmatch(img,temp)

print(res)