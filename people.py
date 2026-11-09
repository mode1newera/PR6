# Собственное исключение для неправильных анкет
class AnketaError(Exception):
    """Ошибка данных одной анкеты."""


# Person — общий родительский класс
class Person:

    # Конструктор принимает три основных поля
    def __init__(self, fio, email, phone):

        # Проверяем ФИО и сохраняем исправленный вариант
        self.fio = self.check_fio(fio)

        # Проверяем почту и сохраняем результат
        self.email = self.check_email(email)

        # Проверяем телефон и сохраняем единый формат
        self.phone = self.check_phone(phone)

    @staticmethod
    def check_fio(value):

        # Разделяем ФИО на слова
        words = value.split()

        # Должно быть хотя бы два слова
        if len(words) < 2:
            raise AnketaError("в ФИО меньше двух слов")

        # Собираем ФИО обратно и исправляем регистр
        return " ".join(words).title()

    # Статический метод проверки почты
    @staticmethod
    def check_email(value):

        # Убираем пробелы по краям
        email = value.strip().lower()

        # Проверяем, чтобы символ @ был ровно один
        if email.count("@") != 1:
            raise AnketaError("в почте должна быть ровно одна @")

        user, domain = email.split("@")

        if not user or not domain or "." not in domain:
            raise AnketaError("пустая часть почты или нет точки в домене")

        if domain.startswith(".") or domain.endswith("."):
            raise AnketaError("точка на краю домена")

        if any(ch.isspace() for ch in email):
            raise AnketaError("внутри почты есть пробелы")

        return email

    @staticmethod
    def check_phone(value):

        # Оставляем из введённого номера только цифры
        # Удаляются скобки, пробелы, дефисы и плюс
        digits = "".join(ch for ch in value if ch in "0123456789")

        # Проверяем длину номера.
        # Требуется ровно 11 цифр.
        if len(digits) != 11:
            raise AnketaError(f"в телефоне {len(digits)} цифр вместо 11")

        # Номер должен начинаться на 7 или 8.
        if digits[0] not in "78":
            raise AnketaError("телефон должен начинаться с 7 или 8")

        # Приводим номер к единому формату, чтобы он всегда начинался с 7
        return "7" + digits[1:]

    # Метод маскировки телефона
    def masked_phone(self):

        # Показываем код оператора и последние 2 цифры
        # Остальную часть заменяем звёздочками
        return f"+7 ({self.phone[1:4]}) ***-**-{self.phone[-2:]}"

    # Метод сокращения ФИО
    def short_fio(self):

        # Отделяем фамилию от имени и отчества
        surname, *names = self.fio.split()

        # Превращаем имя и отчество в инициалы
        return surname + " " + " ".join(n[0] + "." for n in names)

    # Дочерние классы его переопределяют
    def role(self):
        return "человек"

    # Для студента это группа, для преподавателя кафедра
    def extra(self):
        return "—"

    # У обычного человека группа отсутствует
    def group_key(self):
        return None

    # Определяем строковое представление объекта
    def __str__(self):

        # Используем другие методы этого же объекта.
        return f"{self.fio};{self.role()};{self.extra()};{self.masked_phone()}"

    # Определяем сравнение двух объектов по ФИО.
    def __lt__(self, other):
        return self.fio < other.fio


class Student(Person):

    def __init__(self, fio, email, phone, group):

        super().__init__(fio, email, phone)

        self.group = "".join(group.split()).lower()

        # Пустая группа считается ошибкой.
        if not self.group:
            raise AnketaError("группа пуста")

    def role(self):
        return "студент"

    def extra(self):
        return self.group

    # Возвращаем группу для статистики
    def group_key(self):
        return self.group

class Teacher(Person):

    # Преподаватель имеет дополнительное поле department
    def __init__(self, fio, email, phone, department):

        # Проверяем общие данные через Person.
        super().__init__(fio, email, phone)

        self.department = " ".join(department.split())

        if not self.department:
            raise AnketaError("кафедра пуста")

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.department