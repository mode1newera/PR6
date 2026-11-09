class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property # @property превращает метод в свойство, можно обращаться без скобок
    def fahrenheit(self):

        return self.celsius * 9 / 5 + 32 # Перевод из Цельсия в Фаренгейты

    def __str__(self):
        return f"{self.celsius:.1f} C = {self.fahrenheit:.1f} F"

    def __lt__(self, other):
        return self.celsius < other.celsius

values = [
    Temperature(21.5),
    Temperature(-3),
    Temperature(0)
]

for value in values:
    print(value)

print("\nПо возрастанию:")

for value in sorted(values):
    print(value)

print("\nСамый тёплый:", max(values))