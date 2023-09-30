import random


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def create_vigenere_square(alphabet):
    square = {}
    for char in alphabet:
        shift_chars = []
        for shift in range(len(alphabet)):
            shifted_char = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            shift_chars.append(shifted_char)
        square[char] = ''.join(shift_chars)
    return square



# Генерация ключа для шифра Виженера
def generate_key(key_word, original_text):
    key_word_arr = list(key_word)
    key = ""
    index = 0
    while len(key) < len(original_text):
        if index == len(key_word):
            index = 0
        key += key_word_arr[index]
        index += 1
    return key

def encrypt_char(table: dict, origial_char: str, key_char: str):
    encrypted_char = table.get(key_char)[ALPHABET.index(origial_char)]
    return encrypted_char



# Шифр Виженера
def vigenere_encryption(key, original_text, alphabet):
    vigenere_square = create_vigenere_square(alphabet)
    key_word = generate_key(key, original_text)
    encryption_result = ''
    for ind, char in enumerate(original_text):
        encrypted = encrypt_char(vigenere_square, char, key_word[ind])
        encryption_result += encrypted
    return encryption_result

# Расшифровка Виженера
def vigenere_decryption(key, encrypted_text, alphabet):
    vigenere_square = create_vigenere_square(alphabet)

    key_word = generate_key(key, encrypted_text)
    decryption_result = ''
    for ind, char in enumerate(key_word):
        row = vigenere_square.get(char)
        decrypted_char = alphabet[row.index(encrypted_text[ind])]
        decryption_result += decrypted_char
    return decryption_result

# Генерация дополнительного ключа
def generate_extra_key(key_length, alphabet):
    password = ""
    for i in range(key_length):
        password += random.choice(alphabet)
    return password

# Взлом пароля
def hack_password(original_text, encrypted_text, alphabet, key_word):
    temp_key = generate_extra_key(len(key_word), alphabet)
    quantity_of_operations = 1
    while vigenere_decryption(temp_key, encrypted_text, alphabet) != original_text:
        temp_key = generate_extra_key(len(key_word), alphabet)
        quantity_of_operations += 1
    return quantity_of_operations


if __name__ == "__main__":
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    original_text = "PRIVET"
    key_word = "BYE"
    print('Original: ', original_text)
    vig_enc = vigenere_encryption(key_word, original_text, ALPHABET)
    print('Encrypted: ', vig_enc)
    vig_dec = vigenere_decryption(key_word, vig_enc, ALPHABET)
    print('Decrypted: ', vig_dec)
    
    print(f"Iterations to hack: {hack_password(original_text, vig_enc, ALPHABET, key_word)}")