'''
Лабораторная работа №1 по дисциплине ЛОИС
Выполнена студентами группы 121702 БГУИР Колтовичем Д., Зайцем Д., Кимстачем Д.
Вариант 1: импликация Гёделя
Задача: разработать программу, выполняющую прямой нечеткий логический вывод
'''

import string

from Parser import NAMES


def generate_nonexistent_name(names: list):
    for name in string.ascii_uppercase:
        for num in range(100):
            new_name = f'{name}{num}'
            if new_name not in names:
                yield new_name


    print('Лимит возможных имен посылок исчерпан')
    raise SystemExit


name_generator = generate_nonexistent_name(NAMES)