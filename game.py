from tkinter import *
from msvcrt import getch
import math

class Minimap:
    #Движение
    cur_pos = 1 #Текущая клетка
    X_cur = 0   #Текущая координата X
    Y_cur = 0   #Текущая координата Y

    way = {1: {'X':0, 'Y':0, 'S':'C'}} #Клетки: X, Y - координаты. S - статус ('V' - посещенная, 'N' - непосещенная, 'C' - текущая)
    max_pos = 1

    centr_cell_id = 1
    
    def __init__(self, root, canvas):      
        self.canvas = canvas
        self.root = root
        #Связывание событий с нажатием клавиш
        self.root.bind("<Up>", self.UpKey)
        self.root.bind("<Down>", self.DownKey)
        self.root.bind("<Left>", self.LeftKey)
        self.root.bind("<Right>", self.RightKey)
        
        #Очертания карты
        map_size = [self.canvas.winfo_width() // 3.5, self.canvas.winfo_height() // 5]
        self.canvas.create_line(map_size[0], map_size[1], self.canvas.winfo_width() - map_size[0], map_size[1], width=5)
        self.canvas.create_line(self.canvas.winfo_width() - map_size[0], map_size[1], self.canvas.winfo_width() - map_size[0], self.canvas.winfo_height() - map_size[1], width=5)
        self.canvas.create_line(map_size[0], self.canvas.winfo_height() - map_size[1], self.canvas.winfo_width() - map_size[0], self.canvas.winfo_height() - map_size[1], width=5)
        self.canvas.create_line(map_size[0], map_size[1], map_size[0], self.canvas.winfo_height() - map_size[1], width=5)

        #Сетка       
        self.X_len = math.sqrt(math.pow(self.canvas.winfo_width() - 2 * map_size[0], 2)) / 5 #Ширина одной клетки миникарты
        self.Y_len = math.sqrt(math.pow(self.canvas.winfo_height() - 2 * map_size[1], 2)) / 5 #Высота одной клетки миникарты
        for x in range(1, 5):
            self.canvas.create_line(map_size[0], map_size[1] + x * self.Y_len, self.canvas.winfo_width() - map_size[0], map_size[1] + x * self.Y_len)
        for y in range(1, 5):
            self.canvas.create_line(map_size[0] + y * self.X_len, map_size[1], map_size[0] + y * self.X_len, self.canvas.winfo_height() - map_size[1])

        self.centr_cell = [map_size[0] + 2 * self.X_len, map_size[1] + 2 * self.Y_len] #Координаты верхнего левого угла центральной клетки (0;0) ЦЕНТРАЛЬНАЯ КЛЕТКА БУДЕТ МЕНЯТЬСЯ 
        self.canvas.create_rectangle(self.centr_cell[0],self.centr_cell[1], self.centr_cell[0] + self.X_len, self.centr_cell[1] + self.Y_len, fill="red") #Заполнение центральной клетки
        
        ###############____Для отладки____#################
        self.debug1 = self.canvas.create_text(30,10,font=("Times New Roman","10"),text="cur_pos={}".format(self.cur_pos))
        self.debug2 = self.canvas.create_text(30,25,font=("Times New Roman","10"),text="X_cur={}".format(self.X_cur))
        self.debug3 = self.canvas.create_text(30,40,font=("Times New Roman","10"),text="Y_cur={}".format(self.Y_cur))
        ###################################################

    #Окрашивание посещаемых клеток (красный цвет - текущая клетка, зеленый - посещенные, нет цвета - непосещенные)
    def VisitPaint(self):
        for w in self.way: #Сделать замену центральной клетки и смещение в зависимости от стороны, за которую пытаются зайти
            if self.way[w]['S'] == 'C':
                self.canvas.create_rectangle(self.centr_cell[0] + self.X_len * (self.way[w]['Y'] - self.way[self.centr_cell_id]['Y']),
                                             self.centr_cell[1] - self.Y_len * (self.way[w]['X'] - self.way[self.centr_cell_id]['X']),
                                             self.centr_cell[0] + self.X_len * (self.way[w]['Y'] - self.way[self.centr_cell_id]['Y']) + self.X_len,
                                             self.centr_cell[1] - self.Y_len * (self.way[w]['X'] - self.way[self.centr_cell_id]['X']) + self.Y_len,
                                             fill="red")
            if self.way[w]['S'] == 'V':
                #self.canvas.create_rectangle(self.centr_cell[0] + self.X_len * self.way[w]['Y'],
                #                             self.centr_cell[1] - self.Y_len * self.way[w]['X'],
                #                             self.centr_cell[0] + self.X_len * self.way[w]['Y'] + self.X_len,
                #                             self.centr_cell[1] - self.Y_len * self.way[w]['X'] + self.Y_len,
                #                             fill="green")
                self.canvas.create_rectangle(self.centr_cell[0] + self.X_len * (self.way[w]['Y'] - self.way[self.centr_cell_id]['Y']),
                                             self.centr_cell[1] - self.Y_len * (self.way[w]['X'] - self.way[self.centr_cell_id]['X']),
                                             self.centr_cell[0] + self.X_len * (self.way[w]['Y'] - self.way[self.centr_cell_id]['Y']) + self.X_len,
                                             self.centr_cell[1] - self.Y_len * (self.way[w]['X'] - self.way[self.centr_cell_id]['X']) + self.Y_len,
                                             fill="green")


    #Обновление позиции (номера текущей клетки) и статуса клетки
    def CurRefresh(self):
        for w in self.way:
            if self.X_cur == self.way[w]['X'] and self.Y_cur == self.way[w]['Y']:
                self.way[self.cur_pos]['S'] = 'V'
                self.cur_pos = w
                self.way[self.cur_pos]['S'] = 'C'
                return
        self.way[self.cur_pos]['S'] = 'V'    
        self.max_pos += 1        
        self.way[self.max_pos] = {'X':self.X_cur, 'Y':self.Y_cur, 'S':'C'}
        self.cur_pos = self.max_pos
        #print(self.way)

    #Функция для блокировки повторного вызова события при нажатии клавиш
    def Ignore(self, event):
        return "break"

    #Бинд с функцией игнорирования
    def KeyIgnore(self):
        self.root.bind("<Up>", self.Ignore)
        self.root.bind("<Down>", self.Ignore)
        self.root.bind("<Left>", self.Ignore)
        self.root.bind("<Right>", self.Ignore)    
    
    #Обработчики событий нажатия на клавишу
    def UpKey(self, event):
        self.KeyIgnore()
        self.X_cur += 1
        self.CurRefresh() #Обновление позиции
        self.VisitPaint()
        self.canvas.after(500, self.ReBind)
    def DownKey(self, event):
        self.KeyIgnore()
        self.X_cur -= 1
        self.CurRefresh() #Обновление позиции
        self.VisitPaint()
        self.canvas.after(500, self.ReBind)
    def LeftKey(self, event):
        self.KeyIgnore()
        self.Y_cur -= 1
        self.CurRefresh() #Обновление позиции
        self.VisitPaint()
        self.canvas.after(500, self.ReBind)
    def RightKey(self, event):
        self.KeyIgnore()
        self.Y_cur += 1
        self.CurRefresh() #Обновление позиции
        self.VisitPaint()
        self.canvas.after(500, self.ReBind)

    #Повторный бинд после нажатия клавиши, обновление текста отладки
    def ReBind(self):
        self.canvas.itemconfig(self.debug1, text="cur_pos={}".format(self.cur_pos))
        self.canvas.itemconfig(self.debug2, text="X_cur={}".format(self.X_cur))
        self.canvas.itemconfig(self.debug3, text="Y_cur={}".format(self.Y_cur))
        self.root.bind("<Up>", self.UpKey)
        self.root.bind("<Down>", self.DownKey)
        self.root.bind("<Left>", self.LeftKey)
        self.root.bind("<Right>", self.RightKey)
        print(self.max_pos)
        print(self.way)

    

root = Tk()
root.title("ABCDEFG")
root.update_idletasks()
k = 1
w = 1024
h = 768
x = (root.winfo_screenwidth() // 2) - (w // 2)
y = (root.winfo_screenheight() // 2) - (h // 2)
root.geometry("{}x{}+{}+{}".format(w, h, x, y))
root.resizable(False, False)

#2 канваса
main = Canvas(root,width=1000*k,height=600*k,bg="white")
main.grid(row=0,column=0)
bottombar = Canvas(root,width=1024*k,height=168*k,bg="lightblue")
bottombar.grid(row=1,column=0)
main.update()
bottombar.update()

minimap = Minimap(root, main)

#img = PhotoImage(file="./new_new.gif")
#for x in range(0, 700*k, 104):
#    for y in range(0, 350*k, 60):
#        main.create_image(x, y, image=img, anchor='nw') #заполнить канвас изображением


root.mainloop()



