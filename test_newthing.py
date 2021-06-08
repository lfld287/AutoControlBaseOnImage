import myImage.newThing as nt
import PIL.Image as Image
import numpy as np

#打开一张图片
img = Image.open("tmp.png")


img = img.convert("L")

img.show()
#将图片化为32*32的
# img = img.resize((1920, 32))
# img.show()
#二值化
img = img.point(lambda x: x > 150 and 255)
img.show()
img.save("nnnn.png")

# #将图片转换为数组形式，元素为其像素的亮度值
# img_array = np.asarray(img)
# print (img_array)
# #得到网格特征统计图
# features_array = nt.get_features(img_array)
# print (features_array)
# features_vector =features_array.reshape(features_array.shape[0]*features_array.shape[1])
# print (features_vector)