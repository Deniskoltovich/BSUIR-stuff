from lab1.pipe import Pipe
import matplotlib.pyplot as plt

PROCESSOR_ELEMENTS_QUANTITY = 4

def plot_efficiency_of_r(num_of_pairs):
    num_size = 4
    pair = [0 for _ in range(num_size)]
    efficiency = []
    for i in range(1, num_of_pairs):
        pairs = list([pair, pair] for _ in range(i))
        pipe = Pipe(*pairs, num_size=num_size)
        while not pipe.is_done:
            pipe.next_step()

        t1 = num_size * i
        tn = pipe.steps_to_complete
        efficiency.append((t1 / tn) / PROCESSOR_ELEMENTS_QUANTITY)

    plt.plot(range(1, num_of_pairs), efficiency, marker='o', linestyle='-')
    plt.plot(range(1, num_of_pairs), [1 for _ in range(1, num_of_pairs)], marker='o', linestyle='-')

    plt.xlabel('r')
    plt.ylabel('e')
    plt.title('График зависимости эффективности e от ранга задачи r')

    # Отображение сетки
    plt.grid(True)

    # Отображение графика
    plt.show()



def plot_efficiency_of_n(num_of_pairs):

    num_size = 4
    pair = [0 for _ in range(num_size)]
    efficiency = []
    for i in range(1, num_of_pairs):
        pairs = list([pair, pair] for _ in range(i))
        pipe = Pipe(*pairs, num_size=num_size)
        while not pipe.is_done:
            pipe.next_step()

        t1 = num_size * i
        tn = pipe.steps_to_complete
        efficiency.append((t1 / tn) / PROCESSOR_ELEMENTS_QUANTITY)

    plt.plot((1, *[4 for _ in range(num_of_pairs - 2)]), efficiency, marker='o',linestyle='none')

    plt.xlabel('количествo процессорных элементов n')
    plt.ylabel('e')
    plt.title('График зависимости эффективности e от количества\n процессорных элементов n')

    # Отображение сетки
    plt.grid(True)

    # Отображение графика
    plt.show()


if __name__ == '__main__':
    plot_efficiency_of_r(num_of_pairs=20)
    plot_efficiency_of_n(num_of_pairs=20)

