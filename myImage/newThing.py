
import numpy as np
 
 
 
#将二值化后的数组转化成网格特征统计图
 
def get_features(array:np.ndarray):
    #拿到数组的高度和宽度
    h, w = array.shape
    data = []
    for x in range(0, w/4):
        offset_y = x * 4
        temp = []
        for y in range(0,h/4):
            offset_x = y * 4
            #统计每个区域的1的值
            temp.append(sum(sum(array[0+offset_y:4+offset_y,0+offset_x:4+offset_x])))
        data.append(temp)
    return np.asarray(data)
 
    
 

