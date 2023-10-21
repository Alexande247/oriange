import cv2
import imutils
import matplotlib.pyplot as plt

file_path = 'D:\ceshi'
img: None= cv2.imread('D:\ceshi\sss.png',cv2.IMREAD_UNCHANGED)

gray: None= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
if ret:
    print('成功读取数据')
else:
    print('未读取到数据')
plt.imshow(thresh, cmap='gray')
plt.title("示例")
plt.rcParams['font.sans-serif']=['SimHei']
plt.show()
img = cv2.resize(img, (600, 600))
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 157, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('Image', thresh)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    if cX==cY:
        continue
    print(c[0][0][0], c[0][0][1])
    print(c[7][0][0], c[7][0][1])
    print(c[15][0][0], c[15][0][1])
    print(c[22][0][0], c[22][0][1])
    print('--------------')
    print(cX, cY)
    print('--------------')

    # 在图像上绘制形状的轮廓和中心
    cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
    cv2.circle(img,(c[0][0][0],c[0][0][1]), 7, (255, 255, 255), -1)
    cv2.circle(img, (c[7][0][0],c[7][0][1]), 7, (255, 255, 255), -1)
    cv2.circle(img, (c[15][0][0], c[15][0][1]), 7, (255, 255, 255), -1)
    cv2.circle(img, (c[22][0][0], c[22][0][1]), 7, (255, 255, 255), -1)
    cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(img, "center", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # 展示图片
    cv2.imshow("Image", img)
    print(cX, cY)
    cv2.waitKey(0)


