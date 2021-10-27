import tkinter as tk

# 创建一些需要全局使用的量
isSelect = select1 = select2 = windowSelect = s = False
point = [[0, 700], [0, 700]]  # 端点list
windowPoints = [[0, 0], [0, 0]]  # 窗口list
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8
XL = XR = YT = YB = 0


# 处理函数
def draw(x, y):
    canvas_window.create_rectangle(x, y, x, y)


def swapPoint():
    global point
    temp = point[0]
    point[0] = point[1]
    point[1] = temp


def choosePoint():
    choosep['text'] = '取消选择'
    global isSelect, point
    point = [[0, 0], [0, 0]]
    LStart.configure(text=str(point[0]))
    LEnd.configure(text=str(point[1]))
    isSelect = True


def callback(event):
    global isSelect, select1, select2, windowPoints, s
    if isSelect and not windowSelect:
        print('yes')
        select1 = True
        if select1 == True and select2 == False:
            point[0] = [event.x, 700 - event.y]
            draw(event.x, event.y)
            # print(event.x,700-event.y)
            select2 = True
            LStart.configure(text=str(point[0]))
            return
        if select1 and select2:
            point[1] = [event.x, 700 - event.y]
            draw(event.x, event.y)
            # print(event.x, 700-event.y)
            LEnd.configure(text=str(point[1]))
            isSelect = select1 = select2 = False
            choosep['text'] = '选择直线段的端点'
    if isSelect and windowSelect:
        # print('yes')
        if not s:
            windowPoints[0] = [event.x, event.y]
            draw(event.x, event.y)
            # print(event.x, event.y)
            s = True
            return
        if s:
            windowPoints[1] = [event.x, event.y]
            draw(event.x, event.y)
            # print(event.x, event.y)
            isSelect = s = False


# 算法
def Bresenham():
    b = (point[1][0] - point[0][0])
    a = -(point[0][1] - point[1][1])
    # 根据k分为四种情况（主要是增量产生了变化）
    # 0<k<1
    if abs(a) < abs(b) and a * b > 0:
        if point[0][0] > point[1][0]:
            swapPoint()
        b = (point[1][0] - point[0][0])
        a = -(point[0][1] - point[1][1])
        x = point[0][0]
        y = point[0][1]
        e = -b
        while x < point[1][0]:
            draw(x, 700 - y)
            x += 1
            e += 2 * a
            if e > 0:
                y += 1
                e -= 2 * b
    # -1<k<0
    if abs(a) < abs(b) and a * b < 0:
        if point[0][0] > point[1][0]:
            swapPoint()
        b = (point[1][0] - point[0][0])
        a = -(point[0][1] - point[1][1])
        x = point[0][0]
        y = point[0][1]
        e = -b
        while x < point[1][0]:
            draw(x, 700 - y)
            x += 1
            e += -2 * a
            if e > 0:
                y -= 1
                e -= 2 * b
    # K>1
    if abs(a) > abs(b) and a * b > 0:
        if point[0][0] > point[1][0]:
            swapPoint()
        b = (point[1][0] - point[0][0])
        a = -(point[0][1] - point[1][1])
        x = point[0][0]
        y = point[0][1]
        e = -a
        while y < point[1][1]:
            draw(x, 700 - y)
            y += 1
            e += 2 * b
            if e > 0:
                x += 1
                e -= 2 * a
    # k<-1
    if abs(a) > abs(b) and a * b < 0:
        if point[0][0] > point[1][0]:
            swapPoint()
        b = (point[1][0] - point[0][0])
        a = -(point[0][1] - point[1][1])
        x = point[0][0]
        y = point[0][1]
        e = -a
        while y > point[1][1]:
            draw(x, 700 - y)
            y -= 1
            e += 2 * b
            if e > 0:
                x += 1
                e += 2 * a


def setWindow():
    global windowSelect, isSelect
    windowSelect = True
    isSelect = True


def encode(Point):
    c = 0
    if Point[0] < XL:
        c = c | LEFT
    if Point[0] > XR:
        c = c | RIGHT
    if Point[1] > YT:
        c = c | TOP
    if Point[1] < YB:
        c = c | BOTTOM
    return c


def cut():
    global point
    c1 = encode(point[0])
    c2 = encode(point[1])
    x1 = point[0][0]
    x2 = point[1][0]
    y1 = point[0][1]
    y2 = point[1][1]
    x = y = 0
    # print(encode(point[0]))
    # print(encode(point[1]))
    while c1 != 0 or c2 != 0:
        if c2 & c1 != 0:
            point[1]=point[0]=[0,0]
            return
        c=c1
        if c1 == 0:
            c = c2
        if LEFT & c != 0:
            x = XL
            y = y1 + (y2 - y1) * (XL - x1) / (x2 - x1)
        elif RIGHT & c != 0:
            x = XR
            y = y1 + (y2 - y1) * (XR - x1) / (x2 - x1)
        elif BOTTOM & c != 0:
            y = YB
            x = x1 + (x2 - x1) * (YB - y1) / (y2 - y1)
        elif TOP & c != 0:
            y = YT
            x = x1 + (x2 - x1) * (YT - y1) / (y2 - y1)
        if c == c1:
            point[0][0] = int(x)
            point[0][1] = int(y)
            c1 = encode([x, y])
        else:
            point[1][0] = int(x)
            point[1][1] = int(y)
            c2 = encode([x, y])


def drawWindow():
    global windowPoints, XL, XR, YB, YT
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
    canvas_window.create_rectangle(xmin, ymin, xmax, ymax)


# 创建GUI
window = tk.Tk()
window.title('多边形的裁剪')
window.geometry('700x700+200+50')
window.resizable(False, False)

# 创建画布
canvas_window = tk.Canvas(window, width=700, height=700)
canvas_window.pack()

# 按钮与标签
choosep = tk.Button(window, width=15, height=1, text="选择直线段的端点", command=choosePoint)
choosep.place(x=10, y=610)
LPoint1 = tk.Label(window, text="起点坐标 :")
LPoint1.place(x=10, y=650)
LStart = tk.Label(window, text="0,0")
LStart.place(x=80, y=650)
LPoint2 = tk.Label(window, text="终点坐标 :")
LPoint2.place(x=10, y=670)
LEnd = tk.Label(window, text="0,0")
LEnd.place(x=80, y=670)
BBresenham = tk.Button(window, width=15, height=1, text="Bressnham", command=Bresenham)
BBresenham.place(x=150, y=610)
BCut = tk.Button(window, width=15, height=1, text="裁剪", command=cut)
BCut.place(x=150, y=650)
BSetwindow = tk.Button(window, width=15, height=1, text="选择裁剪窗口", command=setWindow)
BSetwindow.place(x=580, y=610)
BDrawwindow = tk.Button(window, width=15, height=1, text="绘制裁剪窗口", command=drawWindow)
BDrawwindow.place(x=580, y=650)
# 运行
window.bind("<Button-1>", callback)
window.mainloop()
