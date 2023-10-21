import cv2
import imutils
import matplotlib.pyplot as plt

file_path = 'D:\ceshi'      #文件路径
img: None= cv2.imread('D:\ceshi\sss.png',cv2.IMREAD_UNCHANGED)
#将图像赋予变量
gray: None= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)    #将图像转化为灰度图像并赋予变量
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# ret,返回的是读取的第一帧的值   函数内几个变量分别代表：图片源，阈值，最大值，算法类型
if ret:
    print('成功读取数据')
else:
    print('未读取到数据')
plt.imshow(thresh, cmap='gray')     #imshow()函数的功能就是把数值展示成热图
plt.title("示例")     #修改图片标题
plt.rcParams['font.sans-serif']=['SimHei']      #解决标题中文乱码
plt.show()      #显示图片
img = cv2.resize(img, (600, 600))       #修改输出图像大小尺寸
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)     #转化为灰度图像
blurred = cv2.GaussianBlur(gray, (5, 5), 0)     #高斯滤波是对整幅图像进行加权平均的过程，应该是处理杂色，修边啥的
thresh = cv2.threshold(blurred, 157, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('Image', thresh)     #显示图像得窗口名字，要显示的图像

cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_SIMPLE)           #寻找轮廓的检索模式，轮廓的近似方法
cnts = imutils.grab_contours(cnts)          #返回cnts中的countors(轮廓)

for c in cnts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    if cX==cY:
        continue

    # 在图像上绘制形状的轮廓和中心
    cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
    cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(img, "center", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # 展示图片
    cv2.imshow("Image", img)
    print(cX, cY)
    cv2.waitKey(0)


