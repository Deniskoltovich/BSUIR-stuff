class Solver:
    def __init__(self, logical_conclusion: dict, rule: dict):
        self.logical_conclusion = logical_conclusion
        self.rule = rule
        self.equations = []
        self.varnames = {self.get_first_var_name(key) for key in rule['set'].keys()}

    def run(self):
        self.make_equations()
        solutions = []
        for eq in solver.equations:
            solutions.extend(self.solve_equation(eq))
        result = self.find_intersections(solutions)

        if len(result) == 0:
            print('Нельзя построить обратный вывод!')
            return

        self.print_result(result)


    def find_intersections(self, solutions):
        intersections = []
        for varname in sorted(self.varnames):
            # varname_intervals [(0.1, 1.0), (0.7, 0.1), ...]
            varname_intervals = [solution[varname] for solution in solutions if solution.get(varname)]
            if len(varname_intervals) == 0:
                continue
            intersection = {varname: (
                max(inter[varname][0] for inter in varname_intervals),
                min(inter[varname][1] for inter in varname_intervals)
            ) for varname in self.varnames}

            if any(value[0] > value[1] for value in intersection.values()):
                continue

            intersections.append(intersection)

        return intersections



    def make_equations(self):
        """Создает систему уравнений на основе правила и множества следствий"""
        for name, value in logical_conclusion['set'].items():
            equation = {'right_part': value}
            left_part = []
            for name1, value1 in rule['set'].items():
                if self.get_second_var_name(name1) == name:
                    min_set = (value1, self.get_first_var_name(name1))
                    left_part.append(min_set)

            equation['left_part'] = left_part
            self.equations.append(equation)

        return None

    @staticmethod
    def solve_equation(equation):
        solutions = []
        var_names = [varname[1] for varname in equation['left_part']]
        for min_set in equation['left_part']:
            # min_set (0.1, 'x1')
            solution = {}  # solution {'x1': (0.1, 1.0)}
            if min_set[0] == equation['right_part']:
                solution = {
                    min_set[1]: (min_set[0], 1.0),
                }
            elif min_set[0] < equation['right_part']:
                continue
            elif min_set[0] > equation['right_part']:
                solution = {
                    min_set[1]: (equation['right_part'], equation['right_part'])
                }

            solution.update({
                name: (0.0, 1.0) for name in var_names if name != min_set[1]
            })
            solutions.append({min_set[1]: solution})

        return solutions

    @staticmethod
    def get_second_var_name(elem_name: str):
        return elem_name.split(',')[1]

    @staticmethod
    def get_first_var_name(elem_name: str):
        return elem_name.split(',')[0]


    def print_result(self, result):
        repr = '<'
        for var in sorted(self.varnames):
            repr += f'C({var}),'
        repr = repr.removesuffix(',') + '> ∈ '

        for res in result:
            repr += '('
            for key, value in sorted(res.items()):
                repr += f'{list(value)}*'
            repr = repr.removesuffix('*') + ') U '

        repr = repr.removesuffix('U ')

        print(repr)






if __name__ == '__main__':
    rule = {
        'name': 'R',
        'set': {
            'x1,y1': 0.7,
            'x1,y2': 0.1,
            'x1,y3': 0.2,
            'x2,y1': 0.7,
            'x2,y2': 0.3,
            'x2,y3': 0.1,
        }
    }
    logical_conclusion = {
        'name': 'A',
        'set': {
            'y1': 0.7,
            'y2': 0.3,
            'y3': 0.2
        }
    }
    # rule = {
    #     'name': 'R',
    #     'set': {
    #         'x1,y1': 0.7,
    #         'x1,y2': 0.1,
    #         'x1,y3': 0.1,
    #         'x2,y1': 0.5,
    #         'x2,y2': 0.1,
    #         'x2,y3': 0.1,
    #     }
    # }
    # logical_conclusion = {
    #     'name': 'A',
    #     'set': {
    #         'y1': 0.6,
    #         'y2': 0.2,
    #         'y3': 0.2
    #     }
    # }
    # rule = {
    #     'name': 'R',
    #     'set': {
    #         'x1,y1': 0.7,
    #         'x1,y2': 0.8,
    #         'x1,y3': 0.3,
    #         'x2,y1': 0.7,
    #         'x2,y2': 0.8,
    #         'x2,y3': 0.3,
    #     }
    # }
    # logical_conclusion = {
    #     'name': 'A',
    #     'set': {
    #         'y1': 0.7,
    #         'y2': 0.8,
    #         'y3': 0.3
    #     }
    # }
    solver = Solver(logical_conclusion, rule)
    solver.run()
