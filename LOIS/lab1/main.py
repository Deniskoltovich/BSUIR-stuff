'''
Лабораторная работа №1 по дисциплине ЛОИС
Выполнена студентами группы 121702 БГУИР Колтовичем Д., Зайцем Д., Кимстачем Д.
Вариант 1: импликация Гёделя
'''



from itertools import chain

from implication import Implication
from Parser import Parser


def main():
    # Считываем информацию с файла
    with open('input2.txt', 'r') as f:
        data = f.readlines()

    # Парсим информацию, которую считали с файла
    parser = Parser(data)
    parser.parse()

    generated_parcels = []
    for rule in parser.rules:
        print(f'\nПравило: {rule[0]}~>{rule[1]}')
        conclusions = []

        first_predicate = next(predicate for predicate in parser.predicates if predicate['name'] == rule[0])
        second_predicate = next(predicate for predicate in parser.predicates if predicate['name'] == rule[1])
        print('Предикаты:')
        Implication.print_set(first_predicate)
        Implication.print_set(second_predicate)
        for parcel in chain(parser.parcels, generated_parcels):
            print(f'Посылка: ', end='')
            Implication.print_set(parcel)

            print('Результат прямого вывода:')
            implication = Implication(first_predicate, second_predicate, parcel)
            conclusions.extend(implication.solve())
        generated_parcels.extend(conclusions)



if __name__ == "__main__":
    main()
