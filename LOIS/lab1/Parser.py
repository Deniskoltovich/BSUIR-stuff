'''
Лабораторная работа №1 по дисциплине ЛОИС
Выполнена студентами группы 121702 БГУИР Колтовичем Д., Зайцем Д., Кимстачем Д.
Вариант 1: импликация Гёделя
Задача: разработать программу, выполняющую прямой нечеткий логический вывод
'''


import re
from itertools import chain


class Parser:
    def __init__(self, data):
        self.data = data
        self.predicates = []
        self.rules = []

    def delete_spaces(self):
        """Удаляет пробельные символы в self.data"""
        self.data = [item.replace(' ', '').replace('\n', '') for item in self.data]

    def parse_data(self):
        """
        Разбивает self.data на предикаты и правила
        """
        # parcel_index = self.data.index('')
        # rules_index = self.data[parcel_index + 1:].index('') + parcel_index + 1
        #
        # self.predicates.extend(self.data[:parcel_index])
        # self.parcels.extend(self.data[parcel_index + 1: rules_index])
        # self.rules.extend(self.data[rules_index + 1:])
        rules_index = self.data.index('')
        self.predicates.extend(self.data[:rules_index])
        self.rules.extend(self.data[rules_index + 1:])


    def validate(self):
        reg_exp = r"([A-Z]\d*)=(\{(\<[a-z]\d*,\d(\.\d+)?\>)(,\<[a-z]\d*,\d(\.\d+)?\>)*})|\{\}"
        for item in self.predicates:
            if item != '' and not re.match(reg_exp, item):
                raise RuntimeError('invalid input format')

    @staticmethod
    def parse_set(sets: list) -> list[dict]:
        """
        приводит нечеткие множества set в список с элементами формата:
        {'name': 'A', 'set': {'x1': 0.1, 'x2': 0,2}}
        """
        parsed = []
        for item in sets:
            splited = item.split('=')
            set_values: list[str] = splited[1].replace('{' ,'').replace('}', '').split('>,')
            data = {'name': splited[0],
                 'set':
                     {
                        item.split(',')[0].replace('<', ''):
                        float(item.split(',')[1].replace('>', ''))
                        for item in set_values
                    }
                 }
            if len(data.get('set')) != len(set_values):
                print(f'Внимание! Множество {item} содержит элементы с одинаковым названием, сохранено будет только последнее вхождение этого элемента')
            parsed.append(data)
        return parsed

    def parse(self):
        self.delete_spaces()
        self.parse_data()
        self.validate()
        self.predicates = self.parse_set(self.predicates)
        self.rules = [rule.split('~>') for rule in self.rules]
