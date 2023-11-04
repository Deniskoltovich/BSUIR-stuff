class SharedSecretGenerator:
    PRIMARY_NUMBER = 7759

    def is_primitive_element(self, primitive, primary):
        # набор остатков степеней primitive, вычисленных по модулю primary
        pow_mod_remainders = set()
        for i in range(1, primary):
            remainder = self.modulus_pow(primitive, i, primary)
            if remainder in pow_mod_remainders:
                # каждый остаток является уникальным
                return False
            pow_mod_remainders.add(remainder)
        return True

    @staticmethod
    def modulus_pow(base, exponent, mod=1):
        result = 1
        base = base % mod

        while exponent > 0:
            if exponent % 2:
                result = (result * base) % mod
            base = (base * base) % mod
            exponent //= 2
        return result

    def find_primitive(self, primary: int):
        for primitive in range(2, primary):
            if self.is_primitive_element(primitive, primary):
                return primitive
        return None

    def generate_shared_secret(self, primary, primitive, alice_key, bob_key):
        alice_open = self.modulus_pow(primitive, alice_key, primary)
        bob_open = self.modulus_pow(primitive, bob_key, primary)
        shared_secret = self.modulus_pow(alice_open, bob_key, primary)
        if shared_secret != self.modulus_pow(bob_open, alice_key, primary): raise RuntimeError('Shared secrets are not eq')
        return shared_secret


if __name__ == '__main__':
    shared_sec_gen = SharedSecretGenerator()
    primitive_element = shared_sec_gen.find_primitive(shared_sec_gen.PRIMARY_NUMBER)
    print(f'Примитивный элемент для {shared_sec_gen.PRIMARY_NUMBER} -- {primitive_element}')
    alice_key = int(input('Ключ для Алисы: '))
    bob_key = int(input('Ключ для Боба: '))

    shared_secret = shared_sec_gen.generate_shared_secret(shared_sec_gen.PRIMARY_NUMBER,
                                                                 primitive_element, alice_key, bob_key)
    print(f'Общий секрет: {shared_secret}')