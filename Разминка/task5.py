# Создаём собственный тип ошибки AgeError
class AgeError(Exception):
    pass
class Person:
    def __init__(self, name, age):
        if not 0 <= age <= 120:

            raise AgeError(f"возраст {age} вне границ 0..120")
        
        self.name = name
        self.age = age

data = [
    ("Иванов Иван", 19),
    ("Петрова Анна", 200),
    ("Сидоров Пётр", -5),
    ("Орлова Мария", 20)
]

accepted = []

for name, age in data:

    # Пробуем создать объект Person
    try:
        accepted.append(Person(name, age))

    # Если возникла AgeError, перехватываем её
    except AgeError as error:

        # Выводим причину отказа
        print(f"Не принято: {name} — {error}")

print(f"\nПринято: {len(accepted)}")

for person in accepted:
    print(f"  {person.name}, {person.age} лет")