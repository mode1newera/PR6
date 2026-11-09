from collections import Counter
from pathlib import Path
from people import AnketaError, Student, Teacher


def parse_line(raw):
    fields = raw.split(";")
    if len(fields) != 5:
        raise AnketaError(f"полей {len(fields)} вместо 5")
    kind, fio, email, phone, extra = fields
    kind = kind.strip().lower()
    if kind == "s":
        return Student(fio, email, phone, extra)
    if kind == "t":
        return Teacher(fio, email, phone, extra)
    raise AnketaError(f"неизвестный тип: {kind or '(пусто)'}")

class Registry:
    def __init__(self):
        self.accepted = []
        self.rejected = []
        self.total = 0
        self.empty = 0

    def add(self, person):
        self.accepted.append(person)

    def load(self, filename):
        try:
            lines = Path(filename).read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            return False
        self.accepted.clear()
        self.rejected.clear()
        self.total = len(lines)
        self.empty = 0
        for number, raw in enumerate(lines, 1):
            if not raw.strip():
                self.empty += 1
                continue
            try:
                self.add(parse_line(raw))
            except AnketaError as error:
                self.rejected.append((number, raw, str(error)))
        return True

    def by_roles(self):
        return Counter(p.role() for p in self.accepted)

    def by_groups(self):
        groups = Counter()
        for person in self.accepted:
            group = person.group_key()
            if group is not None:
                groups[group] += 1
        return groups

    def save_ok(self, filename):
        with Path(filename).open("w", encoding="utf-8") as file:
            for p in sorted(self.accepted):
                fields = (p.fio, p.email, p.phone, p.role(), p.extra())
                file.write(";".join(fields) + "\n")

    def save_errors(self, filename):
        with Path(filename).open("w", encoding="utf-8") as file:
            for number, raw, reason in self.rejected:
                file.write(f"строка {number}: {reason}\n    {raw}\n")

    def __len__(self):
        return len(self.accepted)