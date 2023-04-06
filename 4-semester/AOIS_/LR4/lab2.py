import re
from collections import deque
from enum import Enum
from itertools import product


class Tokens(Enum):
    VARIABLE = 0
    LEFT_BRACKET = 1
    RIGHT_BRACKET = 2
    INVERSION = 3
    CONJUNCTION = 4
    DISJUNCTION = 5
    IMPLICATION = 6
    EQUIVALENCE = 7


class Context:
    AVAILABLE_TOKENS: dict = {
        '(': Tokens.LEFT_BRACKET,
        ')': Tokens.RIGHT_BRACKET,
        '!': Tokens.INVERSION,
        '*': Tokens.CONJUNCTION,
        '+': Tokens.DISJUNCTION,
        '→': Tokens.IMPLICATION,
        '↔': Tokens.EQUIVALENCE,
    }

    def __init__(self, logic_sentence: str):
        self.operation_priority = PriorityOfOperations()
        self.logical_sentence: str = logic_sentence.replace('<=>', '↔').replace('=>', '→')
        self.tokens = []
        self.tokens = self.get_tokens()
        self.vars = set(sorted(self.get_set_of_vars()))
        self.logical_expression = LogicalExpression(tokens=self.tokens)
        self.truth_table = []
        self.evaluate()

    def get_index_form(self) -> int:
        return sum([2 ** index * implementation.value for index, implementation in enumerate(self.truth_table[::-1])])

    def get_pcnf_number_form(self, return_list=None) -> str | list:
        pcnf_number_form = [str(i) for i, implementation in enumerate(self.truth_table) if
                            implementation.value == 0]
        return '*(' + ', '.join(pcnf_number_form) + ')' if not return_list else pcnf_number_form

    def get_pdnf_number_form(self, return_list=None) -> str | list:
        pdnf_number_form = [str(i) for i, implementation in enumerate(self.truth_table) if
                            implementation.value == 1]
        return '+(' + ', '.join(pdnf_number_form) + ')' if not return_list else pdnf_number_form

    def get_pcnf(self) -> str:
        disjunction = []
        for number in self.get_pcnf_number_form(return_list=True):
            implementation = self.truth_table[int(number)]
            vars = [var if value == 0 else '!' + var for var, value in
                    implementation.interpretation.items()]
            disjunction.append('(' + ' + '.join(vars) + ')')
        return ' * '.join(disjunction)

    def get_pdnf(self):
        conjuction = []
        for number in self.get_pdnf_number_form(return_list=True):
            implementation = self.truth_table[int(number)]
            vars = [var if value == 1 else '!' + var for var, value in
                    implementation.interpretation.items()]
            conjuction.append('(' + ' * '.join(vars) + ')')
        return ' + '.join(conjuction)

    def get_tokens(self):
        token_found = False
        end_of_var_index = 0
        for ind, char in enumerate(self.logical_sentence):
            if (token_found and ind < end_of_var_index) or char.isspace(): continue
            if char.isalpha():
                end_of_var_index = ind + 1
                while end_of_var_index < len(self.logical_sentence) and self.logical_sentence[
                    end_of_var_index].isalnum():
                    end_of_var_index += 1
                token_str = self.logical_sentence[ind:end_of_var_index]
                token_type = Tokens.VARIABLE
                token = Token(token_type, token_str, self.operation_priority[new_token_type])
                self.tokens.append(token)
                token_found = True
            elif self.AVAILABLE_TOKENS.get(char, False):
                new_token_type = self.AVAILABLE_TOKENS[char]
                token = Token(new_token_type, char, self.operation_priority[new_token_type])
                self.tokens.append(token)

        return self.tokens

    def get_set_of_vars(self):
        pattern = r'[a-zA-Z]\w*'
        variables = set(re.findall(pattern, self.logical_sentence))
        return variables

    def evaluate(self):
        permutations = sorted(list(product([0, 1], repeat=len(self.vars))))
        for perm in permutations:
            interpret = dict(zip(self.vars, perm))
            self.logical_expression.evaluate(interpret, self.truth_table)

    def print_table(self):
        for var in self.vars:
            print(var, end='\t')
        print(self.logical_sentence)
        for inter in self.truth_table:
            for value in inter.interpretation.values():
                print(str(value), end='\t')
            print(str(inter.value))


class LogicalExpression:
    def __init__(self, tokens):
        self.token_list = tokens
        self.var_stack = []
        self.operations_stack = []
        
    
        
    def evaluate(self, interpretation_row, truth_table):
        self.interpretation = {**interpretation_row}
        for token in self.token_list:
            self.process_token(token)
        while self.operations_stack:
            self.process_operation()
        truth_table.append(TruthTableRow(interpretation_row, self.var_stack.pop()))
    
    def process_token(self, token):
        match token.type:
            case Tokens.VARIABLE:
                self._process_variable(token)
                return
            case Tokens.LEFT_BRACKET:
                self._process_left_bracket(token)
                return
            case Tokens.RIGHT_BRACKET:
                self._process_right_bracket()
                return
        self._process_operator(token)
    
    def _process_variable(self, token):
        self.var_stack.append(self.interpretation[token.value])
    
    def _process_left_bracket(self, token):
        self.operations_stack.append(token)
    
    def _process_operator(self, token):
        if not self.operations_stack or \
                self.operations_stack[-1].type == Tokens.LEFT_BRACKET:
            self.operations_stack.append(token)
        else:
            while self.operations_stack and token.priority >= self.operations_stack[-1].priority \
                    and self.operations_stack[-1].type != Tokens.LEFT_BRACKET:
                self.process_operation()
            self.operations_stack.append(token)

    def _process_right_bracket(self):
        while self.operations_stack[-1].type != Tokens.LEFT_BRACKET:
            self.process_operation()
        self.operations_stack.pop()

    def process_operation(self):
        operation = self.operations_stack.pop()
        if operation.type == Tokens.INVERSION:
            operand = self.var_stack.pop()
            self.var_stack.append(int(not operand))
        else:
            right_operand = self.var_stack.pop()
            left_operand = self.var_stack.pop()
            match operation.type:
                case Tokens.CONJUNCTION:
                    self.var_stack.append(int(left_operand and right_operand))
                case Tokens.DISJUNCTION:
                    self.var_stack.append(int(left_operand or right_operand))
                case Tokens.IMPLICATION:
                    self.var_stack.append(int((not left_operand) or right_operand))
                case Tokens.EQUIVALENCE:
                    self.var_stack.append(int(left_operand == right_operand))


class Token:
    def __init__(self, type: Tokens, value, priority: int):
        self.type = type
        self.value = value
        self.priority = priority


class PriorityOfOperations:
    def __init__(self):
        self.operations = {
            Tokens.LEFT_BRACKET: -1,
            Tokens.VARIABLE: -1,
            Tokens.RIGHT_BRACKET: -1,
            Tokens.INVERSION: 0,
            Tokens.CONJUNCTION: 1,
            Tokens.DISJUNCTION: 2,
            Tokens.IMPLICATION: 3,
            Tokens.EQUIVALENCE: 4,
        }

    def __getitem__(self, item):
        return self.operations[item]


class TruthTableRow:
    def __init__(self, interpretation: dict, value: int):
        self.interpretation = interpretation
        self.value = value

if __name__=='__main__':

    logical_expression: str = '(!((!x1+!x2)&!(x1&x3)))'
    # formula: str = 'x1*x2+x3'
    # formula: str = '(x1+x2)*x3*(x2+x4)'
    # formula: str = 'x1 => x2'
    context = Context(logical_expression)
    context.print_table()
    print(f"PCNF: {context.get_pcnf()}\n")
    print(f'PCNF number form: {context.get_pcnf_number_form()}\n')
    print(f"PDNF: {context.get_pdnf()}\n", )
    print(f'PDNF number form: {context.get_pdnf_number_form()}\n')
    print(f'Index form = {context.get_index_form()}\n')
