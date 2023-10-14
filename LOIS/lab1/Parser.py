import re
from itertools import chain


class Parser:
    def __init__(self, data):
        self.data = data
        self.predicates = []
        self.parcels = []
        self.rules = []

    def delete_spaces(self):
        self.data = [item.replace(' ', '').replace('\n', '') for item in self.data]

    def parse_data(self):
        parcel_index = self.data.index('')
        rules_index = self.data[parcel_index + 1:].index('') + parcel_index + 1

        self.predicates.extend(self.data[:parcel_index])
        self.parcels.extend(self.data[parcel_index + 1: rules_index])
        self.rules.extend(self.data[rules_index + 1:])

    def validate(self):
        reg_exp = r"([A-Z]\d*)=(\{(\([a-z]\d*,\d(\.\d+)?\))(,\([a-z]\d*,\d(\.\d+)?\))*})|\{\}"
        for item in chain(self.predicates, self.parcels):
            if item != '' and not re.match(reg_exp, item):
                raise RuntimeError('invalid input format')

    @staticmethod
    def parse_set(set: list) -> list[dict]:
        parsed = []
        for item in set:
            splited = item.split('=')
            set_values: list[str] = splited[1].replace('{' ,'').replace('}', '').split('),')
            parsed.append(
                {'name': splited[0],
                 'set':
                     {
                        item.split(',')[0].replace('(', ''):
                        float(item.split(',')[1].replace(')', ''))
                        for item in set_values
                    }
                 }
            )
        return parsed


    def parse(self):
        self.delete_spaces()
        self.parse_data()
        self.validate()
        self.predicates = self.parse_set(self.predicates)
        self.parcels = self.parse_set(self.parcels)
        self.rules = [rule.split('~>') for rule in self.rules]
