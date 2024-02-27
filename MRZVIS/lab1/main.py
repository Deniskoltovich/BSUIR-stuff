from dataclasses import dataclass
from typing import Generator

from operations import binary_multiplication_generator


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
                try:
                    representation += f"{i + 1} - {int(tmp1, 2)} = {tmp1}, {int(tmp2, 2)}={tmp2}\n"
                except ValueError:
                    representation += f"{i + 1} - ---, ---\n"

            else:
                representation += f"{i + 1} - ---, ---\n"

        representation += "\n"
        for i, item in enumerate(self.pipeline):
            representation += f"Этап {i + 1}:\n"
            representation += str(item) + "\n"

        representation += "\nРезультат:\n"
        for i in range(len(self.pairs)):
            try:
                tmp = "".join(map(str, self.result[i]))
                representation += f'{i + 1} - {int(tmp, 2)}={tmp}\n'
            except (IndexError, ValueError, TypeError):
                representation += f'{i + 1} - ---\n'

        return representation + "\n" + '_' * 100


def main():
    pairs = []
    num_of_pairs = int(input('Введите кол-во пар: '))
    for i in range(num_of_pairs):
        pair = input(f'Введите пару {i + 1} через пробел:\n').split()
        try:
            if any(len(item) != 4 or int(item, 2) > 15 for item in pair):
                raise RuntimeError('Введите 4-битное число')
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