class Implication:
    def __init__(self, first_predicate: dict, second_predicate: dict, parcel: dict):
        self.first_predicate = first_predicate
        self.second_predicate = second_predicate
        self.parcel = parcel

    def calculate_implication(self):
        result = []
        for i in range(len(self.first_predicate['corteges'])):
            row = []
            elements = []
            for j in range(len(self.second_predicate['corteges'])):
                elements = [self.first_predicate['corteges'][i]['name'], self.second_predicate['corteges'][j]['name']]
                value = self.implicate(self.first_predicate['corteges'][i], self.second_predicate['corteges'][j])
                row.append([elements, value])
            result.append(row)
        return result

    def implicate(self, first_el, second_el):
        value = 1 if first_el['value'] <= second_el['value'] else second_el['value']
        return value

    def get_elements_except_one(self, el, elements):
        return [element for element in elements if element != el]

    def check_parcel_and_result(self, result):
        conjuncted_matrix = []
        if len(result) != len(self.parcel['corteges']):
            return
        for i in range(len(result)):
            row = []
            for j in range(len(result[i])):
                if self.parcel['corteges'][i]['name'] in result[i][j][0]:
                    el = [self.get_elements_except_one(self.parcel['corteges'][i]['name'], result[i][j][0]),
                          min(self.parcel['corteges'][i]['value'], result[i][j][1])]
                    row.append(el)
            conjuncted_matrix.append(row)
        return conjuncted_matrix

    def get_conclusion(self, conjucted_matrix):
        conclusion = []
        print(conjucted_matrix)
        for i in range(len(conjucted_matrix[0])):
            column = []
            for j in range(len(conjucted_matrix)):
                column.append(conjucted_matrix[j][i])
            column.sort(key=lambda x: x[1], reverse=True)
            conclusion.append(column[0])
        return conclusion

    def show_ans(self, ans):
        string = "{"
        for i in range(len(ans)):
            cortege = ""
            if len(ans[i][0]) > 1:
                cortege = "(({}),{})".format(','.join(ans[i][0]), ans[i][1])
            else:
                cortege = "({}, {})".format(','.join(ans[i][0]), ans[i][1])
            string += cortege
            if i != len(ans) - 1:
                string += ','
        string += "}"
        return string

    def calculate(self):
        implication_matrix = self.implication()
        conjucted_matrix = self.check_parcel_and_result(self.calculate_implication())
        ans = self.get_conclusion(conjucted_matrix)
        print(self.show_ans(ans))

    def implication(self):
        # if len(self.first_predicate['set']) != len(self.second_predicate['set']):
        #     raise RuntimeError(f'The lengths of predicates {self.first_predicate}, {self.second_predicate} are not eq')
        # задаем размер
        matrix = [[_ for _ in range(len(self.second_predicate['set']))]
                  for _ in range(len(self.first_predicate['set'].keys()))
                  ]
        # вычисляем значения элементов матрицы
        for i, item1 in enumerate(self.first_predicate['set'].keys()):
            for j, item2 in enumerate(self.second_predicate['set'].keys()):
                matrix[i][j] = (f'{item1},{item2}',
                                max(self.first_predicate['set'].get(item1),
                                    self.second_predicate['set'].get(item2)
                                    )
                                )

        return matrix