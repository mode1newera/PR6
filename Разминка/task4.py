from math import pi

class Figure:
    def __init__(self, name):
        self.name = name

    def area(self):
        return 0

    def __str__(self):
        return f"{self.name}: площадь {self.area():.2f}"

class Rect(Figure):
    def __init__(self, width, height): # Принимаем ширину и высоту

        # Вызываем конструктор родительского класса
        super().__init__("Прямоугольник")

        # Сохраняем размеры прямоугольника
        self.width, self.height = width, height

    def area(self):
        return self.width * self.height

class Circle(Figure):
    # Конструктор принимает радиус
    def __init__(self, radius):

        # Передаём название базовому классу
        super().__init__("Круг")
        self.radius = radius
    # Переопределяем вычисление площади
    def area(self):
        return pi * self.radius ** 2

figures = [
    Rect(3, 4),
    Circle(2),
    Rect(3, 5)
]

total = 0

# Перебираем фигуры одним циклом
for figure in figures:
    # Выводим название и площадь
    print(figure)

    # Добавляем площадь к общей сумме
    total += figure.area()

# Выводим итоговую площадь
print(f"\nОбщая площадь: {total:.2f}")