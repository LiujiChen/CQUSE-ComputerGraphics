# 实验要求：
#   1.实现圆的Bresenham画法和中点画法
#   2.实现椭圆的扫描转换
#
import math
import tkinter as tk

# 创建需要使用到的全局变量
circle_select = False
oval_select = False
isPoint = False
param_1 = False
param_2 = False
point = [[0, 0], [0, 0]]  # 用于接收点参数的列表
center = [0, 0]  # 圆的圆心
r = 0  # 圆的半径
a = 0  # 椭圆的长半轴
b = 0  # 椭圆的短半轴


# 处理函数

def drawPixel(x, y):
    canvas_window.create_rectangle(x, y, x, y, fill='black')


def start():
    global isPoint
    isPoint = True


def getPoint(event):
    global isPoint, param_1, param_2, point, r, a, b
    if isPoint:
        param_1 = True
        if param_1 and not param_2:
            drawPixel(event.x, event.y)
            point[0] = [event.x, 700 - event.y]
            param_2 = True
            Lparam_1_point.configure(text=str(point[0]))
            return
        if param_1 and param_2:
            drawPixel(event.x, event.y)
            point[1] = [event.x, 700 - event.y]
            isPoint = param_1 = param_2 = False
            if circle_select:
                r = math.sqrt((point[0][0] - point[1][0]) ** 2 + (point[0][1] - point[1][1]) ** 2)
                Lparam_2_point.configure(text=str(r))
            if oval_select:
                Lparam_2_point.configure(text=str(point[1]))


def selectCircle():
    global circle_select, oval_select, isPoint
    circle_select = True
    oval_select = False
    Lchoose['text'] = '选择需要扫描转换的图形 : 圆'
    Lparam_1['text'] = '圆心坐标 :'
    Lparam_2['text'] = '半径长度 :'
    Bcircle_mid['text'] = '中点画圆算法'
    Bcircle_bresenham['text'] = 'Bresenham圆弧算法'


def selectOval():
    global circle_select, oval_select, isPoint
    circle_select = False
    oval_select = True
    Lchoose['text'] = '选择需要扫描转换的图形 : 椭圆'
    Lparam_1['text'] = '长轴顶点坐标 :'
    Lparam_2['text'] = '短轴顶点坐标 :'
    Bcircle_mid['text'] = '椭圆扫描转换'
    Bcircle_bresenham['text'] = '椭圆扫描转换'


def setParam():
    global isPoint, point
    isPoint = True


def chooseAlgorithm_1():
    if circle_select:
        midCircle()
    if oval_select:
        oval()


def chooseAlgorithm_2():
    if circle_select:
        bresenham()
    if oval_select:
        oval()


# 算法

def drawCircle(x0, y0, xr, yr):
    # 使用1/8圆进行对称，实际画点需要将相对坐标(xr,yr)转化为屏幕坐标
    # drawPixel(xr, yr)
    # drawPixel(yr, xr)
    # drawPixel(yr, -xr)
    # drawPixel(xr, -yr)
    # drawPixel(xr, -yr)
    # drawPixel(-xr, -yr)
    # drawPixel(-yr, -xr)
    # drawPixel(-yr, xr)
    # drawPixel(-xr, yr)
    # 从相对坐标轴转化到实际坐标轴后还需要y=700-y转化为屏幕坐标轴
    drawPixel(xr + x0, 700 - (yr + y0))
    drawPixel(yr + x0, 700 - (xr + y0))
    drawPixel(yr + x0, 700 - (y0 - xr))
    drawPixel(xr + x0, 700 - (y0 - yr))
    drawPixel(x0 - xr, 700 - (y0 - yr))
    drawPixel(x0 - yr, 700 - (y0 - xr))
    drawPixel(x0 - yr, 700 - (y0 + xr))
    drawPixel(x0 - xr, 700 - (yr + y0))


def midCircle():
    global r
    d = 1.25 - r  # 初始化增量
    # 使用相对点进行画图
    xr = 0
    yr = int(r)
    x0 = point[0][0]
    y0 = point[0][1]
    # d1 = 2*(x-y)+5    d>0
    # d2 = 2*x+3        d<=0
    while xr <= yr:

        drawCircle(x0, y0, xr, yr)
        xr += 1
        if d > 0:
            d += 2 * (xr - yr) + 5
            yr -= 1
        else:
            d += 2 * xr + 3


def bresenham():
    global r
    # 使用相对点进行画图
    xr = 0
    yr = int(r)
    x0 = point[0][0]
    y0 = point[0][1]
    dd = 2 * (xr - yr + 1)
    dhd = 2 * (dd + yr) - 1
    dvd = 2 * (dd - xr) - 1
    while xr <= yr:
        # 转化坐标和对称画圆与mid一样
        drawCircle(x0, y0, xr, yr)
        if dd < 0:
            if dhd < 0:
                xr += 1
                dd += 2 * xr + 1
                dhd = 2 * (dd + yr) - 1
                dvd = 2 * (dd - xr) - 1
            else:
                xr += 1
                yr -= 1
                dd += 2 * (xr - yr + 1)
                dhd = 2 * (dd + yr) - 1
                dvd = 2 * (dd - xr) - 1
        elif dd == 0:
            xr += 1
            yr -= 1
            dd += 2 * (xr - yr + 1)
            dhd = 2 * (dd + yr) - 1
            dvd = 2 * (dd - xr) - 1
        else:
            if dvd < 0:
                yr -= 1
                dd += -2 * yr + 1
                dhd = 2 * (dd + yr) - 1
                dvd = 2 * (dd - xr) - 1
            else:
                xr += 1
                yr -= 1
                dd += 2 * (xr - yr + 1)
                dhd = 2 * (dd + yr) - 1
                dvd = 2 * (dd - xr) - 1


def oval():
    # 还需要作出优化，这个函数只在b>a的时候，画出的椭圆比较好，反之在长轴顶点画得很差
    global point, center, a, b
    # 计算出相对坐标系的原点位置(绝对坐标)
    x0 = center[0] = (point[0][0] + point[1][0]) // 2
    y0 = center[1] = (point[0][1] + point[1][1]) // 2
    # print(center)
    # 设置相对坐标(xr,yr)
    a = abs(point[0][0] - center[0])
    b = abs(point[0][1] - center[1])
    xr = 0
    yr = int(b)
    d = b ** 2 + (a ** 2) * (0.25 - b)

    def drawoval():
        # 椭圆只能进行1/4对称
        # drawPixel(xr,yr)
        # drawPixel(xr,-yr)
        # drawPixel(-xr,-yr)
        # drawPixel(-xr,yr)
        # y = 700-y
        drawPixel(xr + x0, 700 - (yr + y0))
        drawPixel(xr + x0, 700 - (y0 - yr))
        drawPixel(x0 - xr, 700 - (y0 - yr))
        drawPixel(x0 - xr, 700 - (yr + y0))

    while (b ** 2) * (xr + 1) < (a ** 2) * (yr - 0.5):

        # 调用函数进行对称画椭圆
        drawoval()
        xr += 1
        if d < 0:
            d += (b ** 2) * (2 * xr + 3)
        else:
            yr -= 1
            d += (b ** 2) * (2 * xr + 3) + (a ** 2) * (-2 * yr + 2)

    d = (b ** 2) * ((xr - 0.5) ** 2) + (a ** 2) * ((yr - 1) ** 2) - (a * b) ** 2
    while yr >= 0:

        # 调用函数进行对称画椭圆
        drawoval()
        yr -= 1
        if d < 0:
            xr += 1
            d += (b ** 2) * 2 * (xr + 2) + (a ** 2) * (-2 * yr + 3)
        else:
            d += (a ** 2) * (-2 * yr + 3)


# 创建GUI
window = tk.Tk()
window.title('圆和椭圆的扫描转换')
window.geometry('700x700+200+20')
window.resizable(False, False)
window.bind("<Button-1>", getPoint)
canvas_window = tk.Canvas(window, width=700, height=700)
canvas_window.pack()

# 标签与按钮
Lchoose = tk.Label(window, text='选择需要扫描转换的图形 :')
Lchoose.place(x=10, y=600)
Bcircle = tk.Button(window, width=15, height=1, text='圆', command=selectCircle)
Bcircle.place(x=10, y=625)
Boval = tk.Button(window, width=15, height=1, text='椭圆', command=selectOval)
Boval.place(x=10, y=660)
Bparam = tk.Button(window, width=15, height=1, text='请选择参数 :', command=start)
Bparam.place(x=150, y=640)
Lparam_1 = tk.Label(window, text='圆心坐标 :')
Lparam_1.place(x=300, y=620)
Lparam_1_point = tk.Label(window, text='0,0')
Lparam_1_point.place(x=380, y=620)
Lparam_2 = tk.Label(window, text='半径长度 :')
Lparam_2.place(x=300, y=660)
Lparam_2_point = tk.Label(window, text='0')
Lparam_2_point.place(x=380, y=660)
Lalgorithms = tk.Label(window, text='选择算法 :')
Lalgorithms.place(x=450, y=640)
Bcircle_mid = tk.Button(window, width=15, height=1, text='中点画圆算法', command=chooseAlgorithm_1)
Bcircle_mid.place(x=550, y=620)
Bcircle_bresenham = tk.Button(window, width=15, height=1, text='Bresenham圆弧算法', command=chooseAlgorithm_2)
Bcircle_bresenham.place(x=550, y=660)
# 运行
window.mainloop()
