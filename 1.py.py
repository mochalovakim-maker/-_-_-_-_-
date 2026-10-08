"""
Программа для построения фракталов:
- Ковёр Серпинского
- Кривая Коха
- Снежинка Коха
- Салфетка Серпинского
- Кривая Серпинского
- Кривая Гильберта
"""

import tkinter as tk  # Библиотека для создания графического интерфейса
from tkinter import colorchooser  # Диалог выбора цвета
import math  # Для тригонометрических функций (sin, cos, atan2)


class FractalApp:
    def __init__(self, root):
        # Сохраняем ссылку на главное окно
        self.root = root
        # Устанавливаем заголовок окна
        self.root.title("Фракталы")
        # Задаём размер окна (ширина 1200, высота 800)
        self.root.geometry("1200x800")
        
        # Переменная для хранения выбранного типа фрактала (по умолчанию "carpet")
        self.fractal_type = tk.StringVar(value="carpet")
        # Цвет фигуры по умолчанию - чёрный
        self.color = "black"
        # Цвет фона по умолчанию - белый
        self.bg_color = "white"
        # Глубина рекурсии по умолчанию - 3
        self.depth = 3
        
        # Начальные координаты для кривых Коха
        self.start_x = 300  # Начальная точка по X
        self.start_y = 350  # Начальная точка по Y
        self.end_x = 500    # Конечная точка по X
        self.end_y = 350    # Конечная точка по Y
        self.length = 300   # Длина стороны для ковра и салфетки
        
        # Текущие координаты для рисования линий для построение кривых серпинского и гильберта
        self.current_x = 0  # Текущая X
        self.current_y = 0  # Текущая Y
        self.dx = 0  # Приращение по X для одного отрезка
        self.dy = 0  # Приращение по Y для одного отрезка
        
        # Создаём все кнопки и поля ввода
        self.create_widgets()
        # Рисуем фрактал
        self.draw()
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Левая панель с настройками (рамка с выпуклым краем)
        panel = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        # Размещаем панель слева, с отступами, растягиваем по вертикали
        panel.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        
        # Заголовок над радиокнопками
        tk.Label(panel, text="Выберите фрактал:", font=("Arial", 10, "bold")).pack(pady=(10,5))
        
        # Список всех фракталов в виде кортежей (название, значение)
        fractals = [
            ("Ковёр Серпинского", "carpet"),
            ("Кривая Коха", "koch"),
            ("Снежинка Коха", "snowflake"),
            ("Салфетка Серпинского", "sierpinski"),
            ("Кривая Серпинского", "serpinsky_curve"),
            ("Кривая Гильберта", "hilbert")
        ]
        
        # Создаём радиокнопку для каждого фрактала
        for text, value in fractals:
            rb = tk.Radiobutton(panel, text=text, variable=self.fractal_type,
                                value=value, command=self.draw)
            rb.pack(anchor=tk.W, padx=10)  # anchor=tk.W - выравнивание по левому краю
        
        # Текст перед полем ввода глубины
        tk.Label(panel, text="Глубина рекурсии:", font=("Arial", 10)).pack(pady=(15,0))
        
        # Поле для ввода числа (глубина рекурсии)
        self.depth_entry = tk.Entry(panel, width=10, font=("Arial", 10))
        self.depth_entry.insert(0, "3")  # Значение по умолчанию
        self.depth_entry.pack(pady=5)
        
        # Кнопка применения глубины
        tk.Button(panel, text="Применить глубину", command=self.apply_depth,
                  bg="#3498db", fg="white", width=15).pack(pady=5)
        
        # Рамка для группировки полей с координатами
        coord_frame = tk.LabelFrame(panel, text="Координаты", font=("Arial", 9, "bold"))
        coord_frame.pack(fill=tk.X, padx=10, pady=10)  # fill=tk.X - растягиваем по ширине
        
        # Поле для начальной X
        tk.Label(coord_frame, text="Начальная X:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.start_x_entry = tk.Entry(coord_frame, width=8)
        self.start_x_entry.insert(0, "300")
        self.start_x_entry.grid(row=0, column=1, padx=5)
        
        # Поле для начальной Y
        tk.Label(coord_frame, text="Начальная Y:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.start_y_entry = tk.Entry(coord_frame, width=8)
        self.start_y_entry.insert(0, "350")
        self.start_y_entry.grid(row=1, column=1, padx=5)
        
        # Поле для конечной X
        tk.Label(coord_frame, text="Конечная X:").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.end_x_entry = tk.Entry(coord_frame, width=8)
        self.end_x_entry.insert(0, "500")
        self.end_x_entry.grid(row=2, column=1, padx=5)
        
        # Поле для конечной Y
        tk.Label(coord_frame, text="Конечная Y:").grid(row=3, column=0, sticky=tk.W, padx=5)
        self.end_y_entry = tk.Entry(coord_frame, width=8)
        self.end_y_entry.insert(0, "350")
        self.end_y_entry.grid(row=3, column=1, padx=5)
        
        # Поле для длины стороны ковра/салфетки
        tk.Label(coord_frame, text="Длина стороны:").grid(row=4, column=0, sticky=tk.W, padx=5)
        self.length_entry = tk.Entry(coord_frame, width=8)
        self.length_entry.insert(0, "300 ")
        self.length_entry.grid(row=4, column=1, padx=5)
        
        # Кнопка применения координат
        tk.Button(coord_frame, text="Применить координаты", command=self.apply_coords,
                  bg="#3498db", fg="white", width=15).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Текст для выбора цвета фигуры
        tk.Label(panel, text="Цвет фигуры:", font=("Arial", 10)).pack(pady=(10,0))
        
        # Кнопка выбора цвета фигуры
        self.color_btn = tk.Button(panel, text="Выбрать цвет", command=self.choose_color,
                                    bg=self.color, fg="white", width=15)
        self.color_btn.pack(pady=5)
        
        # Текст для выбора цвета фона
        tk.Label(panel, text="Цвет фона:", font=("Arial", 10)).pack(pady=(10,0))
        
        # Кнопка выбора цвета фона
        self.bg_btn = tk.Button(panel, text="Выбрать фон", command=self.choose_bg_color,
                                 bg=self.bg_color, width=15)
        self.bg_btn.pack(pady=5)
        
        # Главная кнопка построения фрактала
        tk.Button(panel, text="ПОСТРОИТЬ", command=self.draw,
                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                  width=15, height=2).pack(pady=15)
        
        # Рамка для холста 
        canvas_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=3)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Холст для рисования
        self.canvas = tk.Canvas(canvas_frame, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Заполняет всю рамку
        
        # При изменении размера окна перерисовываем фрактал
        self.canvas.bind('<Configure>', lambda e: self.draw())
    
    def apply_depth(self):
        """Применяет введённую глубину рекурсии"""
        try:
            # Считываем значение из поля и преобразуем в число
            self.depth = int(self.depth_entry.get())
            self.draw()  # Перерисовываем фрактал с новой глубиной
        except ValueError:
            # Если введено не число, оставляем значение по умолчанию
            self.depth = 3
    
    def apply_coords(self):
        """Применяет введённые координаты"""
        try:
            # Считываем все координаты из полей ввода
            self.start_x = int(self.start_x_entry.get())
            self.start_y = int(self.start_y_entry.get())
            self.end_x = int(self.end_x_entry.get())
            self.end_y = int(self.end_y_entry.get())
            self.length = int(self.length_entry.get())
            self.draw()  # Перерисовываем с новыми координатами
        except ValueError:
            # Если введены не числа, игнорируем
            pass
    
    def choose_color(self):
        """Открывает окно выбора цвета для фигуры"""
        # askcolor возвращает кортеж (RGB, HEX), берем HEX
        color = colorchooser.askcolor(color=self.color)
        if color[1]:  # Если пользователь выбрал цвет (не нажал Отмена)
            self.color = color[1]  # Сохраняем цвет
            self.color_btn.config(bg=self.color)  # Меняем цвет кнопки
            self.draw()  # Перерисовываем фрактал
    
    def choose_bg_color(self):
        """Открывает диалог выбора цвета для фона"""
        color = colorchooser.askcolor(color=self.bg_color)
        if color[1]:
            self.bg_color = color[1]  # Сохраняем цвет фона
            self.bg_btn.config(bg=self.bg_color)  # Меняем цвет кнопки
            self.canvas.config(bg=self.bg_color)  # Меняем цвет холста
            self.draw()  # Перерисовываем фрактал
    
    # ==================== КОВЁР СЕРПИНСКОГО ====================
    def draw_carpet_recursive(self, x, y, size, depth):
        """Рекурсивное построение ковра Серпинского"""
        # Если размер меньше 1 пикселя - не рисуем 
        if size < 1:
            return
        # Базовый случай глубина 0 - рисуем один квадрат
        if depth == 0:
            self.canvas.create_rectangle(x, y, x+size, y+size, fill=self.color, outline=self.color)
        else:
            # Рекурсивный случай: делим квадрат на 9 частей
            new_size = size / 3  # Новая сторона в 3 раза меньше
            # Перебираем все 9 подквадратов (3 строки, 3 столбца)
            for row in range(3):
                for col in range(3):
                    # Пропускаем центральный квадрат (row=1, col=1) - это дырка
                    if row == 1 and col == 1:
                        continue
                    # Рекурсивно вызываем для каждого из 8 квадратов
                    self.draw_carpet_recursive(x + col*new_size, y + row*new_size, new_size, depth-1)
    
    def draw_carpet(self):
        """Подготовка и запуск построения ковра Серпинского"""
        # Получаем текущие размеры холста
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        # Если холст слишком маленький - не рисуем
        if w <= 10 or h <= 10:
            return
        
        # Определяем размер квадрата
        if self.length > 0 and self.length < min(w, h):
            size = self.length  # Используем заданную пользователем длину
            x = (w - size) / 2  # Центрируем по горизонтали
            y = (h - size) / 2  # Центрируем по вертикали
        else:
            # Автоматический размер с отступом 60 пикселей от краёв
            size = min(w, h) - 60
            x = (w - size) / 2
            y = (h - size) / 2
        
        # Запускаем рекурсивное построение
        self.draw_carpet_recursive(x, y, size, self.depth)
        # Рисуем внешнюю рамку
        self.canvas.create_rectangle(x, y, x+size, y+size, outline="gray", width=1)
    
    # ==================== КРИВАЯ КОХА ====================
    def koch_line(self, x1, y1, x2, y2, depth):
        """Рекурсивное построение кривой Коха"""
        # Базовый случай: глубина 0 - рисуем прямую линию
        if depth == 0:
            self.canvas.create_line(x1, y1, x2, y2, fill=self.color, width=2)
        else:
            # Вычисляем разницу между концами отрезка
            dx = x2 - x1
            dy = y2 - y1
            # Длина всего отрезка
            length = math.sqrt(dx*dx + dy*dy)
            
            # Точка на 1/3 от начала
            xA = x1 + dx / 3
            yA = y1 + dy / 3
            
            # Точка на 2/3 от начала
            xB = x2 - dx / 3
            yB = y2 - dy / 3
            
            # Угол наклона отрезка (чтобы построить зубец под углом 60 градусов независимо от направления исходного отрезка)
            angle = math.atan2(dy, dx)
            
            # Вершина зубца: поворачиваем на 60 градусов
            xC = xA + (length / 3) * math.cos(angle - math.pi/3)
            yC = yA + (length / 3) * math.sin(angle - math.pi/3)
            
            # Рекурсивно рисуем 4 маленьких отрезка
            self.koch_line(x1, y1, xA, yA, depth-1)
            self.koch_line(xA, yA, xC, yC, depth-1)
            self.koch_line(xC, yC, xB, yB, depth-1)
            self.koch_line(xB, yB, x2, y2, depth-1)
    
    def draw_koch(self):
        """Построение кривой Коха от начальной до конечной точки"""
        self.koch_line(self.start_x, self.start_y, self.end_x, self.end_y, self.depth)
    
    # ==================== СНЕЖИНКА КОХА ====================
    def draw_snowflake(self):
        """Построение снежинки Коха (три кривые Коха в треугольнике)"""
        # Вычисляем центр снежинки
        cx = (self.start_x + self.end_x) / 2
        cy = (self.start_y + self.end_y) / 2
        # Радиус описанной окружности
        radius = abs(self.end_x - self.start_x) / 2
        
        # Вычисляем координаты трёх вершин равностороннего треугольника
        points = []
        for i in range(3):
            # Углы: -90°, 30°, 150° (повёрнутые для правильной ориентации)
            angle = i * 2 * math.pi / 3 - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))
        
        # Рисуем три стороны треугольника как кривые Коха
        self.koch_line(points[0][0], points[0][1], points[1][0], points[1][1], self.depth)
        self.koch_line(points[1][0], points[1][1], points[2][0], points[2][1], self.depth)
        self.koch_line(points[2][0], points[2][1], points[0][0], points[0][1], self.depth)
    
    # ==================== САЛФЕТКА СЕРПИНСКОГО ====================
    def draw_sierpinski_recursive(self, x1, y1, x2, y2, x3, y3, depth):
        """Рекурсивное построение треугольника Серпинского (салфетки)"""
        # Базовый случай: глубина 0 - рисуем треугольник
        if depth == 0:
            self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=self.color, outline=self.color)
        else:
            # Вычисляем середины сторон треугольника
            x12 = (x1 + x2) / 2  # Середина между вершиной 1 и 2
            y12 = (y1 + y2) / 2
            x23 = (x2 + x3) / 2  # Середина между вершиной 2 и 3
            y23 = (y2 + y3) / 2
            x31 = (x3 + x1) / 2  # Середина между вершиной 3 и 1
            y31 = (y3 + y1) / 2
            
            # Рекурсивно рисуем 3 угловых треугольника
            # Центральный треугольник не рисуется (получается дырка)
            self.draw_sierpinski_recursive(x1, y1, x12, y12, x31, y31, depth-1)
            self.draw_sierpinski_recursive(x12, y12, x2, y2, x23, y23, depth-1)
            self.draw_sierpinski_recursive(x31, y31, x23, y23, x3, y3, depth-1)
    
    def draw_sierpinski(self):
        """Подготовка и запуск построения салфетки Серпинского"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return
        
        # Определяем размер треугольника
        if self.length > 0:
            side = self.length  # Используем заданную длину
        else:
            side = min(w, h) - 100  # Автоматический размер
        
        cx = w / 2  # Центр по горизонтали
        cy = h / 2  # Центр по вертикали
        
        # Координаты вершин равностороннего треугольника
        x1 = cx                # Верхняя вершина
        y1 = cy - side * 0.5
        x2 = cx - side * 0.5   # Левая нижняя вершина
        y2 = cy + side * 0.5
        x3 = cx + side * 0.5   # Правая нижняя вершина
        y3 = cy + side * 0.5
        
        # Запускаем рекурсию
        self.draw_sierpinski_recursive(x1, y1, x2, y2, x3, y3, self.depth)
    
    # ==================== КРИВАЯ СЕРПИНСКОГО ====================
    def draw_and_update(self, dx, dy):
        """Рисует линию от текущей позиции до новой и обновляет координаты"""
        self.canvas.create_line(self.current_x, self.current_y,
                                self.current_x + dx, self.current_y + dy,
                                fill=self.color, width=2)
        self.current_x += dx  # Смещаем текущую позицию
        self.current_y += dy
    
    def r(self, depth):
        """Строит правую верхнюю часть кривой Серпинского"""
        if depth > 0:
            depth -= 1
            self.r(depth)                          # Рекурсивно строим часть
            self.draw_and_update(self.dx, self.dy)  # Отрезок вниз вправо
            self.d(depth)                          # Поворот вниз
            self.draw_and_update(2 * self.dx, 0)    # Горизонтальный отрезок
            self.u(depth)                          # Поворот вверх
            self.draw_and_update(self.dx, -self.dy) # Отрезок вверх-вправо
            self.r(depth)                          # Завершаем сторону
    
    def d(self, depth):
        """Строит правую нижнюю часть кривой Серпинского"""
        if depth > 0:
            depth -= 1
            self.d(depth)                          # Рекурсивно строим часть
            self.draw_and_update(-self.dx, self.dy) # Отрезок вниз-влево
            self.l(depth)                          # Поворот влево
            self.draw_and_update(0, 2 * self.dy)    # Вертикальный отрезок
            self.r(depth)                          # Поворот вправо
            self.draw_and_update(self.dx, self.dy)  # Отрезок вправо-вниз
            self.d(depth)                          # Завершаем сторону
    
    def l(self, depth):
        """Строит левую нижнюю часть кривой Серпинского"""
        if depth > 0:
            depth -= 1
            self.l(depth)                          # Рекурсивно строим часть
            self.draw_and_update(-self.dx, -self.dy) # Отрезок влево-вверх
            self.u(depth)                          # Поворот вверх
            self.draw_and_update(-2 * self.dx, 0)   # Горизонтальный отрезок влево
            self.d(depth)                          # Поворот вниз
            self.draw_and_update(-self.dx, self.dy) # Отрезок влево-вниз
            self.l(depth)                          # Завершаем сторону
    
    def u(self, depth):
        """Строит левую верхнюю часть кривой Серпинского"""
        if depth > 0:
            depth -= 1
            self.u(depth)                          # Рекурсивно строим часть
            self.draw_and_update(self.dx, -self.dy) # Отрезок вверх-вправо
            self.r(depth)                          # Поворот вправо
            self.draw_and_update(0, -2 * self.dy)   # Вертикальный отрезок вверх
            self.l(depth)                          # Поворот влево
            self.draw_and_update(-self.dx, -self.dy) # Отрезок влево-вверх
            self.u(depth)                          # Завершаем сторону
    
    def draw_serpinsky_curve(self):
        """Построение кривой Серпинского"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return
        
        # Количество отрезков на грани 
        count = 2 ** (self.depth + 2) - 2
        # Длина одного шага
        step_length = (w / 2) / count
        
        # Приращения для каждого отрезка
        self.dx = step_length
        self.dy = step_length
        
        # Начальная позиция
        self.current_x = (w - self.dx * count) / 2 + self.dx
        self.current_y = (h - self.dy * count) / 2
        
        # Строим четыре стороны кривой с соединительными отрезками
        self.r(self.depth)
        self.draw_and_update(self.dx, self.dy)
        self.d(self.depth)
        self.draw_and_update(-self.dx, self.dy)
        self.l(self.depth)
        self.draw_and_update(-self.dx, -self.dy)
        self.u(self.depth)
        self.draw_and_update(self.dx, -self.dy)
    
    # ==================== КРИВАЯ ГИЛЬБЕРТА ====================
    def hilbert_line(self, depth, dx, dy):
        """Рекурсивное построение кривой Гильберта"""
        # Первая часть: повёрнутая подкова
        if depth > 0:
            self.hilbert_line(depth - 1, dy, dx)  # Меняем dx и dy местами (поворот)
        
        # Соединительный отрезок
        self.draw_and_update(dx, dy)
        
        # Вторая часть: обычная подкова
        if depth > 0:
            self.hilbert_line(depth - 1, dx, dy)
        
        # Соединительный отрезок (поворот на 90 градусов)
        self.draw_and_update(dy, dx)
        
        # Третья часть: обычная подкова
        if depth > 0:
            self.hilbert_line(depth - 1, dx, dy)
        
        # Соединительный отрезок (обратное направление)
        self.draw_and_update(-dx, -dy)
        
        # Четвёртая часть: повёрнутая в другую сторону подкова
        if depth > 0:
            self.hilbert_line(depth - 1, -dy, -dx)
    
    def draw_hilbert_curve(self):
        """Построение кривой Гильберта"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return
        
        # Размер квадрата для кривой
        square_size = w / 2
        start_x = (w - square_size) / 2
        start_y = start_x
        
        # Количество отрезков для данной глубины
        step_count = 2 ** (self.depth + 1) - 1
        # Длина одного шага
        step = square_size / step_count
        
        # Начальная позиция
        self.current_x = start_x
        self.current_y = start_y
        
        # Направление движения (горизонтальное)
        self.dx = step
        self.dy = 0
        
        # Запускаем рекурсивное построение
        self.hilbert_line(self.depth, self.dx, self.dy)
    
    # ==================== ГЛАВНЫЙ МЕТОД ====================
    def draw(self):
        """Главный метод, вызываемый при нажатии кнопки ПОСТРОИТЬ"""
        # Очищаем холст
        self.canvas.delete("all")
        
        # Считываем глубину из поля ввода
        try:
            self.depth = int(self.depth_entry.get())
        except ValueError:
            self.depth = 3
        
        # Получаем выбранный тип фрактала
        fractal = self.fractal_type.get()
        
        # Вызываем соответствующий метод в зависимости от выбора
        if fractal == "carpet":
            self.draw_carpet()
        elif fractal == "koch":
            self.draw_koch()
        elif fractal == "snowflake":
            self.draw_snowflake()
        elif fractal == "sierpinski":
            self.draw_sierpinski()
        elif fractal == "serpinsky_curve":
            self.draw_serpinsky_curve()
        elif fractal == "hilbert":
            self.draw_hilbert_curve()


# Точка входа в программу
if __name__ == "__main__":
    root = tk.Tk()          # Создаём главное окно
    app = FractalApp(root)  # Создаём объект приложения
    root.mainloop()         # Запускаем главный цикл обработки событий
