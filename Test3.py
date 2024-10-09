"""
Вариант 26
Фокин Даниил ИСТбд-23

Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных использовать нельзя. При необходимости сохранить информацию в виде файлов, разделяя значения запятыми или пробелами.
Для GUI использовать библиотеку tkinter.

Объекты - квадраты
Функции:
    симметричная сегментация
    визуализация
    раскраска
    поворот вокруг центра
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import math

class Square:
    def __init__(self, size, color, position, angle=0, main_center=None):
        self.size = size
        self.color = color
        self.position = position
        self.angle = angle
        self.main_center = main_center

    def segment(self, padding=0.5):
        half_size = self.size // 2
        x, y = self.position

        new_squares = [
            Square(half_size - padding, self.color, (x, y), main_center=self.main_center),
            Square(half_size - padding, self.color, (x + half_size + padding, y), main_center=self.main_center),
            Square(half_size - padding, self.color, (x, y + half_size + padding), main_center=self.main_center),
            Square(half_size - padding, self.color, (x + half_size + padding, y + half_size + padding), main_center=self.main_center)
        ]
        return new_squares

    def draw(self, canvas):
        x, y = self.position
        half_size = self.size // 2
        center = (x + half_size, y + half_size)

        points = [
            (x, y),
            (x + self.size, y),
            (x + self.size, y + self.size),
            (x, y + self.size)
        ]

        rotation_center = self.main_center if self.main_center else center
        rotated_points = [self.rotate_point(point, rotation_center, math.radians(self.angle)) for point in points]
        flat_points = [coord for point in rotated_points for coord in point]

        canvas.create_polygon(flat_points, fill=self.color)

    def recolor(self, new_color):
        self.color = new_color

    def rotate(self, delta_angle):
        self.angle += delta_angle
        self.angle %= 360

    def rotate_point(self, point, center, angle_rad):
        x, y = point
        cx, cy = center

        x -= cx
        y -= cy

        new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)

        return new_x + cx, new_y + cy

class SquareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Square Manipulation App")
        self.canvas = tk.Canvas(self.root, width=820, height=600, bg='white')
        self.canvas.pack()

        self.squares = []
        self.main_square = None
        self.load_squares_from_file()

        btn_segment = tk.Button(self.root, text="Сегментация", command=self.segment_squares)
        btn_segment.pack(side=tk.LEFT)

        btn_recolor = tk.Button(self.root, text="Раскраска", command=self.recolor_squares)
        btn_recolor.pack(side=tk.LEFT)

        btn_rotate = tk.Button(self.root, text="Поворот", command=self.rotate_squares)
        btn_rotate.pack(side=tk.LEFT)

        self.draw_squares()

    def load_squares_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.split(',')
                    parts = [part.strip() for part in parts]
                    if len(parts) != 4:
                        messagebox.showerror("Ошибка", f"Некорректный формат данных: {line.strip()}.\nКорректный: Размер, Цвет, Позиция x, Позиция y")
                        continue
                    size, color, x, y = parts
                    try:
                        size = int(size)
                        x = int(x)
                        y = int(y)
                    except ValueError:
                        messagebox.showerror("Ошибка", f"Размер, Позиция x и Позиция y должны быть целыми числами: {line.strip()}")
                        continue
                    valid_colors = {"red", "blue", "green", "yellow", "black", "white", "gray"}
                    if color not in valid_colors:
                        messagebox.showerror("Ошибка", f"Некорректные данные: '{color}' в строке: {line.strip()}.\nДопустимые значения:\nred, blue, green, yellow, black, white, gray")
                        continue
                    square = Square(size, color, (x, y))
                    self.squares.append(square)
                    if self.main_square is None:
                        self.main_square = square
                        self.main_center = (x + size // 2, y + size // 2)
                        square.main_center = self.main_center
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def draw_squares(self):
        self.canvas.delete("all")
        for square in self.squares:
            square.draw(self.canvas)

    def segment_squares(self):
        new_squares = []
        for square in self.squares:
            new_squares.extend(square.segment())
        self.squares = new_squares
        self.draw_squares()

    def recolor_squares(self):
        for square in self.squares:
            if square.color == 'red':
                square.recolor('blue')
            elif square.color == 'blue':
                square.recolor('green')
            else:
                square.recolor('red')
        self.draw_squares()

    def rotate_squares(self):
        for square in self.squares:
            square.rotate(45)
        self.draw_squares()

if __name__ == "__main__":
    root = tk.Tk()
    app = SquareApp(root)
    root.mainloop()