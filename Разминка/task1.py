class Student:
    def __init__(self, fio, group): # Срабатывает автоматически при создании студента.

        self.fio = fio
        self.group = group

    def short(self): # Сокращает ФИО до фамилии и инициалов.

        # Разделяем ФИО на слова.
        surname, *names = self.fio.split()
        initials = " ".join(n[0] + "." for n in names) # Берём первую букву каждого имени
        return surname + " " + initials # Возвращаем сокращённое ФИО.

first = Student("Иванов Иван Петрович", "09с41")
second = Student("Петрова Анна", "09с42")

print(first.fio)
print(first.group)
print(first.short())
print(second.short(), "|", second.group)

first.group = "09с43" # Меняем группу первого студента

print("После изменения первого:", first.group, "|", second.group) # Проверка группы у второго