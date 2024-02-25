from dataclasses import dataclass
from typing import Generator


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
    partial_addition = [0] * 8
    result = []
    for i in range(len(multiplicand) - 1, -1, -1):
        # умножаем multiplier на разряд multiplicand и делаем сдвиг (0 справа)
        partial_product = [multiplicand[i] * multiplier_i for multiplier_i in multiplier] + [0] * (len(multiplicand) - 1 - i)

        # Дополняем нулями слева
        partial_product = [0] * (8 - len(partial_product)) + partial_product

        partial_addition = binary_addition(partial_product, partial_addition)
        yield partial_product, partial_addition

        result.insert(0, partial_addition)

@dataclass
class PipeItem:
    item_generator: Generator | None = None
    partial_product: list[int] | None = None
    partial_addition: list[int] | None = None

    def __str__(self):
        partial_product = '---' if not self.partial_product else ''.join(list(map(str, self.partial_product)))
        partial_addition = '---' if not self.partial_addition else ''.join(list(map(str, self.partial_addition)))
        return f'Частичная сумма: {partial_addition}\t Частичное произведение: {partial_product}'

    def __bool__(self):
        return self.item_generator is not None


class Pipe:
    def __init__(self, *pairs):
        self.pairs = pairs
        self.pairs_gen = list(binary_multiplication_generator(*pair) for pair in self.pairs)
        self.pipeline: list[PipeItem] = [PipeItem()] * 4
        self.result = list()
        self.step = 0

    def next_step(self):
        try:
            new_pair = self.pairs_gen.pop(0)
        except IndexError:
            new_pair = None

        self.pipeline = [PipeItem(new_pair)] + self.pipeline
        result = self.pipeline.pop()
        if result:
            self.result.append(result.partial_addition)

        for i in range(len(self.pipeline)):
            if self.pipeline[i]:
                item_gen = self.pipeline[i].item_generator
                partial_result = next(item_gen)
                self.pipeline[i] = PipeItem(item_gen, *partial_result)


        self.step += 1


    def __str__(self):
        representation = f"Такт: {self.step}.\n"
        representation += "Входная очередь:\n"
        for i in range(len(self.pairs) - 1, -1, -1):
            if i not in list(range(len(self.pairs) - len(self.pairs_gen))):
                tmp1 = "".join(map(str, self.pairs[i][0]))
                tmp2 = "".join(map(str, self.pairs[i][1]))

                representation += f"{i + 1} - {int(tmp1, 2)} = {tmp1}, {int(tmp2, 2)}={tmp2}\n"
            else:
                representation += f"{i + 1} - ---, ---\n"

        # for i, pair in enumerate(self.pairs, start=1):
        #     if i <= len(self.pairs_gen):
        #         tmp1 = "".join(map(str, pair[0]))
        #         tmp2 = "".join(map(str, pair[1]))
        #
        #         representation += f"{i} - {int(tmp1, 2)} = {tmp1}, {int(tmp2, 2)}={tmp2}\n"
        #     else:
        #         representation += f"{i} - ---, ---\n"

        representation += "\n"
        for i, item in enumerate(self.pipeline):
            representation += f"Этап {i + 1}:\n"
            representation += str(item) + "\n"

        representation += "\nРезультат:\n"
        for i in range(len(self.pairs)):
            try:
                tmp = "".join(map(str,self.result[i]))
                representation += f'{i + 1} - {int(tmp, 2)}={tmp}\n'
            except IndexError:
                representation += f'{i + 1} - ---\n'

        return representation + "\n" + '_' * 100

num1 = [1,0,1,0]
num2 = [0,1,0,1]

num3 = [1,0,0,1]
num4 = [0,1,1,1]

num5 = [0,0,0,1]
num6 = [1,1,1,1]

pairs = []
num_of_pairs = int(input('Введите кол-во пар: '))
for i in range(num_of_pairs):
    pair = input(f'Введите пару {i + 1} через пробел:\n').split()
    if any(len(item) != 4 for item in pair):
        raise RuntimeError('Введите 4-битное число')
    pairs.append([list(map(int, item)) for item in pair])

pipe = Pipe(*pairs)
while True:
    print(pipe)
    pipe.next_step()
    input()