import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox

# 创建一些需要全局使用的量
isSelect = select1 = select2 = False
point = [[0, 600], [0, 600]]  # 端点list

# 创建GUI
window = tk.Tk()
window.title('直线的扫描转换')
window.geometry('500x600+200+50')
window.resizable(False, False)

# 创建画布
canvas_window = tk.Canvas(window, width=500, height=600)
canvas_window.pack()


# 处理函数
def draw(x_value, y_value):
    global color
    x1, y1 = (x_value - 1), (y_value - 1)
    x2, y2 = (x_value + 1), (y_value + 1)
    canvas_window.create_rectangle(x1, y1, x2, y2, fill='black')


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
    global isSelect, select1, select2
    if isSelect:
        select1 = True
        if select1 == True and select2 == False:
            point[0] = (event.x, 600 - event.y)
            draw(event.x, event.y)
            # print(event.x,600-event.y)
            select2 = True
            LStart.configure(text=str(point[0]))
            return
        if select1 and select2:
            point[1] = (event.x, 600 - event.y)
            draw(event.x, event.y)
            # print(event.x, 600-event.y)
            LEnd.configure(text=str(point[1]))
            isSelect = select1 = select2 = False
            choosep['text'] = '选择直线段的端点'


# 算法
def DDA():
    dx = float(point[1][0] - point[0][0])
    dy = float(point[1][1] - point[0][1])
    k = dy / dx
    if abs(k) <= 1:
        if point[0][0] > point[1][0]:
            swapPoint()
        x = point[0][0]
        y = float(point[0][1])
        # print(dx, dy, k, x, y)
        for x in range(point[0][0], point[1][0]):
            draw(x, 600 - int(y))
            y += k
    else:
        if point[0][1] > point[1][1]:
            swapPoint()
        k = dx / dy
        y = point[0][1]
        x = float(point[0][0])
        # print(dx, dy, k, x, y)
        for y in range(point[0][1], point[1][1]):
            draw(int(x), 600 - y)
            x += k


def MidPoint():
    b = (point[1][0] - point[0][0])
    a = (point[0][1] - point[1][1])
    # 根据k分为四种情况（主要是增量产生了变化）
    # 0<k<1
    if abs(a) < abs(b) and a * b < 0:
        if point[0][0] > point[1][0]:
            swapPoint()
        b = (point[1][0] - point[0][0])
        a = (point[0][1] - point[1][1])
        d = 2 * a + b
        d1 = 2 * a
        d2 = 2 * (a + b)
        x = point[0][0]
        y = point[0][1]
        draw(x, 600 - y)
        while x < point[1][0]:
            x += 1
            if d < 0:
                d += d2
                y += 1
            else:
                d += d1
            draw(x, 600 - y)
    # -1<k<0
    elif abs(a) < abs(b) and a * b > 0:
        if point[0][0] > point[1][0]:
            swapPoint()
        b = (point[1][0] - point[0][0])
        a = (point[0][1] - point[1][1])
        d = 2 * a - b
        d1 = 2 * (a - b)
        d2 = 2 * a
        x = point[0][0]
        y = point[0][1]
        draw(x, 600 - y)
        while x < point[1][0]:
            x += 1
            if d < 0:
                d += d2

            else:
                d += d1
                y -= 1
            draw(x, 600 - y)
    # k>1
    elif abs(a) > abs(b) and a * b < 0:
        if point[0][1] > point[1][1]:
            swapPoint()
        b = (point[1][0] - point[0][0])
        a = (point[0][1] - point[1][1])
        d = a + 2 * b
        d1 = 2 * (a + b)
        d2 = 2 * b
        x = point[0][0]
        y = point[0][1]
        draw(x, 600 - y)
        while y < point[1][1]:
            y += 1
            if d < 0:
                d += d2

            else:
                d += d1
                x += 1
            draw(x, 600 - y)
    # k<-1
    else:
        if point[0][1] < point[1][1]:
            swapPoint()
        b = (point[1][0] - point[0][0])
        a = (point[0][1] - point[1][1])
        d = 2 * a - b
        d1 = -2 * b
        d2 = 2 * (a - b)
        x = point[0][0]
        y = point[0][1]
        draw(x, 600 - y)
        print(a, b, x, y, d1, d2, d)
        while y > point[1][1]:
            y -= 1
            if d < 0:
                d += d2
                x += 1
            else:
                d += d1
            draw(x, 600 - y)


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
            draw(x, 600 - y)
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
            draw(x, 600 - y)
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
            draw(x, 600 - y)
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
            draw(x, 600 - y)
            y -= 1
            e += 2 * b
            if e > 0:
                x += 1
                e += 2 * a


# 按钮与标签
choosep = tk.Button(window, width=15, height=1, text="选择直线段的端点", command=choosePoint)
choosep.place(x=10, y=510)
LPoint1 = tk.Label(window, text="起点坐标 :")
LPoint1.place(x=10, y=550)
LStart = tk.Label(window, text="0,0")
LStart.place(x=80, y=550)
LPoint2 = tk.Label(window, text="终点坐标 :")
LPoint2.place(x=10, y=570)
LEnd = tk.Label(window, text="0,0")
LEnd.place(x=80, y=570)
BDDA = tk.Button(window, width=15, height=1, text="DDA算法", command=DDA)
BDDA.place(x=350, y=500)
BMid = tk.Button(window, width=15, height=1, text="中点算法", command=MidPoint)
BMid.place(x=350, y=535)
BBresenham = tk.Button(window, width=15, height=1, text="Bressnham", command=Bresenham)
BBresenham.place(x=350, y=570)

# 运行窗口
window.bind("<Button-1>", callback)
window.mainloop()
