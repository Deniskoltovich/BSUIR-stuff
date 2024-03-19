from lab1.pipe import Pipe
import matplotlib.pyplot as plt


def plot_acceleration_of_r(num_of_pairs):
    num_size = 4
    pair = [0 for _ in range(num_size)]
    accelerations = []
    for i in range(1, num_of_pairs):
        pairs = list([pair, pair] for _ in range(i))
        pipe = Pipe(*pairs, num_size=num_size)
        while not pipe.is_done:
            pipe.next_step()

        t1 = num_size * i
        tn = pipe.steps_to_complete
        accelerations.append(t1 / tn)

    plt.plot(range(1, num_of_pairs), accelerations, marker='o', linestyle='-')
    plt.plot(range(1, num_of_pairs), [1 for _ in range(1, num_of_pairs)], marker='o', linestyle='-')

    plt.xlabel('r')
    plt.ylabel('K_y(n,r)')
    plt.title('График зависимости коэффициента ускорения Ky(n, r) от ранга задачи r')

    # Отображение сетки
    plt.grid(True)

    # Отображение графика
    plt.show()



def plot_acceleration_of_n(num_of_pairs):

    num_size = 4
    pair = [0 for _ in range(num_size)]
    accelerations = []
    for i in range(1, num_of_pairs):
        pairs = list([pair, pair] for _ in range(i))
        pipe = Pipe(*pairs, num_size=num_size)
        while not pipe.is_done:
            pipe.next_step()

        t1 = num_size * i
        tn = pipe.steps_to_complete
        accelerations.append(t1 / tn)

    plt.plot((1, *[4 for _ in range(num_of_pairs - 2)]), accelerations, marker='o',linestyle='none')

    plt.xlabel('количествo процессорных элементов n')
    plt.ylabel('K_y(n,r)')
    plt.title('График зависимости коэффициента ускорения Ky(n, r) от количества\n процессорных элементов n')

    # Отображение сетки
    plt.grid(True)

    # Отображение графика
    plt.show()


if __name__ == '__main__':
    plot_acceleration_of_r(num_of_pairs=20)
    plot_acceleration_of_n(num_of_pairs=20)

