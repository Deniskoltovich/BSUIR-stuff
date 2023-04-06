from typing import List
from itertools import product
from lab_lib import Minimizer 
class Operations:
    inversion = '!'
    conjunction = '*'
    disjunction = '+'
    trueConjunction = "/\\"
    trueDisjunction = "\\/"
    
    
carrySDNF = "(!x1*!x2*x3) + (!x1*x2*!x3) + (!x1*x2*x3) + (x1*x2*x3)"
resultSDNF = "(!x1*!x2*x3) + (!x1*x2*!x3) + (x1*!x2*!x3) + (x1*x2*x3)"


def fill_operand_list(expression: str) -> List[str]:
    return expression.split("+")

def find_b(minuend: int, subtrahend: int, borrow_in: int):
    return int((not minuend and subtrahend) or (not minuend and borrow_in) or (subtrahend and borrow_in))


def find_d(minuend: int, subtrahend: int, borrow_in: int):
    return int(minuend ^ subtrahend ^ borrow_in)

def draw_subtractor_truth_table(operand_list: List[str]):
    print(f"|{operand_list[0]} |{operand_list[1]} |{operand_list[2]} | b | d |")
    perms = sorted(list(product([0, 1], repeat=3)))
    print("|---|---|---|---|---|")
    sdnf_table = [[] for _ in range(2)]

    for perm in perms:
        x1, x2, x3 = perm
        print(f'| {x1} | {x2} | {x3} | {find_b(x1, x2, x3)} | {find_d(x1, x2, x3)} |')

        

def add_bin_6(x1: str) -> str:
    res = bin(int(x1, 2) + 6)[2:]
    while len(res) != 4: res = '0' + res
    return res

def draw_8421_plus_6_truth_table(operand_list):
    print(f"|{operand_list[0]} |{operand_list[1]} |{operand_list[2]} |{operand_list[3]} |y1 |y2 |y3 |y4 |")
    perms = sorted(list(product([0, 1], repeat=4)))
    print("|---|---|---|---|---|---|---|---|")
    y_sdnf_table = [[] for _ in range(4)]


    for i, perm in enumerate(perms):
        x1, x2, x3, x4 = perm
        if i < 10:
            res_str = add_bin_6(f'{x1}{x2}{x3}{x4}')
            print(f"| {x1} | {x2} | {x3} | {x4} | {res_str[0]} | {res_str[1]} | {res_str[2]} | {res_str[3]} |")
            for j in range(4):
                if res_str[j] == '1':
                    constituent = "".join([f'!x{i+1}*' if x == 0 else f'x{i+1}*' for i,x in enumerate([x1, x2, x3, x4])])
                    y_sdnf_table[j].append(f"({constituent[:len(constituent) -1]})")
        else: 
            print(f"| {x1} | {x2} | {x3} | {x4} |---|---|---|---|")
        
    y_sdnf_table = [Operations.disjunction.join(x) for x in y_sdnf_table] 
    return y_sdnf_table


def ODV(operandList):
    print(f"Таблица истинности для двоичного вычитателя:")
    draw_subtractor_truth_table(operandList)
    global carrySDNF, resultSDNF
    print(f"Функция остатка b (carry) в СДНФ: {carrySDNF}")
    print(f"Функция результата d (result) в СДНФ: {resultSDNF}")
    min = Minimizer(carrySDNF)
    min.minimize_func_quine_method()
    minbSDNF = min.minimized_func
    print(f"Минимизированная функция b (carry): {minbSDNF}")

    min = Minimizer(resultSDNF)
    min.minimize_func_quine_method()
    mindSDNF = min.minimized_func
    print(f"Минимизированная функция d (result): {mindSDNF}")


def D8421n(operandList):
    print(f"\nТаблица истинности для Д8421 -> Д8421+6:")
    y_table = draw_8421_plus_6_truth_table(operandList)
    print("Формулы y1, y2, y3, y4 в СДНФ:")
    print('y1:\t', y_table[0])
    print('y2:\t', y_table[1])
    print('y3:\t', y_table[2])
    print('y4:\t', y_table[3])
    print("Минимизированные y1, y2, y3, y4:")
    min = Minimizer(y_table[0])
    min.minimize_func_quine_method()
    print('y1:\t', min.minimized_func)
    min = Minimizer(y_table[1])
    min.minimize_func_quine_method()
    print('y2:\t', min.minimized_func)
    min = Minimizer(y_table[2])
    min.minimize_func_quine_method()
    print('y3:\t', min.minimized_func)
    min = Minimizer(y_table[3])
    min.minimize_func_quine_method()
    print('y4:\t', min.minimized_func)
    

ops = ['x1', 'x2', 'x3', 'x4']
operandListTask1 = ops
operandListTask2 = ops
ODV(operandListTask1);
D8421n(operandListTask2);
