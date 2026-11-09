class Counter:
    def __init__(self, name):

        self.name = name
        self.value = 0

    def add(self, n=1):
        self.value += n

    def reset(self):
        self.value = 0

    def __str__(self):
        return f"{self.name}: {self.value}"

accepted = Counter("принято") # Счетчик принятых записей
rejected = Counter("отклонено") # Счетчик отклоненных записей

accepted.add(6) # Прибавляем 6
accepted.add() # Прибавляем ещё 1
rejected.add() # Прибавляем 1 к другому счётчику

print(accepted)
print(rejected)

accepted.reset() # Обнуляем первый счетчик

print("после сброса:", accepted)
print("второй счётчик:", rejected)