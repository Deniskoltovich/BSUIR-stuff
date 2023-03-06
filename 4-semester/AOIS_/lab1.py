def decimal_to_binary(number: int) -> list:
    save_number = number
    number = abs(number)
    binary = []
    while number:
        binary.append(number % 2)
        number //= 2
    binary.append(0 if save_number >= 0 else 1)
    binary = binary[::-1]
    binary = binary[:1] + [0] * (8 - len(binary)) + binary[1:]
    return binary


def floating_point_to_decimal(floating_point_number):
    decimal_degree: int = convert_to_decimal([0] + floating_point_number[1]) - 127
    digit_degree = 0
    mantissa_result: float = 0
    for digit in floating_point_number[2]:
        mantissa_result += int(digit) * 2 ** digit_degree
        digit_degree -= 1
    return (1 - 2 * int(floating_point_number[0])) * mantissa_result * 2 ** decimal_degree


def normalize_length(num1, num2, length: int | None = None, save_sign=False):
    if not length:
        max_len = max(len(num1), len(num2))
    else:
        max_len = length
    if save_sign:
        unsigned_num1 = num1[:1] + [0] * abs(max_len - len(num1)) + num1[1:]
        unsigned_num2 = num2[:1] + [0] * abs(max_len - len(num2)) + num2[1:]
    else:
        unsigned_num1 = [0] * abs(max_len - len(num1)) + num1[1:]
        unsigned_num2 = [0] * abs(max_len - len(num2)) + num2[1:]
    return unsigned_num1, unsigned_num2


def binary_sum(unsigned_num1: list, unsigned_num2: list, length=None, save_carry=False, save_sign=False):
    unsigned_num1, unsigned_num2 = normalize_length(unsigned_num1, unsigned_num2, length=length, save_sign=save_sign)
    result = []
    carry = 0
    for i in range(len(unsigned_num1) - 1, -1, -1):
        current_bit = carry
        current_bit += int(unsigned_num1[i]) + int(unsigned_num2[i])

        result = [current_bit % 2] + result
        carry = current_bit >= 2

    if save_carry:
        return result, carry
    return result


def subtraction(num1: list, num2: list, num_size=None):
    return summ(num1, [int(not num2[0])] + num2[1:], num_size=num_size)


def mul(num1: list, num2: list):
    unsigned_num1, unsigned_num2 = normalize_length(num1, num2, length=None)
    table_size = len(unsigned_num1) + len(unsigned_num1)
    multiplication_table = []
    place_holder_size = 0

    for x2_digit in unsigned_num2[::-1]:
        partial_solution = [x2_digit * x for x in unsigned_num1]
        partial_solution = [0] * (table_size - place_holder_size - len(partial_solution)) \
                           + partial_solution + [0] * place_holder_size
        multiplication_table.append(partial_solution)
        place_holder_size += 1
    temp_sum = [0] * table_size
    for partial_solution in multiplication_table:
        temp_sum = summ(temp_sum, partial_solution, num_size=table_size)[1:]

    res = [int(num1[0] != num2[0])] + temp_sum

    return res


def from_additional_to_direct(bin_number):
    if bin_number[0] == 0:
        return bin_number
    one = [0] * (len(bin_number) - 1) + [1]
    for i in range(len(bin_number) - 1, -1, -1):
        if bin_number[i] == 0:
            bin_number[i] = 1
        else:
            bin_number[i] = 0
            break
    else:
        bin_number = [1] + [0] * (len(bin_number) - 2) + [1]
    return reverse_binary_code(bin_number)


def binary_numbers_division(num1: list, x2: list):
    unsigned_x1, unsigned_x2 = num1[1:], x2[1:]
    unsigned_x1, unsigned_x2 = unsigned_x1[unsigned_x1.index(1):], unsigned_x2[unsigned_x2.index(1):]
    quotient, temp_divident = [], []
    shift = False
    sub = False
    for digit in unsigned_x1:
        temp_divident += [digit]
        max = get_max_from_binary([0] + unsigned_x2, [0] + temp_divident)
        if max == [0] + unsigned_x2 and max != [0] + temp_divident:
            quotient += [0]

            continue
        quotient += [1]
        sub = from_additional_to_direct(subtraction([0] + temp_divident, [0] + unsigned_x2)[1:])
        temp_divident = from_additional_to_direct(sub)
        shift = True
        sub = True
    # TODO можно ремайндер добавить
    return [int(num1[0] + x2[0] == 1)] + [0] * (8 - len(quotient) - 1) + quotient


def get_max_from_binary(num1: list, num2: list, signed=False) -> list:
    if signed:
        return num1 if int("".join(str(x) for x in num1), 2) \
                       > int("".join(str(x) for x in num2), 2) else num2
    return num1 if int("".join(str(x) for x in num1[1:]), 2) \
                   > int("".join(str(x) for x in num2[1:]), 2) else num2


def summ(num1: list, num2: list, num_size: int | None = None):
    unsigned_num1, unsigned_num1 = [], []
    if not num_size:
        unsigned_num1, unsigned_num2 = normalize_length(num1, num2, length=8)
    else:
        unsigned_num1, unsigned_num2 = normalize_length(num1, num2, length=num_size)
    num1, num2 = num1[:1] + unsigned_num1, num2[:1] + unsigned_num2
    max_number = get_max_from_binary(num1, num2)
    num1 = from_direct_to_additional(num1)
    num2 = from_direct_to_additional(num2)
    if (num1[0] + num2[0]) % 2 == 0:
        return [num1[0] or num2[0]] + binary_sum(num1, num2)
    elif max_number[0] == 0:
        result = binary_sum(num1, num2)
        result[0] = 0
        return result
    else:
        return [1] + binary_sum(num1, num2)


def from_direct_to_additional(number: list) -> list:
    if number[0] == 0:
        return number
    reversed = reverse_binary_code(number)
    for i in range(len(reversed) - 1, -1, -1):
        if reversed[i] == 0:
            reversed[i] = 1
            break
        else:
            reversed[i] = 0
    return reversed


def reverse_binary_code(number: list) -> list:
    if number[0] == 0:
        return number
    return number[:1] + [int(not digit) for digit in number[1:]]


def mantissa_sum(first_bin,
                 second_bin):
    first_mantissa = [int(first_bin[0])] + [int(x) for x in first_bin[2]]
    sec_mantissa = [int(second_bin[0])] + [int(x) for x in second_bin[2]]
    first_mantissa = first_mantissa[:1] + from_direct_to_additional(first_mantissa)
    second_mantissa = sec_mantissa[:1] + from_direct_to_additional(sec_mantissa)  # TODO mb not [0]
    exponent = first_bin[1]
    new_mantissa = [0] + binary_sum(first_mantissa, second_mantissa)  # TODO mb not [0]
    if new_mantissa[:2] == [1, 0] or new_mantissa[:2] == [0, 1]:
        exponent = binary_sum(exponent, [0, 0, 0, 0, 0, 0, 0, 1], save_sign=True)
        new_mantissa = new_mantissa[:1] + new_mantissa[:len(new_mantissa) - 1]
    sign = 0 if new_mantissa[:2] == [0, 0] else 1
    new_mantissa = from_direct_to_additional(new_mantissa[1:])[1:]
    return [sign, exponent, new_mantissa]


def convert_to_decimal(binary_number: list[int]) -> int:
    number = int("".join(str(x) for x in binary_number[1:]), 2)
    number *= -1 if binary_number[0] == 1 else 1
    return number


def create_mantissa(binary_number: str) -> str:
    mantissa = binary_number[binary_number.find("1"):]
    if len(mantissa) < 23:
        mantissa += "0" * (23 - len(mantissa))
    else:
        mantissa = mantissa[:23]
    return mantissa


def create_exponent(digit_order: int) -> list:
    exponent: list = summ(decimal_to_binary(127), decimal_to_binary(digit_order), num_size=9)[1:]
    exponent = [0] * (8 - len(exponent)) + exponent
    return exponent


def normalize_bin_float(number: int) -> list:
    sign = "1" if number < 0 else "0"
    binary_number = float_to_binary(number, numsize=32)[1:]
    digit_order = binary_number.find(".") - (binary_number.find("1") + 1)
    digit_order += 1 if digit_order < 0 else 0
    binary_number_list: list = list(binary_number)
    binary_number_list.pop(binary_number_list.index("."))
    binary_number = "".join(binary_number_list)
    return [sign, create_exponent(digit_order), create_mantissa(binary_number)]


def float_to_binary(number: float, numsize: int = 16) -> str:
    sign = "1" if number < 0 else "0"
    number = abs(number)
    int_part = int(number)
    float_part: float = number - float(int_part)
    binary_number = [str(x) for x in decimal_to_binary(int_part)[1:]]
    binary_number = "".join(binary_number)
    index_of_one = binary_number.find("1")
    if index_of_one == -1:
        binary_number = sign + "0."
    else:
        binary_number = sign + binary_number[index_of_one:] + "."
    for i in range(numsize - len(binary_number) - 1):
        float_part *= 2
        binary_number += int(int(float_part) != 0)
        float_part = float_part - float(int(float_part))
    return binary_number


def is_equal(first, second) -> bool:
    if len(first) != len(second): return False
    for i in range(len(first)):
        if first[i] != second[i]:
            return False
    return True


def floating_point_summary(first_number, second_number) -> list[str, str, str]:
    first_bin = normalize_bin_float(first_number)
    second_bin = normalize_bin_float(second_number)
    first_bin, second_bin = normalize_exponent(first_bin, second_bin)
    return mantissa_sum(first_bin, second_bin)


def shift_mantissa(mantissa: str, shift_count: int) -> str:
    if shift_count == 0:
        return mantissa
    return "0" * shift_count + mantissa[:-shift_count]


def make_exponents_equal(greater, lesser, shift_count):
    while not is_equal(greater[1], lesser[1]):
        lesser[1] = binary_sum([0] + list(lesser[1]),
                               [0] + [0, 0, 0, 0, 0, 0, 0, 1])
        shift_count += 1
    lesser[2] = shift_mantissa(lesser[2], shift_count)
    return greater, lesser


def normalize_exponent(bin_float_1, bin_float_2):
    shift_count: int = 0
    if get_max_from_binary(list(bin_float_1[1]), list(bin_float_2[1]), signed=True) == bin_float_1[1]:
        # shift_count = int("".join(str(x) for x in exponent_diff[1:]), 2)
        bin_float_1, bin_float_2 = make_exponents_equal(bin_float_2, bin_float_1, shift_count)
        return bin_float_1, bin_float_2

    bin_float_2, bin_float_1 = make_exponents_equal(bin_float_2, bin_float_1, shift_count)
    return bin_float_1, bin_float_2


while True:
    match int(input(
        'Выберите оперaцию: \n1 - Сумма\n2 - Разность\n3 - Умножение\n4 - Деление\n5 - Сложение с плавающей точкой\n')):
        case 1:
            x1 = int(input('Enter x_1: '))
            x2 = int(input('Enter x_2: '))
            result = from_additional_to_direct(summ(decimal_to_binary(x1), decimal_to_binary(x2)))
            print(f'{x1} + {x2} = ', result, f'= {convert_to_decimal(result)}')
            result = from_additional_to_direct(summ(decimal_to_binary(x1), decimal_to_binary(-x2)))
            print(f'{x1} + (-{x2}) = ', result, f'= {convert_to_decimal(result)}')
            result = from_additional_to_direct(summ(decimal_to_binary(-x1), decimal_to_binary(x2)))
            print(f'-{x1} + {x2} = ', result, f'= {convert_to_decimal(result)}')
            result = from_additional_to_direct(summ(decimal_to_binary(-x1), decimal_to_binary(-x2)))
            print(f'-{x1} + (-{x2}) = ', result, f'= {convert_to_decimal(result)}')
        case 2:
            x1 = int(input('Enter x_1: '))
            x2 = int(input('Enter x_2: '))
            result = from_additional_to_direct(subtraction(decimal_to_binary(x1), decimal_to_binary(x2)))
            print(f'{x1} - {x2} = ', result, f'= {convert_to_decimal(result)}')
            result = from_additional_to_direct(subtraction(decimal_to_binary(x1), decimal_to_binary(-x2)))
            print(f'{x1} - (-{x2}) = ', result, f'= {convert_to_decimal(result)}')
            result = from_additional_to_direct(subtraction(decimal_to_binary(-x1), decimal_to_binary(x2)))
            print(f'-{x1} - {x2} = ', result, f'= {convert_to_decimal(result)}')
            result = from_additional_to_direct(subtraction(decimal_to_binary(-x1), decimal_to_binary(-x2)))
            print(f'-{x1} - (-{x2}) = ', result, f'= {convert_to_decimal(result)}')
        case 3:
            x1 = int(input('Enter x_1: '))
            x2 = int(input('Enter x_2: '))
            result = (mul(decimal_to_binary(x1), decimal_to_binary(x2)))
            print(f'{x1} * {x2} = ', result, f'= {convert_to_decimal(result)}')
            result = (mul(decimal_to_binary(x1), decimal_to_binary(-x2)))
            print(f'{x1} * (-{x2}) = ', result, f'= {convert_to_decimal(result)}')
            result = (mul(decimal_to_binary(-x1), decimal_to_binary(-x2)))
            print(f'-{x1} * (-{x2}) = ', result, f'= {convert_to_decimal(result)}')
        case 4:
            x1 = int(input('Enter x_1: '))
            x2 = int(input('Enter x_2: '))
            result = (binary_numbers_division(decimal_to_binary(x1), decimal_to_binary(x2)))
            print(f'{x1} // {x2} = ', result, f'= {convert_to_decimal(result)}')
            result = (binary_numbers_division(decimal_to_binary(x1), decimal_to_binary(-x2)))
            print(f'{x1} // (-{x2}) = ', result, f'= {convert_to_decimal(result)}')
            result = (binary_numbers_division(decimal_to_binary(-x1), decimal_to_binary(x2)))
            print(f'-{x1} // (-{x2}) = ', result, f'= {convert_to_decimal(result)}')
        case 5:
            x1 = float(input('Enter x_1: '))
            x2 = float(input('Enter x_2: '))
            result = floating_point_summary(x1, x2)
            print(floating_point_to_decimal(result))
