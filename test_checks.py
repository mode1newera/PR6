import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from people import Student, AnketaError
from registry import Registry, parse_line

class Checks(unittest.TestCase):
    def test_person(self):
        p = Student(' иванов  иВАН ', ' A@Example.Com ', '8 (921) 111-22-33', '09 С 41')
        self.assertEqual((p.fio,p.email,p.phone,p.extra()),
                         ('Иванов Иван','a@example.com','79211112233','09с41'))
        self.assertEqual(p.short_fio(), 'Иванов И.')
        self.assertEqual(p.masked_phone(), '+7 (921) ***-**-33')
        for email in ['a.b.ru','@b.ru','a@b','a@.b.ru','a@b.ru.','a b@b.ru','a@@b.ru']:
            with self.subTest(email=email), self.assertRaises(AnketaError):
                Student('Иванов Иван',email,'79211112233','09с41')
        for phone in ['123','69211112233']:
            with self.subTest(phone=phone), self.assertRaises(AnketaError):
                Student('Иванов Иван','a@b.ru',phone,'09с41')
        for kind, extra in [('s',''),('t',' '),('x','И9')]:
            with self.subTest(kind=kind), self.assertRaises(AnketaError):
                parse_line(f'{kind};Иванов Иван;a@b.ru;79211112233;{extra}')

    def test_registry(self):
        r = Registry()
        self.assertTrue(r.load('anketa.txt'))
        self.assertEqual((len(r),len(r.rejected),r.total,r.empty), (6,7,14,1))
        self.assertEqual(r.by_roles(), {'студент':4,'преподаватель':2})
        self.assertEqual(r.by_groups(), {'09с41':3,'09с43':1})
        self.assertEqual([x[0] for x in r.rejected], [5,6,7,8,9,10,14])
        self.assertTrue(r.load('anketa.txt'))
        self.assertEqual(len(r), 6)
        with TemporaryDirectory(dir='.') as folder:
            b = Path(folder)
            r.save_ok(b/'ok.txt')
            r.save_errors(b/'errors.txt')
            self.assertEqual(len((b/'ok.txt').read_text(encoding='utf-8').splitlines()),6)
            self.assertIn('строка 10: кафедра пуста',(b/'errors.txt').read_text(encoding='utf-8'))
            self.assertFalse(r.load(b/'missing.txt'))
            (b/'empty.txt').write_text('\n  \n',encoding='utf-8')
            self.assertTrue(r.load(b/'empty.txt'))
            self.assertEqual((len(r),r.empty), (0,2))

if __name__ == '__main__':
    unittest.main()
