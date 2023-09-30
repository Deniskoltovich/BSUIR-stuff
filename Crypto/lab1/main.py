import itertools
import random
import string
import time

import matplotlib.pyplot as plt

NUM_ITERATIONS = 4


class PasswordGenerator:
    def __init__(self, len: int) -> None:
        self.len = len
       
        self.password = ''.join(random.choice(string.printable) for _ in range(len))

    def generate_combinations(self, length):
        prod = itertools.product(string.printable, repeat=length)
        return prod

    def generate_random_password(self, length: int) -> str:
        return ''.join(random.choice(string.printable) for _ in range(length))


    def brute_force_password_crack(self, password=None):
        actual  = password if password else self.password
        for combination in self.generate_combinations(len(actual)):
            if ''.join(combination) == actual: return None


    def calculate_average_password_crack_time(self, password=None):
        total_time = 0
        for _ in range(NUM_ITERATIONS):
            start_time = time.time()
            self.brute_force_password_crack(password)
            end_time = time.time()
            total_time += end_time - start_time
        return total_time / NUM_ITERATIONS
    
    def avg_time(self):
        num_iterations =  NUM_ITERATIONS # Количество попыток подбора пароля
        total_time = 0

        for _ in range(num_iterations):
            total_time += self.calculate_average_password_crack_time()
        average_time = total_time / num_iterations
        print(f"Среднее время подбора пароля: {average_time} секунд")
    

class Visualizer:
    def __init__(self, password: str) -> None:
        self.password = password


    def visualize_character_distribution(self):
        character_counts = {}
        for char in self.password:
            if char in character_counts:
                character_counts[char] += 1
            else:
                character_counts[char] = 1

        characters = list(character_counts.keys())
        counts = list(character_counts.values())

        plt.bar(characters, counts)
        plt.xlabel('Символы')
        plt.ylabel('Частота')
        plt.title('Частотное распределение символов')
        plt.show()

    def crack_time(self):
        password_generator = PasswordGenerator(len(self.password))
        password_lengths = range(1, 5)
        average_times = []

        for length in password_lengths:
            password = password_generator.generate_random_password(length)
            total_time = 0
            for i in range(NUM_ITERATIONS):
                total_time += password_generator.calculate_average_password_crack_time(password)
            average_time = total_time / NUM_ITERATIONS
            average_times.append(average_time)

        plt.plot(password_lengths, average_times)
        plt.xlabel('Длина пароля')
        plt.ylabel('Среднее время подбора (секунды)')
        plt.title('Зависимость времени подбора от длины пароля')
        plt.show()



if __name__ == "__main__":
    password_length = int(input("Введите длину пароля: "))


    password_generator = PasswordGenerator(password_length)
    print(fr'password: {password_generator.password}')
    visualizer = Visualizer(password_generator.password)


    visualizer.visualize_character_distribution()

    password_generator.avg_time()

    visualizer.crack_time()


