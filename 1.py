## 1 задача
import random
import numpy as np
import matplotlib.pyplot as plt

# Зададим N
N = [100, 1000, 10000]

# Получаем последовательности случайных чисел
sequences = {n: [random.random() for _ in range(n)] for n in N}

# Вычисляем характеристики для каждой последовательности
for n, sequence in sequences.items():
    M = np.mean(sequence)
    D = np.var(sequence)
    std_dev = np.sqrt(D)
    print(f"Для N={n}: Мат. ожидание (M)={M:.5f}, Дисперсия (D)={D:.5f}, Среднеквадр. отклонение={std_dev:.5f}")
    
    # Проверка частотности и равномерности
    plt.hist(sequence, bins='auto', color='blue', alpha=0.7, rwidth=0.85, density=True)
    plt.title(f'Гистограмма распределения для N={n}')
    plt.xlabel('Значение')
    plt.ylabel('Частота')
    plt.show()

    # Построение функций R(X)
    count, bins, ignored = plt.hist(sequence, bins=10, density=True, alpha=0.5, color='g')
    plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')
    plt.title(f'Функция R(X) для N={n}')
    plt.xlabel('Интервал')
    plt.ylabel('Вероятность P')
    plt.show()

# Расчет математического ожидания для последовательностей 1000 и переменной длины
fixed_length_sequences = [1000 * i for i in range(1, 11)]
variable_length_sequences = [i * 1000 for i in range(1, 11)]

fixed_means = [np.mean([random.random() for _ in range(1000)]) for _ in range(1, 11)]
variable_means = [np.mean([random.random() for _ in range(i * 1000)]) for i in range(1, 11)]

# Построение графика зависимости M-Mi от i
M_theoretical = 0.5
fixed_deviations = [M_theoretical - mean for mean in fixed_means]
variable_deviations = [M_theoretical - mean for mean in variable_means]

plt.plot(fixed_length_sequences, fixed_deviations, 'o-', label='Фиксированная длина')
plt.plot(variable_length_sequences, variable_deviations, 'o-', label='Переменная длина')
plt.axhline(0, color='red', linestyle='--', label='Теоретическое М')
plt.xlabel('Номер последовательности')
plt.ylabel('Разность (M-Mi)')
plt.title('Отклонение М от Мi')
plt.legend()
plt.grid(True)
plt.show()

# Определение вероятности P{|M-Mi|<s} для переменной длины
s = np.std([random.random() for _ in range(10000)])
probabilities = [abs(M_theoretical - mean) < s for mean in variable_means]
probability = sum(probabilities) / len(probabilities)
print(f"Вероятность того, что отклонение М от Мi меньше среднеквадратичного отклонения (s={s}): {probability:.5f}")


## 2 задача
# Определим функцию для метода серединных произведений
def middle_square_method(seed, n):
    numbers = []
    number = seed
    for _ in range(n):
        sq_number = str(number ** 2).zfill(8)  # Заполняем начало нулями до 8 цифр
        middle_digits = sq_number[len(sq_number)//4:-len(sq_number)//4]  # Извлекаем середину
        number = int(middle_digits)
        numbers.append(number / 10000)  # Нормируем число, чтобы оно было между 0 и 1
    return numbers
# Сид значение
seed = 1234
sequences = {n: middle_square_method(seed, n) for n in N}
