from lab2copy import Context


class Minimizer:
    CONJUNCTION = ' * '
    DISJUNCTION = ' + '

    def __init__(self, formula: str, mode):
        self.mode = mode
        self.context = Context(formula)
        self.vars = self.context.vars
        self.operation_in_constituents, self.operation_out_constituents = [self.CONJUNCTION,
                                                                           self.DISJUNCTION] if 'DNF' in mode \
            else [self.DISJUNCTION, self.CONJUNCTION]
        self.non_minimized_func = Context(formula).get_pcnf() if 'CNF' in mode else Context(formula).get_pdnf()
        self.constant = 1 if self.mode == 'DNF' else 0

        self.implicants = sorted(self.non_minimized_func.split(self.operation_out_constituents))
        self.minimized_func = self.reduced_func = self.non_minimized_func

    def create_karnough_table(self, *vars):
        var1, var2, var3 = vars
        table = [[0 for _ in range(5)] for _ in range(3)]
        oper = self.operation_in_constituents
        table[1][0], table[2][0], table[0][1], table[0][2], table[0][3], table[0][4] = \
            f'!{var1}', var1, f'!{var2}{oper}!{var3}', f'!{var2}{oper}{var3}', f'{var2}{oper}{var3}', f'{var2}{oper}!{var3}'
        truth_table = self.context.truth_table
        column = {'00': 1, '01': 2, '11': 3, '10': 4}
        for row in truth_table:
            value = row.value
            interp: dict = row.interpretation
            temp: str = str(interp[var2]) + str(interp[var3])
            table[interp[var1] + 1][column[temp]] = value

        return table

    @staticmethod
    def is_processed_cells(cells: list, founded: list) -> bool:
        counter = 0
        for i in cells:
            if i not in founded: return False

        return True

    def process_4_cell_line(self, table, neighbor_indexes, founded):
        for row_ind, row in enumerate(table):
            if row_ind == 0: continue
            if row.count(self.constant) == 4:
                neighbor_indexes.append([row_ind])
                founded.extend([[row_ind, 0], [row_ind, 1], [row_ind, 2], [row_ind, 3], [row_ind, 4]])
                continue

        return neighbor_indexes, founded

    def is_normal_square_area(self, table, col_value, col_ind, row_ind, founded) -> bool:
        return col_ind != 4 and col_value == self.constant \
            and table[row_ind][col_ind + 1] == self.constant \
            and row_ind != 2 and table[row_ind + 1][col_ind] == self.constant \
            and table[row_ind + 1][col_ind + 1] == self.constant and not self.is_processed_cells(
                [[row_ind, col_ind], [row_ind + 1, col_ind + 1], [row_ind + 1, col_ind], [row_ind, col_ind + 1]],
                founded)

    def is_diff_side_square_area(self, table, col_value, col_ind, row_ind, founded) -> bool:
        return row_ind != 2 and col_ind == 1 and col_value == self.constant \
            and table[row_ind + 1][col_ind] == self.constant and \
            table[row_ind][4] == self.constant and table[row_ind + 1][4] == self.constant \
            and not self.is_processed_cells([[row_ind, col_ind], [row_ind + 1, col_ind], \
                                             [row_ind, 4], [row_ind + 1, 4]], founded)

    def process_4_cell_square(self, table, neighbor_indexes, founded):
        for row_ind, row in enumerate(table):
            if row_ind == 0: continue
            for col_ind, col_value in enumerate(row):
                if col_ind == 0: continue
                if self.is_normal_square_area(table, col_value, col_ind, row_ind, founded):
                    neighbor_indexes.append([col_ind, col_ind + 1, 0])
                    founded.extend([[row_ind, col_ind], [row_ind + 1, col_ind + 1], [row_ind + 1, col_ind],
                                    [row_ind, col_ind + 1]])

                if self.is_diff_side_square_area(table, col_value, col_ind, row_ind, founded):
                    neighbor_indexes.append([col_ind, 4, 0])
                    founded.extend([[row_ind, col_ind], [row_ind + 1, col_ind], [row_ind, 4], [row_ind + 1, 4]])
        return neighbor_indexes, founded

    def process_2_cell_area(self, table, neighbor_indexes, founded):
        for row_ind, row in enumerate(table):
            if row_ind == 0: continue
            for col_ind, col_value in enumerate(row):
                if col_ind == 0: continue
                if row_ind != 2 and col_value == self.constant and table[row_ind + 1][col_ind] == self.constant \
                        and ([row_ind, col_ind] not in founded or [row_ind + 1, col_ind] not in founded):
                    neighbor_indexes.append([row_ind, row_ind + 1, col_ind, col_ind])
                    founded.extend([[row_ind, col_ind], [row_ind + 1, col_ind]])
                if col_ind != 4 and col_value == self.constant and table[row_ind][col_ind + 1] == self.constant \
                        and ([row_ind, col_ind] not in founded or [row_ind, col_ind + 1] not in founded):
                    neighbor_indexes.append([row_ind, row_ind, col_ind, col_ind + 1])
                    founded.extend([[row_ind, col_ind], [row_ind, col_ind + 1]])
                if col_ind == 1 and col_value == self.constant and row[-1] == self.constant \
                        and ([row_ind, 4] not in founded or [row_ind, col_ind] not in founded):
                    neighbor_indexes.append([row_ind, row_ind, col_ind, -1])
                    founded.extend([[row_ind, col_ind], [row_ind, 4]])
        return neighbor_indexes, founded

    def process_1_cell_area(self, table, neighbor_indexes, founded):
        for row_ind, row in enumerate(table):
            if row_ind == 0: continue
            for col_ind, col_value in enumerate(row):
                if col_ind == 0: continue
                if col_value == self.constant and [row_ind, col_ind] not in founded:
                    neighbor_indexes.append([row_ind, col_ind])
                    founded.append([row_ind, col_ind])

        return neighbor_indexes, founded

    def process_table(self, table):
        neighbor_indexes = []
        founded = []
        neighbor_indexes, founded = self.process_4_cell_line(table, neighbor_indexes, founded)
        neighbor_indexes, founded = self.process_4_cell_square(table, neighbor_indexes, founded)
        neighbor_indexes, founded = self.process_2_cell_area(table, neighbor_indexes, founded)
        neighbor_indexes, founded = self.process_1_cell_area(table, neighbor_indexes, founded)

        return self.concat_for_karnough(table, neighbor_indexes)
    
    def get_4_area_implicant(self, table, item):
        implicant1 = table[item[0]][0] + self.operation_in_constituents + table[0][item[2]]
        implicant2 = table[item[1]][0] + self.operation_in_constituents + table[0][item[3]]
        implicant = self.union_karnough_implicants(implicant1, implicant2)
        return implicant
    
    def get_square_area_implicant(self, table, item, inversion):
        implicant: str = f'{table[item[0]][0]}{self.operation_in_constituents}{table[0][item[1]]}'
        if inversion:
            implicant = self.operation_in_constituents.join(
                list(map(lambda x: f'!{x}' if x.find('!') == -1 else x.replace('!', ''),
                         implicant.split(self.operation_in_constituents))))
            
        return implicant

    def concat_for_karnough(self, table, neigthboor_indexes):
        implicants = []
        inversion = True if 'CNF' in self.mode else False
        for item in neigthboor_indexes:
            if len(item) == 1:
                implicant: str = table[item[0]][0]
                if inversion:
                    implicant = implicant.replace('!', '') if implicant.find('!') != -1 else f'!{implicant}'
                else:
                    implicant = implicant if implicant.find('!') != -1 else implicant.replace('!', '')
            elif len(item) == 2:
                implicant: str = self.get_square_area_implicant(table, item, inversion)
            elif len(item) == 3:
                implicant = self.union_karnough_implicants(table[0][item[0]], table[0][item[1]])
            else:
                implicant = self.get_4_area_implicant(table, item)

            implicants.append(f'({implicant})')

        return implicants

    def union_karnough_implicants(self, implicant1, implicant2):
        literals1 = set(self.get_literals(implicant1))
        literals2 = set(self.get_literals(implicant2))
        result_literals = literals1.intersection(literals2)
        inversion = True if 'CNF' in self.mode else False
        if inversion:
            result_literals = list(map(lambda x: f'!{x}' if x.find('!') == -1 else x.replace('!', ''), result_literals))

        return f'{self.operation_in_constituents.join(result_literals)}'

    def karnough_method(self):
        implicants = self.process_table(self.create_karnough_table(*sorted(self.vars)))
        implicants = [i for i in implicants if i]

        self.minimized_func = self.operation_out_constituents.join(implicants)
        return None

    def print_karnough_table(self):
        table = self.create_karnough_table(*sorted(self.vars))
        print(*table[0], sep='\t|\t', end='\n' + '_' * 100 + '|\n')
        for ind, row in enumerate(table[1:]):
            for item in row:
                print(str(item).center(8 + len(table[0][ind + 1]), ' ') if item != row[0] else str(item).center(5, ' '),
                      end='\t|')
            print('\n' + '_' * 100, end='\n\n' if ind != 1 else '\n')

    def reduce_func(self, implicants=None):
        if implicants is None:
            implicants = self.implicants
        new_implicants = self.process_implicants_to_reduce(implicants)
        new_implicants = sorted(
            set(map(lambda x: f'({x})' if x not in self.vars and x[0] != '(' and x[-1] != ')' else x, new_implicants)))
        new_func = self.operation_out_constituents.join(new_implicants)
        if new_func != self.reduced_func:
            self.reduced_func = new_func
            self.reduce_func(new_implicants)

    def process_implicants_to_reduce(self, implicants_list):
        new_implicants_list = []
        concatenated_implicants = []
        for i, implicants_i in enumerate(implicants_list):
            for j, implicants_j in enumerate(implicants_list):
                if i != j:
                    new_implicant = self.intersec_implicants(implicants_i, implicants_j)
                    if new_implicant:
                        new_implicants_list.append(new_implicant)
                        concatenated_implicants += [implicants_i, implicants_j]
        new_implicants_list += [implicant for implicant in implicants_list if implicant not in concatenated_implicants]
        return new_implicants_list

    def intersec_implicants(self, implicant_1: str, implicant_2: str):
        literals_1, literals_2 = self.get_literals(implicant_1), self.get_literals(implicant_2)
        union_literals = [x for x in literals_1]
        union_literals.extend(literals_2)
        union_literals = set(map(lambda x: x.replace('!', ''), union_literals))
        if len(union_literals) == len(literals_1):
            new_literals = set(literals_1).intersection(set(literals_2))
            if len(new_literals) != len(literals_1) - 1: return
            return self.operation_in_constituents.join(new_literals)

    def return_removed_implicants(self, influent_impl: list[str], removable_impl: list[str]):
        removable_impl.sort(key=len, reverse=True)
        shortened_func = self.operation_out_constituents.join(influent_impl)
        solution_for_shortened_func = Context(f'({shortened_func})').truth_table
        solution_for_reduced_func = Context(f'({self.reduced_func})').truth_table

        while self.get_truth_table_row(solution_for_shortened_func) != self.get_truth_table_row(
                solution_for_reduced_func):
            influent_impl += [removable_impl.pop()]
            solution_for_shortened_func = Context(
                f'({self.operation_out_constituents.join(influent_impl)})').truth_table
        return influent_impl

    def is_removable_implicants(self, implicant_1, implicant_2):
        if len(implicant_1) != len(implicant_2) \
                or not all(literal in implicant_2 or literal.replace('!', '') in implicant_2 \
                           for literal in implicant_1) \
                or not self.num_of_different_literal(implicant_1, implicant_2) == 1:
            return False

        return True

    def num_of_different_literal(self, first_literals: list[str], second_literals: list[str]):
        return sum(
            [
                (var in first_literals and f'!{var}' in second_literals) or \
                (f'!{var}' in first_literals and var in second_literals)
                for var in self.vars
            ]
        )

    def get_literals(self, implicant_str: str):
        return implicant_str.replace('(', '').replace(')', '').split(self.operation_in_constituents)

    def process_implicants_for_calc(self, implicants):
        influent_implicant, removable_implicants = [], []
        reduced_function_sol = Context(f'({self.reduced_func})').truth_table
        if len(implicants) == 1:
            return implicants, implicants
        for implicant in implicants:
            other_implicants = [i for i in implicants if i != implicant]
            new_formula = f'({self.operation_out_constituents.join(other_implicants)})'
            shortened_func_sol = Context(new_formula).truth_table
            influent_implicant.append(implicant) \
                if self.get_truth_table_row(shortened_func_sol) != self.get_truth_table_row(reduced_function_sol) \
                else removable_implicants.append(implicant)
        if self.get_truth_table_row(shortened_func_sol) != self.get_truth_table_row(
                reduced_function_sol):
            influent_implicant = self.return_removed_implicants(influent_implicant, removable_implicants)
        shortened_func = self.operation_out_constituents.join(influent_implicant)
        shortened_func_sol = Context(f'({shortened_func})').truth_table
        if self.get_truth_table_row(shortened_func_sol) != self.get_truth_table_row(
                reduced_function_sol):
            influent_implicant = self.return_removed_implicants(influent_implicant, removable_implicants)
        return influent_implicant, removable_implicants

    def minimize_func_calculation_method(self):
        self.reduce_func()

        implicants_list = self.reduced_func.split(self.operation_out_constituents)
        influent_implicant, removable_implicants = self.process_implicants_for_calc(implicants_list)
        new_implicants = sorted(influent_implicant, key=len)
        self.minimized_func = self.operation_out_constituents.join(new_implicants)

    @staticmethod
    def find_removable_implicants_table_process(reduced_func_implicants, reverted_table, influent_impl):
        removable_implicants = set()
        for col in reverted_table:
            cover_implicant = [reduced_func_implicants[j] for j in range(len(col)) if col[j] == 1]
            if any(implicant in influent_impl for implicant in cover_implicant):
                continue
            cover_implicant.sort(key=len, reverse=True)
            removable_implicants.add(cover_implicant.pop())
        return removable_implicants

    @staticmethod
    def find_removable_implicants(reduced_func_implicants, implicant_table, influent_impl):
        reverted_table = list(map(list, zip(*implicant_table)))
        return Minimizer.find_removable_implicants_table_process(reduced_func_implicants, reverted_table, influent_impl)

    @staticmethod
    def get_truth_table_row(inter):
        return ''.join([str(interpretation.value) for interpretation in inter])

    def minimize_func_quine_method(self):
        self.reduce_func()

        reduced_func_implicants = self.reduced_func.split(self.operation_out_constituents)
        implicant_table = self.create_impl_table(reduced_func_implicants)
        unremovable_implicants = self.find_unremovable_implicants(reduced_func_implicants, implicant_table)
        removable_implicants = self.find_removable_implicants(reduced_func_implicants, implicant_table,
                                                              unremovable_implicants)
        self.minimized_func = self.operation_out_constituents.join(
            sorted(unremovable_implicants.union(removable_implicants), key=len))

    @staticmethod
    def find_unremovable_implicants(reduced_func_implicants: list[str], implicant_table):
        reverted_table = list(map(list, zip(*implicant_table)))
        unremovable_implicants = set(
            reduced_func_implicants[column.index(1)] for column in reverted_table if sum(column) == 1)
        return unremovable_implicants

    def create_impl_table(self, reduced_func_implicants: list[str]):
        table = [[0] * len(self.implicants) for _ in range(len(reduced_func_implicants))]
        for i in range(len(table)):
            for j in range(len(table[i])):
                if self.is_first_implicant_in_second(reduced_func_implicants[i], self.implicants[j]):
                    table[i][j] = 1
        return table

    def is_first_implicant_in_second(self, implicant: str, constituent: str):
        implicant_literals = self.get_literals(implicant)
        constituent_literals = self.get_literals(constituent)
        return all(literal in constituent_literals for literal in implicant_literals)
