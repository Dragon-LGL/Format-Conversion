#tif转jpg
# -*- coding: UTF-8 -*-
import numpy as np
import os
import sys
from PIL import Image
from osgeo import gdal, gdalconst

# 读取tif
'''bandsOrder为RGB对应的波段顺序，
例如高分一号多光谱包含蓝，绿，红，近红外四个波段，
那么真彩色对应的波段顺序为3，2，1'''


def readTif(original, bandsOrder=[3, 2, 1]):
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()
    ds = gdal.Open(original, gdal.GA_ReadOnly)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    geotransform = ds.GetGeoTransform()
    proj = ds.GetProjection()
    data = np.empty([rows, cols, 3], dtype=float)
    for i in range(3):
        band = ds.GetRasterBand(bandsOrder[i])
        data1 = band.ReadAsArray()
        data[:, :, i] = data1
    return data
    

#百分比拉伸
def stretchImg(imgPath, resultPath, lower_percent=0.6, higher_percent=99.4):
    data=readTif(imgPath)
    n = data.shape[2]
    out = np.zeros_like(data, dtype=np.uint8)
    print('开始转换，请稍后······')
    x=0
    for i in range(n):
        a = 0
        b = 255
        c = np.percentile(data[:, :,i], lower_percent)
        d = np.percentile(data[:, :,i], higher_percent)
        t = a + (data[:, :,i] - c) * (b - a) / (d - c)
        t[t < a] = a
        t[t > b] = b
        out[:, :,i] = t
        x=1/n+x
        y=round(x,3)
        print('完成度：{}%'.format(y*100))
    outImg=Image.fromarray(np.uint8(out))
    outImg.save(resultPath)

imgPath='Samples_03.tif'	#输入路径
resultPath='s3.jpg'	#输出路径
stretchImg(imgPath,resultPath)
print('运行结束，输出成功！')
