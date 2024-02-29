'''
Лабораторная работа №1 по дисциплине МРЗВиС
Выполнена студентами группы 121702 БГУИР Колтовичем Д., Зайцем Д.
Вариант 1: умножение 4-разрядных чисел(с младших разрядов) со сдвигом множимого влево
Задача: разработать программу, выполняющую вычисление попарного произведения компонентов двух векторов
'''


NUM_SIZE = 4


def binary_addition(num1: list, num2: list):
    result = []
    carry = 0

    if len(num1) < len(num2):
        num1 = [0] * (len(num2) - len(num1)) + num1
    else:
        num2 = [0] * (len(num1) - len(num2)) + num2

    for i in range(len(num1) - 1, -1, -1):
        bit_sum = num1[i] + num2[i] + carry
        result.insert(0, bit_sum % 2)

        carry = bit_sum // 2

    if carry:
        result.insert(0, carry)

    return result


def binary_multiplication_generator(multiplier, multiplicand):
    if multiplier == [None] or multiplicand == [None]:
        for _ in range(NUM_SIZE):
            yield None, None

    partial_addition = [0] * 8
    for i in range(len(multiplicand) - 1, -1, -1):
        # умножаем multiplier на разряд multiplicand и делаем сдвиг влево (0 справа)
        partial_product = [multiplicand[i] * multiplier_i for multiplier_i in multiplier] + [0] * (len(multiplicand) - 1 - i)

        # Дополняем нулями слева
        partial_product = [0] * (8 - len(partial_product)) + partial_product

        partial_addition = binary_addition(partial_product, partial_addition)
        yield partial_product, partial_addition
