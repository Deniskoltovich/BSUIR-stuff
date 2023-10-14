from implication import Implication
from Parser import Parser
from generateAllRules import GenerateAllRules

def main():
    # Считываем информацию с файла
    with open('input.txt', 'r') as f:
        data = f.readlines()


    # Парсим информацию, которую считали с файла
    parser = Parser(data)
    parser.parse()

    for rule in parser.rules:
        first_predicate = next(predicate for predicate in parser.predicates if predicate['name'] == rule[0])
        second_predicate = next(predicate for predicate in parser.predicates if predicate['name'] == rule[1])
        for parcel in parser.parcels:
            implication = Implication(first_predicate, second_predicate, parcel)
            implication.calculate()
    # for rule in all_rules:
    #     first_predicate = wnext(element for element in parser.predicate if element['name'] == rule[0])
    #     second_predicate = next(element for element in parser.predicate if element['name'] == rule[1])
    #     for parcel in parser.parcel:
    #         implicate = ImplicationCopy(first_predicate, second_predicate, parcel)
    #         print(f"Rule: {rule[0]}~>{rule[1]}, and parcel: {parcel['name']}")
    #         implicate.calculate()

if __name__ == "__main__":
    main()
