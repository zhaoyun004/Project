import tkinter as tk

root = tk.Tk()

canvas =tk.Canvas(root, width=200, height=300)
canvas.pack()

# 画三条直线
line1 = canvas.create_line(0,50,200,50, fill='yellow')
line2 = canvas.create_line(100, 0, 100, 100, fill='red', dash=(4,4))  # 画四个像素停四个像素
line3 = canvas.create_line(0,50,200,50, fill='black')

# 画一个矩形
rect1 = canvas.create_rectangle(50, 25, 150, 75, fill='blue')

# 改变现有图形
canvas.coords(line1, 0, 25, 200, 25)  # 改变尺寸
canvas.itemconfig(rect1, fill='red')  # 改变颜色
canvas.delete(line3)  # 删除图形

canvas.create_rectangle(40, 150, 160, 210, dash=(4, 4))
# 绘制一个椭圆形（实际就是给定一个矩形的坐标，然后进行填充）
canvas.create_oval(40, 150, 160, 210, fill='pink')
# 在指定位置插入一个文本框（坐标指的是中心位置）
canvas.create_text(100, 180, text='NireStudio')

# 创建按键，删除所有图形
button1 = tk.Button(root, text='delete all', command=(lambda x=tk.ALL:canvas.delete(x)))
button1.pack()

tk.mainloop()
