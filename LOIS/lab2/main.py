'''
Лабораторная работа №2 по дисциплине ЛОИС
Выполнена студентами группы 121702 БГУИР Колтовичем Д., Зайцем Д., Кимстачем Д.
Алгоритм продумывался совместно со студентами группы 121702 Летко А., Нагла Н., Голушко Д.
Вариант 6: нечеткая композиция (max({min({x_i} U {y_i}) | i})
Задача: разработать программу, выполняющую обратный нечеткий логический вывод
'''

from Parser import Parser
from solver import InverseFuzzyInference

if __name__ == '__main__':
    # Считываем информацию с файла
    with open('inputs/input1.txt', 'r') as f:
        data = f.readlines()

    parser = Parser(data)
    parser.parse()

    for rule in parser.rules:
        print('Правило:', parser.format_rule(rule), end='\n\n')
        for predicate in parser.predicates:
            print('Нечёткий предикат, задающий множество следствий:', parser.format_set(predicate))
            solver = InverseFuzzyInference(logical_conclusion=predicate, rule=rule)
            solver.run()
