'''
Лабораторная работа №1 по дисциплине ЛОИС
Выполнена студентами группы 121702 БГУИР Колтовичем Д., Зайцем Д., Кимстачем Д.
Вариант 1: импликация Гёделя
'''

class Implication:
    def __init__(self, first_predicate: dict, second_predicate: dict, parcel: dict):
        self.first_predicate = first_predicate
        self.second_predicate = second_predicate
        self.parcel = parcel

    def solve(self):
        """
        Создает матрицу импликации согласно правилу и предикатам, производит операцию
        конъюнкции посылки с матрицей и делает прямой вывод. Результат прямого вывода снова
         учавствует в конъюнкции с матрицей импликации (если может). Возвращает результаты прямых выводов.
        """
        #проводим импликацию
        implication_matrix = self.implication()

        i = 1
        used_parcels = []
        current_parcel = self.parcel
        new_parcels = []

        while True:
            # проводим конъюнкцию
            conjunction_matrix = self.conjunction(current_parcel, implication_matrix)
            if not conjunction_matrix:
                break
            # делаем вывод из матрицы конъюнкции
            direct_conclusion = self.make_conclusion(conjunction_matrix, f'{self.parcel["name"]}{i}')
            used_parcels.append(current_parcel['set'])
            # если такой вывод уже использовался (зацикливание)
            if direct_conclusion['set'] in used_parcels:
                if len(new_parcels) == 0:
                    print('Зацикливание')
                    return new_parcels
                break
            new_parcels.append(direct_conclusion)


            self.print_set(direct_conclusion)
            current_parcel = direct_conclusion
            i += 1

        if len(new_parcels) == 0: print('Области определения не совпадают')
        return new_parcels

    @staticmethod
    def print_set(set: dict):
        output = f"{set['name']} = " + '{'
        for var, val in set['set'].items():
            output += f'({var}, {val}), '
        print(output.removesuffix(', ') + '}')

    @staticmethod
    def make_conclusion(conjunction_matrix: list[list[tuple]], name: str):
        """
        Делает прямой вывод из матрицы конъюнкции
        """
        supremos = [] # список макс значений по столбцам
        for col_idx in range(len(conjunction_matrix[0])):
            supremos.append(max(
                row[col_idx][1] for row in conjunction_matrix
            ))
        # переменные по столбцам
        # item[0] = 'x1,y1'
        vars = [item[0].split(',')[1] for item in conjunction_matrix[0]]

        conclusion = {
            'name': name,
            'set': dict(zip(vars, supremos))
        }
        return conclusion

    @staticmethod
    def check_parcel_to_conjunct(parcel_vec: dict, implication_matrix: list[list[tuple]]):
        """
        Проверяет подходит ли посылка для конъеюнкции с матрицей импликации. Проверяет размерность
        и область определения
        """
        # parcel_vec = {'name': 'F', 'set': {'x1': 0.2, 'x2': 1.0}}
        # проверяем размеры
        if len(parcel_vec['set']) != len(implication_matrix):
            raise ValueError
        # проверяем, чтобы переменные в строках совпадали
        for row in implication_matrix:
            # row = [('x1,y1', 1.0), ...]
            # если названия элементов парселя не совп. с "названиями строк" в матрице
            t = row[0][0].split(',')[0]
            if parcel_vec['set'].get(row[0][0].split(',')[0]) is None:
                raise ValueError

    @staticmethod
    def conjunction(parcel_vec: dict, implication_matrix: list[list[tuple]]):
        try:
            Implication.check_parcel_to_conjunct(parcel_vec, implication_matrix)
        except ValueError:
            return None
        # для каждого элемента в матрице ипликации и соотв. по строке элемента в парселе ищем минимальное
        conjunction_matrix = []
        for row in implication_matrix:
            # item = ('x1,y1', 1.0)
            conjunction_matrix.append(
                [(item[0],
                  min(item[1], parcel_vec['set'].get(item[0].split(',')[0]))
                  ) for item in row]
            )

        return conjunction_matrix

    def implication(self) -> list[list[tuple]]:
        matrix = []
        # вычисляем значения элементов матрицы
        for item1 in self.first_predicate['set'].keys():
            matrix.append([
                (f'{item1},{item2}',
                    max(self.first_predicate['set'].get(item1),
                        self.second_predicate['set'].get(item2))
                 ) for item2 in self.second_predicate['set'].keys()
            ])
        return matrix
