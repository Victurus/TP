#!/usr/bin/python3
# Данный скрипт написан по заданию - ООП
# Предмет: Технологии программирования
# Реализованы классы Фигур, Поля отрисовки и Стилей
# Автор: Виктор Давыдов

class Figure(object):
    """ Базовый класс Фигура для подсчёта количества созданных фигур """
    total = 0
    figures = []

    @staticmethod
    def status():
        print(" Сейчас существует ", Figure.total, " фигур(ы):")
        for item in Figure.figures:
            print(item)

    def __init__(self, name):
        self.name = name
        Figure.total += 1
        Figure.figures += [name]

class Appearance(object):
    """ Базовый класс представление для подсчёта статистики стилей и цветов """
    colors = []
    styles = []
    @staticmethod
    def status():
        print(" Цветовая палитра состот из ", len(Appearance.colors), " цветов(а):")
        for color in Appearance.colors:
            print(" Цвет - ",  color, sep='')
        print(" Набор стилей состоит из ",    len(Appearance.styles), " стилей(я):")
        for style in Appearance.styles:
            print(" Стиль:\n", style, sep='')

    def __init__(self, name):
        self.name = name

class Color(Appearance):
    """ Класс задающий цвет консоли UNIX-систем """
    def __init__(self, foreground, background):
        self.color_s = "\033[" + str(foreground) + ";" + str(background) + "m"
        self.color_e = "\033[00m"
        Appearance.__init__(self, self.color_s + "|||||" + self.color_e)
        Appearance.colors += [self.name]

class Style(Appearance):
    """ Класс задающий стиль начертания фигур """
    # axis - ось
    def __init__(self, filler, point, xaxis, yaxis, center):
        Appearance.__init__(self," %+15s : [ %3s ]\n" % ("Заполнитель", filler) +
                                 " %+15s : [ %3s ]\n" % ("Точка",        point) +
                                 " %+15s : [ %3s ]\n" % ("Оси(X)",       xaxis) +
                                 " %+15s : [ %3s ]\n" % ("Оси(Y)",       yaxis) +
                                 " %+15s : [ %3s ]" % ("Центр",       center))
        Appearance.styles += [self.name]
        self.filler = filler
        self.point  = point
        self.xaxis  = xaxis
        self.yaxis  = yaxis
        self.center = center

class Field(object):
    """ Класс поле для отображения фигур """
    def __init__(self, sx, ex, sy, ey, line_color, field_color, axis_color, style, indent=4):
        self.sx = sx   #\
        self.sy = sy   # |> размерность создаваемого
        self.ex = ex   # |> поля
        self.ey = ey   #/
        self.filler = field_color.color_s + style.filler + field_color.color_e # заполнитель поля
        self.point  = line_color.color_s  + style.point  + line_color.color_e  # точка рисуемой фигуры
        self.xaxis  = axis_color.color_s  + style.xaxis  + axis_color.color_e  # \  оси
        self.yaxis  = axis_color.color_s  + style.yaxis  + axis_color.color_e  #  | координат
        self.center = axis_color.color_s  + style.center + axis_color.color_e  # /  и центр координат
        self.indent = indent # отступ цифр координат
        self.style  = style  # запоминание стиля начертания поля и фигур
        self.col_indent = len(style.filler) # отступ между точками поля
        self.field = [] # поле
        for i in range(self.sy, self.ey):
            row = []
            for j in range(self.sx, self.ex):
                if i == j == 0:
                    row += [self.center]
                elif i == 0:
                    row += [self.xaxis]
                elif j == 0:
                    row += [self.yaxis]
                else:
                    row += [self.filler]
            self.field += [row]

    def ch_line_color(self, line_color): # изменение цвета
        self.point  = line_color.color_s  + self.style.point  + line_color.color_e

    def __str__(self):
        res = ""
        rows = self.ey - self.sy # размеры поля
        cols = self.ex - self.sx # в количествах точек по XY
        ### точки вертикального отображения ###
        l = [str(abs(i)).ljust(self.col_indent,' ') for i in range(self.sx, self.ex)]
        maxlen = 0 # поиск цифры максимальной длины
        for item in l:
            if len(item) > maxlen:
                maxlen = len(item)
        ### отпечатка верхнего ряда цифр ###
        for i in range(maxlen):
            print(' ' * (self.indent + 2),end='')
            for item in l:
                print(item[i].ljust(self.col_indent,' '), end='')
            print()
        ### отпечатка поля ###
        for i in range(rows):
            res+=" " + str(abs(i + self.sy)).ljust(self.indent,' ')
            for j in range(cols):
                res += self.field[i][j]
            res+="\n"
        res+=" Построено\n"
        return res

class Circle(Figure):
    """ Класс отрисовки круга с координатами (x, y), радиуса r """
    def __init__(self, x, y, r):
        Figure.__init__(self, " Кружочек")
        self.x = x * -1
        self.y = y
        self.r = abs(r)

    def draw(self, field):
        rows = field.ey - field.sy
        cols = field.ex - field.sx
        rquadro = self.r ** 2
        for i in range(rows):
            for j in range(cols):
                func_val = (field.sy + i + self.y) ** 2 + (field.sx + j + self.x) ** 2
                if func_val == rquadro or func_val == rquadro - 1 or func_val == rquadro + 1:
                    field.field[i][j] = field.point

class Square(Figure):
    """ Класс квадрата с координатами верхнего левого угла - (x, y), со стороной side """
    def __init__(self, x, y, side, filled=True):
        Figure.__init__(self, " Квадратик")
        self.side = abs(side)
        self.x = x
        self.y = y * -1
        self.filled = filled

    def draw(self, field):
        # координаты расположения квадрата на поле(что уместилось)
        sx = max(self.x + abs(field.sx), 0)
        sy = max(self.y + abs(field.sy), 0)
        ex = min(sx + self.side, field.ex - field.sx)
        ey = min(sy + self.side, field.ey - field.sy)
        # реальные координаты квадрата
        snx = self.x + abs(field.sx)
        enx = self.x + abs(field.sx) + self.side - 1
        sny = self.y + abs(field.sy)
        eny = self.y + abs(field.sy) + self.side - 1
        # вывод
        for i in range(sy, ey):
            for j in range(sx, ex):
                if self.filled or i == sny or i == eny or j == snx or j == enx:
                    field.field[i][j] = field.point

class Rectangle(Figure):
    """ Класс прямоугольника с координатами верхнего левого угла - (x, y), со сторонами sidex и sidey """
    def __init__(self, x, y, sidex, sidey, filled=True):
        Figure.__init__(self, " Прямоугольничек")
        self.sidex = abs(sidex)
        self.sidey = abs(sidey)
        self.x = x
        self.y = y * -1
        self.filled = filled

    def draw(self, field):
        # координаты расположения квадрата на поле(что уместилось)
        sx = max(self.x + abs(field.sx), 0)
        sy = max(self.y + abs(field.sy), 0)
        ex = min(sx + self.sidex, field.ex - field.sx)
        ey = min(sy + self.sidey, field.ey - field.sy)
        # реальные координаты квадрата
        snx = self.x + abs(field.sx)
        enx = self.x + abs(field.sx) + self.sidex - 1
        sny = self.y + abs(field.sy)
        eny = self.y + abs(field.sy) + self.sidey - 1
        # вывод
        for i in range(sy, ey):
            for j in range(sx, ex):
                if self.filled or i == sny or i == eny or j == snx or j == enx:
                    field.field[i][j] = field.point

class Point(Figure):
    """ Класс точки на поле с координатами - (x, y) """
    def __init__(self, x, y):
        Figure.__init__(self, " Точечка")
        self.x = x
        self.y = y * -1

    def draw(self, field):
        x = max(self.x + abs(field.sx), -1)
        y = max(self.y + abs(field.sy), -1)
        rows = field.ey - field.sy
        cols = field.ex - field.sx
        if x >= 0 and y >= 0 and x < cols and y < rows:
            field.field[y][x] = field.point

def main():
    # Appearance config
    color_field = Color(32, 43)
    color_line  = Color(31, 42)
    color_axis  = Color(30, 44)
    mystyle = Style(' . ', ' * ', ' - ', ' | ', ' + ')
    # Field creation
    myfield = Field(-10, 14, -10, 9, color_line, color_field, color_axis, mystyle)
    # Cyrcle creation
    mycircle = Circle(-7, 5, 3)
    mycircle.draw(myfield)
    # Square creation
    color_line1 = Color(34, 46)
    myfield.ch_line_color(color_line1)
    mysquare = Square(3, 4, 7, False)
    mysquare.draw(myfield)
    # Point creation
    color_line2 = Color(35, 47)
    myfield.ch_line_color(color_line2)
    mypoint = Point(2, 7)
    mypoint.draw(myfield)
    # Rectangle creation
    color_line3 = Color(32, 40)
    myfield.ch_line_color(color_line3)
    myrectangle = Rectangle(-9, -2, 9, 4, False)
    myrectangle.draw(myfield)
    print(myfield)
    Appearance.status()
    Figure.status()

main()
