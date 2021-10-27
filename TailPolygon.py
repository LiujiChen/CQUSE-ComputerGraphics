import tkinter as tk
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
# 创建一些需要全局使用的量
Egdes = []
XL = XR = YT = YB = 0
windowPoints = [[0, 0], [0, 0]]  # 窗口list
pointList = []
is_choose = True
windowSelect = s = is_Select = False
matrix = np.zeros([700, 700])


# 处理函数
def drawPixel(x, y):
    canvas_window.create_rectangle(x, y, x, y, fill='black')


def choosePoints():
    global is_choose, pointList
    pointList.pop()
    is_choose = False
    for i in range(len(pointList) - 1):
        DDA(pointList[i], pointList[i + 1])
    DDA(pointList[-1], pointList[0])
    # for i in range(len(pointList)):
    #     print(pointList[i])
    # Polygon()
    # print(matrix)


def getPoint(event):
    global pointList,s,windowSelect,windowPoints,is_Select
    if is_choose and not windowSelect:
        # print(event.x, event.y)
        drawPixel(event.x, event.y)
        pointList.append([event.x, 700-event.y])
        # if len(pointList) >= 2:
        #     DDA(pointList[-2], pointList[-1])
    if windowSelect and is_Select:
        if not s:
            windowPoints[0] = [event.x, event.y]
            drawPixel(event.x, event.y)
            # print(event.x, event.y)
            s = True
            return
        if s:
            windowPoints[1] = [event.x, event.y]
            drawPixel(event.x, event.y)
            # print(event.x, event.y)
            is_Select = s = False


def drawWindow():
    global windowPoints, XL, XR, YB, YT, Egdes
    xmin = min(windowPoints[0][0], windowPoints[1][0])
    XL = xmin
    xmax = max(windowPoints[0][0], windowPoints[1][0])
    XR = xmax
    ymin = min(windowPoints[0][1], windowPoints[1][1])
    YT = 700 - ymin
    ymax = max(windowPoints[0][1], windowPoints[1][1])
    YB = 700 - ymax
    # print(windowPoints)
    # print(XL, XR, YB, YT)
    Egdes = [XL, YT, XR, YB]
    canvas_window.create_rectangle(xmin, ymin, xmax, ymax)


def setWindow():
    global windowSelect, is_Select
    windowSelect = True
    is_Select = True

def inside(point,edge):
    if edge==XL:
        if point[0]>=edge:
            return True
        else:
            return False
    elif edge==YT:
        if point[1]>edge:
            return False
        else:
            return True
    elif edge==XR:
        if point[0]>edge:
            return False
        else:
            return True
    elif edge==YB:
        if point[1]>=edge:
            return True
        else:
            return False

def getInterse(point1,point2,edge):
    interse=[0,0]
    if edge==XL:
        interse[0]=XL
        interse[1]= int(point1[1] + (XL-point1[0]) * (point2[1] - point1[1]) / (point2[0] - point1[0]))
    elif edge==YT:
        interse[1]=YT
        interse[0]= int(point1[0] + (YT-point1[1]) * (point2[0] - point1[0]) / (point2[1] - point1[1]))
    elif edge==XR:
        interse[0] = XR
        interse[1] = int(point1[1] + (XR-point1[0]) * (point2[1] - point1[1]) / (point2[0] - point1[0]))
    elif edge==YB:
        interse[1] = YB
        interse[0] = int(point1[0] + (YB-point1[1]) * (point2[0] - point1[0]) / (point2[1] - point1[1]))
    print("求交",point1,point2,edge)
    return interse

# 算法
def DDA(point1, point2):
    global matrix
    dx = float(point2[0] - point1[0])
    dy = float(point2[1] - point1[1])
    k = dy / dx
    if abs(k) <= 1:
        if point1[0] > point2[0]:
            temp = point1
            point1 = point2
            point2 = temp
        x = point1[0]
        y = float(point1[1])
        # print(dx, dy, k, x, y)
        for x in range(point1[0], point2[0]):
            drawPixel(x, 700-int(y))
            matrix[x][int(y)] = 1
            y += k
    else:
        if point1[1] > point2[1]:
            temp = point1
            point1 = point2
            point2 = temp
        k = dx / dy
        y = point1[1]
        x = float(point1[0])
        # print(dx, dy, k, x, y)
        # print(dx, dy, k, x, y)
        for y in range(point1[1], point2[1]):
            drawPixel(int(x), 700-y)
            matrix[int(x)][y] = 1
            x += k

def cut():
    global pointList
    PolygonPoints=[]
    # print(pointList)
    print("检查Edges",Egdes,XL,YT,XR,YB)
    print("原始多边形顶点：",pointList)
    for edge in Egdes:
        print("检查每条edge",edge)
        for i in range(0,len(pointList)):
            if i != len(pointList)-1:
                if inside(pointList[i],edge):
                    if inside(pointList[i+1],edge):
                        PolygonPoints.append(pointList[i+1])
                    else:
                        PolygonPoints.append(getInterse(pointList[i], pointList[i+1], edge))
                else:
                    if inside(pointList[i+1],edge):
                        PolygonPoints.append(getInterse(pointList[i], pointList[i+1], edge))
                        PolygonPoints.append(pointList[i+1])
            else:
                if inside(pointList[-1],edge):
                    if inside(pointList[0],edge):
                        PolygonPoints.append(pointList[0])
                    else:
                        PolygonPoints.append(getInterse(pointList[-1], pointList[0], edge))
                else:
                    if inside(pointList[0],edge):
                        PolygonPoints.append(getInterse(pointList[-1],pointList[0],edge))
                        PolygonPoints.append(pointList[0])
        print("每次循环得到的新多边形顶点：",PolygonPoints)
        pointList=PolygonPoints
        PolygonPoints=[]
    print(pointList)
    for i in range(0,len(pointList)):
        pointList[i][1] = 700-pointList[i][1]
    canvas_window.create_polygon(pointList, outline="black", fill="yellow")



# 创建GUI
window = tk.Tk()
window.title('多边形的裁剪')
window.geometry('700x700+200+20')
window.resizable(False, False)
window.bind("<Button-1>", getPoint)
canvas_window = tk.Canvas(window, width=700, height=700)
canvas_window.pack()

# 标签和按钮
B_choosePoints = tk.Button(window, width=15, height=1, text="选择完毕", command=choosePoints)
B_choosePoints.place(x=10, y=640)
BSetwindow = tk.Button(window, width=15, height=1, text="选择裁剪窗口", command=setWindow)
BSetwindow.place(x=580, y=610)
BDrawwindow = tk.Button(window, width=15, height=1, text="绘制裁剪窗口", command=drawWindow)
BDrawwindow.place(x=580, y=650)
BCut = tk.Button(window, width=15, height=1, text="裁剪", command=cut)
BCut.place(x=150, y=640)
# 运行
window.mainloop()
