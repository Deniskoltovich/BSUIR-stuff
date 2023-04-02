from lab2copy import Context, TruthTableRow
from itertools import permutations



class Minimizer:
    
    CONJUNCTION = ' * '
    DISJUNCTION = ' + '
    
    def __init__(self, raw_formula: str, mode):
        self.mode = mode
        self.context = Context(raw_formula)
        self.vars = self.context.vars
        self.operation_in_constituents, self.operation_out_constituents = [self.CONJUNCTION, self.DISJUNCTION] if 'DNF' in mode \
            else [self.DISJUNCTION, self.CONJUNCTION]
        self.non_minimized_func = Context(raw_formula).get_pcnf() if 'CNF' in mode else Context(raw_formula).get_pdnf()
        self.implicants_set = sorted(self.non_minimized_func.split(self.operation_out_constituents))
        self.reduced_func = self.non_minimized_func
        self.minimized_func = None
        
    def create_karnough_table(self, *vars):
        var1, var2, var3 = vars
        table = [[0 for _ in range(5)] for _ in range(3)]
        oper = self.operation_in_constituents
        table[1][0], table[2][0], table[0][1], table[0][2], table[0][3], table[0][4] = \
            var1, '!' + var1, f'!{var2}{oper}!{var3}', f'!{var2}{oper}{var3}', f'{var2}{oper}{var3}', f'{var2}{oper}!{var3}'
        truth_table = self.context.truth_table
        column = {'00': 1, '01': 2, '11' : 3, '10': 4 }
        for row in truth_table:
            value = row.value
            interp: dict = row.interpretation
            temp: str = str(interp[var2]) + str(interp[var3])
            table[interp[var1] + 1][column[temp]] = value
            
        return table
            
    def process_table(self, table):
        constant = 1 if self.mode == 'DNF' else 0
        neigthboor_indexes = []
        founded = []
        for row_ind, row in enumerate(table):
            if row_ind == 0: continue
            if row.count(constant) == 4:
                neigthboor_indexes.append([row_ind, row_ind])
                founded.extend([[row_ind, 0], [row_ind, 1], [row_ind, 2], [row_ind, 3] ])

                continue
            
        for row_ind, row in enumerate(table):
            if row_ind == 0: continue
            num_of_skips = 0
            for col_ind, col_value in enumerate(row):
                if num_of_skips > 1 or col_ind == 0:
                    num_of_skips -= 1
                    continue
                if col_ind != 4 and col_value == constant and table[row_ind][col_ind + 1] == constant and \
                    row_ind != 2 and table[row_ind + 1][col_ind] == constant and table[row_ind + 1][col_ind + 1] == constant:
                    neigthboor_indexes.append([col_ind, col_ind + 1, 0])
                    founded.extend([[row_ind, col_ind], [row_ind + 1, col_ind + 1], [row_ind + 1, col_ind], [row_ind, col_ind + 1] ])
                    num_of_skips = 2
                num_of_skips -= 1
        
        for row_ind, row in enumerate(table):
            if row_ind == 0: continue
            for col_ind, col_value in enumerate(row):
                if col_ind == 0 or num_of_skips > 1: 
                    num_of_skips -= 1
                    continue
                if col_ind == 1 and col_value == constant and row[-1] == constant \
                        and [row_ind, 4] not in founded and [row_ind, col_ind] not in founded:
                    neigthboor_indexes.append([row_ind, row_ind, col_ind, -1])
                
                elif row_ind != 2 and col_value == constant and table[row_ind + 1][col_ind] == constant \
                        and [row_ind, col_ind] not in founded and [row_ind + 1, col_ind] not in founded:
                    num_of_skips = 2
                    neigthboor_indexes.append([row_ind, row_ind + 1, col_ind, col_ind])
                elif col_ind != 4 and col_value == constant and table[row_ind][col_ind + 1] == constant\
                        and [row_ind, col_ind] not in founded and [row_ind, col_ind + 1] not in founded:
                    num_of_skips = 2
                    neigthboor_indexes.append([row_ind, row_ind, col_ind, col_ind + 1])
         
        return self.concat_for_karnough(table, neigthboor_indexes)
        
    def concat_for_karnough(self, table, neigthboor_indexes):
        implicants = []
        for item in neigthboor_indexes:
            if len(item) == 2:
                implicant: str = table[item[0]][0]
                implicants.append(implicant)
            elif len(item) == 3:
                implicant1 = table[0][item[0]]
                implicant2 = table[0][item[1]]
                implicant = self.union_implicants(implicant1, implicant2)
                implicants.append(implicant)
            else:
                implicant1 = table[item[0]][0] + self.operation_in_constituents + table[0][item[2]]
                implicant2 = table[item[1]][0] + self.operation_in_constituents + table[0][item[3]]
                implicant = self.union_implicants(implicant1, implicant2)
                implicants.append(implicant)
                
        return implicants
                
        #TODO: union implicants
        
    def karnough_method(self):
        # perm = list(permutations(sorted(self.vars)))
        implicants = self.process_table(self.create_karnough_table(*sorted(self.vars)))
        implicants = [i for i in implicants if i]
        
        self.minimized_func = self.operation_out_constituents.join(implicants)
        

    def reduce_func(self, implicants=None):
        if implicants is None:
            implicants = self.implicants_set
        new_implicants = self.process_implicants_to_reduce(implicants)
        new_func = self.operation_out_constituents.join(set(sorted(new_implicants)))
        if new_func != self.reduced_func:
            self.reduced_func = new_func
            self.reduce_func(implicants=new_implicants)

    def process_implicants_to_reduce(self, implicants_list):
        new_implicants_list = []
        concatenated_implicants = []
        for i, implicants_i in enumerate(implicants_list):
            for j, implicants_j in enumerate(implicants_list):
                if i != j:
                    new_implicant = self.union_implicants(implicants_i, implicants_j)
                    if new_implicant:
                        new_implicants_list.append(new_implicant)
                        concatenated_implicants += [implicants_i, implicants_j]
        new_implicants_list += [implicant for implicant in implicants_list if implicant not in concatenated_implicants]
        return new_implicants_list
       

    def union_implicants(self, implicant_1: str, implicant_2: str):
        literals_1 = self.get_literals(implicant_1)
        literals_2 = self.get_literals(implicant_2)
        if not self.is_removable_implicants(literals_1, literals_2):
            return
        for var in self.vars:
            if f'!{var}'  in literals_1 and var in literals_2:
                literals_1.remove(f'!{var}')
                literals_2.remove(var)
            elif var in literals_1 and f'!{var}' in literals_2:
                literals_1.remove(var)
                literals_2.remove(f'!{var}')
        try:
            for literal in literals_1:
                literals_2.remove(literal)
        except Exception:
            ...
        else:
            return self.implicant_string(literals_1 + literals_2)

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

    def minimize_func_calculation_method(self):
        self.context.print_table()
        self.reduce_func()
        implicants_list = self.reduced_func.split(self.operation_out_constituents)
        influent_implicant, removable_implicants = [], []
        reduced_function_sol = Context(f'({self.reduced_func})').truth_table
        for implicant in implicants_list:
            other_implicants = [i for i in implicants_list if i != implicant]
            new_formula =  f'({self.operation_out_constituents.join(other_implicants)})'
            shortened_func_sol = Context(new_formula).truth_table
            influent_implicant.append(implicant) \
                if self.get_truth_table_row(shortened_func_sol) != self.get_truth_table_row(reduced_function_sol) \
            else removable_implicants.append(implicant)
            
        shortened_func = self.operation_out_constituents.join(influent_implicant)
        shortened_func_sol = Context(f'({shortened_func})').truth_table
        if self.get_truth_table_row(shortened_func_sol) != self.get_truth_table_row(
                reduced_function_sol):
            influent_implicant = self.return_removed_implicants(influent_implicant, removable_implicants)
        self.minimized_func = self.operation_out_constituents.join(sorted(influent_implicant, key=len))

    def return_removed_implicants(self, necessary_implicants: list[str], unnecessary_implicants: list[str]):
        unnecessary_implicants.sort(key=len, reverse=True)
        shortened_func = self.operation_out_constituents.join(necessary_implicants)
        solution_for_shortened_func = Context(f'({shortened_func})').truth_table
        solution_for_reduced_func = Context(f'({self.reduced_func})').truth_table

        while self.get_truth_table_row(solution_for_shortened_func) != self.get_truth_table_row(solution_for_reduced_func):
            necessary_implicants += [unnecessary_implicants.pop()]
            shortened_func = self.operation_out_constituents.join(necessary_implicants)
            solution_for_shortened_func = Context(f'({shortened_func})').truth_table
        return necessary_implicants

    def minimize_func_quine_method(self, print_table=None):
        self.context.print_table()
        self.reduce_func()
        reduced_func_implicants = self.reduced_func.split(self.operation_out_constituents)
        implicant_table = self.create_impl_table(reduced_func_implicants)
        if print_table:
            self.print_implicant_table(reduced_func_implicants, implicant_table)
        unremovable_implicants = self.find_unremovable_implicants(reduced_func_implicants, implicant_table)
        removable_implicants = self.find_removable_implicants(reduced_func_implicants, implicant_table, unremovable_implicants)
        self.minimized_func = self.operation_out_constituents.join(sorted(unremovable_implicants.union(removable_implicants), key=len))

    @staticmethod
    def find_unremovable_implicants(reduced_func_implicants: list[str], implicant_table):
        reverted_table = list(map(list, zip(*implicant_table)))
        unremovable_implicants = set(reduced_func_implicants[column.index(1)] for column in reverted_table if sum(column) == 1)
        return unremovable_implicants

    @staticmethod
    def find_removable_implicants(reduced_func_implicants: list[str], implicant_table, core_implicants):
        convenient_implicant_table = list(map(list, zip(*implicant_table)))
        removable_implicants = set()
        for col in convenient_implicant_table:
            cover_implicant = [reduced_func_implicants[j]
                                    for j in range(len(col)) if col[j] == 1]
            if any(implicant in core_implicants for implicant in cover_implicant):
                continue
            cover_implicant.sort(key=len, reverse=True)
            removable_implicants.add(cover_implicant.pop())
        return removable_implicants

    def print_implicant_table(self, reduced_func_implicants: list[str], implicant_table):
        print(' ' * 20 + ' '.join(self.implicants_set))
        for i in range(len(implicant_table)):
            print(reduced_func_implicants[i].center(20, ' ') +
                  ' '.join(['1'.center(len(self.implicants_set[j]), ' ') if implicant_table[i][j] == 1
                            else '0'.center(len(self.implicants_set[j]), ' ')
                            for j in range(len(implicant_table[i]))]).center(
                      len(' '.join(self.implicants_set)), ' '
                  ))

    def is_first_implicant_in_second(self, implicant: str, constituent: str):
        implicant_literals = self.get_literals(implicant)
        constituent_literals = self.get_literals(constituent)
        return all(literal in constituent_literals for literal in implicant_literals)

    def create_impl_table(self, reduced_func_implicants: list[str]):
        table = [[0] * len(self.implicants_set) for _ in range(len(reduced_func_implicants))]
        for i in range(len(table)):
            for j in range(len(table[i])):
                if self.is_first_implicant_in_second(reduced_func_implicants[i], self.implicants_set[j]):
                    table[i][j] = 1
        return table

    @staticmethod
    def get_truth_table_row(solution: list[TruthTableRow]):
        return ''.join([str(interpretation.value) for interpretation in solution])

    def implicant_string(self, literals_list: list[str]):
        return '(' + self.operation_in_constituents.join(literals_list) + ')'
