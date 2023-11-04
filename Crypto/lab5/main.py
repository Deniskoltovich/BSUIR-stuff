import json

from Crypto.Util.number import getStrongPrime


class RSA:
    OPEN_EXPONENT = 65537

    @staticmethod
    def egcd(num_1, num_2):
        # Extended Euclidean Algorithm
        s = 0
        old_s = 1
        t = 1
        old_t = 0
        r = num_2
        old_r = num_1
        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
        return old_r, old_s, old_t

    def modular_inversion(self, num_1, num_2):
        # gcd(num1, num2) = num1 * d + num2 * y
        gcd, d, y = self.egcd(num_1, num_2)
        if d <= 0:
            d += num_2
        return d

    def generate_key(self):
        p = getStrongPrime(1024)
        q = getStrongPrime(1024)
        n = p * q
        fi = (p - 1) * (q - 1)
        d = self.modular_inversion(self.OPEN_EXPONENT, fi)
        return {
            'pubic_key': {
                'open_e': self.OPEN_EXPONENT,
                'n': n
            },
            'private_key': {
                'd': d,
                'n': n
            }
        }

    def create_dig_sign(self, message, private_key):
        r = list(map(
            lambda x: (ord(x) ** private_key['d']) % private_key['n'],
            message)
        )
        return {'message': message, 'sign': r}

    def check_dig_sign(self, s: dict, pub_key):
        mes =  ''.join(list(map(
            lambda x: chr(
                pow(x, pub_key['open_e'], pub_key['n']),
                ), s['sign']
            )))
        return s['message'] == mes

    @staticmethod
    def encrypt_message(message: str, pub_key: dict) -> list[int]:
        # c = E(m) = {m} ^ {e}  mod n
        return list(map(
            lambda x: (ord(x) ** pub_key['open_e']) % pub_key['n'],
            message)
        )

    @staticmethod
    def decrypt_message(message: list[int], private_key: dict):
        # m = D(c) = {c} ^ {d}  mod n

        return ''.join(list(map(
            lambda x: chr(
                pow(x, private_key['d'], private_key['n']),
                ), message
            )))



if __name__ == '__main__':
    rsa = RSA()
    keys = rsa.generate_key()
    with open('private_key.txt', 'w') as file:
        json.dump(keys['private_key'], file)
    with open('public_key.txt', 'w') as file:
        json.dump(keys['pubic_key'], file)

    message = input('Message: ')

    encypted = rsa.encrypt_message(message, keys['pubic_key'])
    decrypted = rsa.decrypt_message(encypted, keys['private_key'])

    with open('encrypted_message.txt', 'w') as file:
        json.dump(encypted, file)

    with open('decrypted_message.txt', 'w') as file:
        file.write(decrypted)
    print('here')

    d = rsa.create_dig_sign(message, keys['private_key'])

    print(rsa.check_dig_sign(d, keys['pubic_key']))


