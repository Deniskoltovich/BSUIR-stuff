import re

# Функция для считывания данных с файла
def read_file():
    with open('input.txt', 'r') as file:
        return file.read()

# Удаляем пробелы и переводы строк в строке, считанной с файла
def delete_spaces(file_content):
    return re.sub(r'[\r\n ]', '', file_content)

# Функция нахождения количества знаков равно
def find_equals_signs(data):
    return data.count('=')

# Функция проверки количества знаков равно
def check_equals_signs(data):
    if find_equals_signs(data) == 3:
        print('Количество знаков равно совпадает')
    else:
        raise

# Функция нахождения имён множеств
def find_names_sets(data):
    return len(re.findall(r'[A-Z]\d*=', data))

# Функция проверки количества имён множеств
def check_names_sets(data):
    if find_names_sets(data) == 3:
        print('Количество множеств совпадает')
    else:
        raise

# Функция, выделяющая элементы массива
def find_sets(data):
    return re.sub(r'[A-Z]\d*=', ' ', data).split()[1:]

# Проверяет соответствие алфавиту нечёткого множества
def check_alphabet_correspondence(set):
    if re.match(r'^[A-Za-z0-9)(}{,.]+$', set):
        print(f'Множество {set} не содержит недопустимых символов')
    else:
        raise

# Проверяет соответствие алфавиту всех множеств
def check_all_sets_alphabet_correspondence(sets):
    for set in sets:
        check_alphabet_correspondence(set)

# Функция проверки множества на правильный ввод фигурных скобок
def check_braces(set):
    if set[0] == '{' and set[-1] == '}':
        print(f'Множество {set} введено правильно')
    else:
        raise

# Функция проверки всех начальных множеств на правильный ввод фигурных скобок
def check_all_sets_braces(sets):
    for set in sets:
        check_braces(set)

# Функция удаления фигурных скобок в множестве
def delete_braces(set):
    return set[1:-1]

# Функция удаления фигурных скобок во всех множествах
def delete_all_sets_braces(sets):
    return [delete_braces(set) for set in sets]

# Функция, которая проверяет, действительно ли в множестве содержатся кортежи,
# без проверки контента внутри
def is_right_set(set):
    if re.match(r'^\(.*\)(,\(.*\))*$', set):
        print(f'The {set} is right')
    else:
        raise

# Функция, проверяющая действительность всех кортежей во всех множествах
def is_right_all_sets(sets):
    for set in sets:
        is_right_set(set)

# Функция нахождения элементов множества
def find_elements(set):
    open_brace = 0
    open_bracket = 0
    start_index = 0
    elements = []
    
    for i in range(len(set)):
        if set[i] == '(':
            open_bracket += 1
        elif set[i] == '{':
            open_brace += 1
        elif set[i] == ')':
            if i == len(set) - 1:
                elements.append(set[start_index:i + 1])
            open_bracket -= 1
        elif set[i] == '}':
            open_brace -= 1
        else:
            if set[i] == ',' and open_brace == 0 and open_bracket == 0:
                elements.append(set[start_index:i])
                start_index = i + 1
    
    return elements

# Функция нахождения элементов всех множеств
def find_all_sets_elements(sets):
    result_sets = {}
    for i, set in enumerate(sets):
        result_sets[i] = find_elements(set)
    return result_sets

# Главная функция
def main():
    ALPHABET = r"{}(),.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    file_content = read_file()
    print(file_content)

    data = delete_spaces(file_content)
    check_equals_signs(data)
    print(data)
    check_names_sets(data)

    sets = find_sets(data)
    check_all_sets_alphabet_correspondence(sets)
    check_all_sets_braces(sets)

    sets = delete_all_sets_braces(sets)
    print(sets)
    is_right_all_sets(sets)

    print(find_all_sets_elements(sets))

if __name__ == "__main__":
    main()