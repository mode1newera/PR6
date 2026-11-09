from pathlib import Path
import sys
from registry import Registry

def show_results(registry):
    people = sorted(registry.accepted)
    fw = max([len("ФИО")] + [len(p.fio) for p in people])
    ew = max([len("Группа/кафедра")] + [len(p.extra()) for p in people])
    header = (f"{'№':>3}  {'ФИО':<{fw}}  {'Роль':<13}  "
              f"{'Группа/кафедра':<{ew}}  Телефон")
    print(header)
    print("-" * len(header))
    for number, person in enumerate(people, 1):
        print(f"{number:>3}  {person.fio:<{fw}}  "
              f"{person.role():<13}  {person.extra():<{ew}}  "
              f"{person.masked_phone()}")
    print("-" * len(header))
    print(f"\nОтклонено строк: {len(registry.rejected)}")
    for number, raw, reason in registry.rejected:
        print(f"  строка {number}: {reason}\n    {raw}")
    print(f"\nВсего строк: {registry.total}; пустых: {registry.empty}")
    print(f"Принято: {len(registry)} | Отклонено: {len(registry.rejected)}")
    print("\nПо ролям:")
    for role, count in sorted(registry.by_roles().items()):
        print(f"  {role:<13} {count}")
    print("\nПо группам:")
    for group, count in sorted(registry.by_groups().items()):
        print(f"  {group:<13} {count}")

def main():
    filename = (Path(sys.argv[1]) if len(sys.argv) > 1 else
                Path(__file__).with_name("anketa.txt"))
    registry = Registry()
    try:
        loaded = registry.load(filename)
    except (OSError, UnicodeError) as error:
        print(f"Не удалось прочитать файл: {error}")
        return
    if not loaded:
        print(f"Файл {filename.name} не найден")
        return
    show_results(registry)
    try:
        registry.save_ok(filename.with_name("ok.txt"))
        registry.save_errors(filename.with_name("errors.txt"))
    except (OSError, UnicodeError) as error:
        print(f"Не удалось сохранить результаты: {error}")
        return
    print("\nСохранено: ok.txt и errors.txt")

if __name__ == "__main__":
    main()
