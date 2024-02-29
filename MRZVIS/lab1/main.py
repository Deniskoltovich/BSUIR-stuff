from pipe import Pipe

'''
Лабораторная работа №1 по дисциплине МРЗВиС
Выполнена студентами группы 121702 БГУИР Колтовичем Д., Зайцем Д.
Вариант 1: умножение 4-разрядных чисел(с младших разрядов) со сдвигом множимого влево 
Задача: разработать программу, выполняющую вычисление попарного произведения компонентов двух векторов
'''


def main():
    pairs = []
    num_of_pairs = int(input('Введите кол-во пар: '))
    for i in range(num_of_pairs):
        pair = input(f'Введите пару {i + 1} через пробел:\n').split()
        try:
            if any(len(item) != 4 or int(item, 2) > 15 for item in pair):
                raise RuntimeError('Введите 4-разрядное число')
        except ValueError:
            raise RuntimeError('Некорректное число!')

        if not pair:
            pairs.append([[None], [None]])
            continue
        pairs.append([list(map(int, item)) for item in pair])

    pipe = Pipe(*pairs)
    while True:
        print(pipe)
        pipe.next_step()
        input()


if __name__ == '__main__':
    main()
