#!/usr/bin/python3

class Figure(object):
    total = 0
    figures = []

    @staticmethod
    def status():
        print(" Сейчас существует ", Figure.total, " фигур:")
        for item in Figure.figures:
            print(item)

    def __init__(self, name):
        self.name = name
        Figure.total += 1
        Figure.figures += [name]

class Appearance(object):
    colors = []
    styles = []
    @staticmethod
    def status():
        print(" Цветовая палитра состот из ", len(Appearance.colors), " цветов:")
        for color in Appearance.colors:
            print(" Цвет - ",  color)
        print(" Набор стилей состоит из ",    len(Appearance.styles), " стилей:")
        for style in Appearance.styles:
            print(" Стиль:\n", style)

    def __init__(self, name):
        self.name = name

class Color(Appearance):
    def __init__(self, foreground, background):
        self.color_s = "\033[" + str(foreground) + ";" + str(background) + "m"
        self.color_e = "\033[00m"
        Appearance.__init__(self, self.color_s + "|||||" + self.color_e)
        Appearance.colors += [self.name]

class Style(Appearance):
    # axis - ось
    def __init__(self, filler, point, xaxis, yaxis, center):
        Appearance.__init__(self,"%+15s : [ %3s ]\n" % ("Заполнитель", filler) +
                                 " %+15s : [ %3s ]\n" % ("Точка",        point) +
                                 " %+15s : [ %3s ]\n" % ("Оси(X)",       xaxis) +
                                 " %+15s : [ %3s ]\n" % ("Оси(Y)",       yaxis) +
                                 " %+15s : [ %3s ]\n" % ("Центр",       center))
        Appearance.styles += [self.name]
        self.filler = filler
        self.point  = point
        self.xaxis  = xaxis
        self.yaxis  = yaxis
        self.center = center

class Field(object):
    def __init__(self, sx, ex, sy, ey, line_color, field_color, axis_color, style, indent=4):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.filler = field_color.color_s + style.filler + field_color.color_e
        self.point  = line_color.color_s  + style.point  + line_color.color_e
        self.xaxis = axis_color.color_s  + style.xaxis + axis_color.color_e
        self.yaxis = axis_color.color_s  + style.yaxis + axis_color.color_e
        self.center = axis_color.color_s  + style.center + axis_color.color_e
        self.indent = indent
        self.style = style
        self.col_indent = len(style.filler)
        self.field = []
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

    def ch_line_color(self, line_color):
        self.point  = line_color.color_s  + self.style.point  + line_color.color_e

    def __str__(self):
        res = ""
        rows = self.ey - self.sy
        cols = self.ex - self.sx
        l = [str(abs(i)).ljust(self.col_indent,' ') for i in range(self.sx, self.ex)]
        maxlen = 0
        for item in l:
            if len(item) > maxlen:
                maxlen = len(item)
        for i in range(maxlen):
            print(' ' * (self.indent + 2),end='')
            for item in l:
                print(item[i].ljust(self.col_indent,' '), end='')
            print()

        for i in range(rows):
            res+=" " + str(abs(i + self.sy)).ljust(self.indent,' ')
            for j in range(cols):
               # if self.sy + i == 0 and self.sx + j == 0:
               #     self.field[i][j] = self.center
               # elif self.sy + i == 0:
               #     self.field[i][j] = self.xaxis
               # elif self.sx + j == 0:
               #     self.field[i][j] = self.yaxis
                res += self.field[i][j]
            res+="\n"
        res+="Построено\n"
        return res

class Circle(Figure):
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
    def __init__(self, x, y, side):
        Figure.__init__(self, " Квадратик")
        self.side = abs(side)
        self.x = x
        self.y = y * -1

    def draw(self, field):
        sx = max(self.x + abs(field.sx), 0)
        sy = max(self.y + abs(field.sy), 0)
        ex = min(sx + self.side, field.ex - field.sx)
        ey = min(sy + self.side, field.ey - field.sy)

        for i in range(sy, ey):
            for j in range(sx, ex):
                field.field[i][j] = field.point

class Point(Figure):
    def __init__(self, x, y):
        Figure.__init__(self, " Точечка")
        self.x = x
        self.y = y * -1

    def draw(self, field):
        x = max(self.x + abs(field.sx), -1)
        y = max(self.y + abs(field.sy), -1)
        if x >= 0 and y >= 0 and x < field.ex - field.sx and y < field.ey - field.sy:
            field.field[y][x] = field.point

def main():
    # Appearance config
    color_field = Color(32, 43)
    color_line  = Color(31, 42)
    color_axis  = Color(30, 44)
    mystyle = Style(' .', ' *', ' -', ' |', ' +')
    # Field creation
    myfield = Field(-10, 14, -10, 9, color_line, color_field, color_axis, mystyle)
    # Cyrcle creation
    mycircle = Circle(-7, 5, 3)
    mycircle.draw(myfield)
    # Square creation
    color_line1 = Color(34, 46)
    myfield.ch_line_color(color_line1)
    mysquare = Square(3, 4, 7)
    mysquare.draw(myfield)
    # Point creation
    color_line2 = Color(35, 47)
    myfield.ch_line_color(color_line2)
    mypoint = Point(2, 7)
    mypoint.draw(myfield)
    print(myfield)
    Appearance.status()
    Figure.status()

main()
