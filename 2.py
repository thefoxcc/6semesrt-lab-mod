import numpy as np
import matplotlib.pyplot as plt

# Параметры для распределения Бернулли
p = 0.3  # вероятность успеха
n = 100  # выборка из случайных велечин
max = 78  # максимальное значение, получаемое при успехе

# Генерация выборки
sample = np.random.binomial(max, p, n)

# Расчёт характеристик
M = np.mean(sample)  # математическое ожидание
D = np.var(sample)  # дисперсия
s = np.std(sample)  # среднеквадратичное отклонение

# Вывод результатов
print(f'Математическое ожидание: {M}')

print(f'Дисперсия: {D}')
print(f'Среднеквадратичное отклонение: {s}')
print(f'Генерация выборки Бернулли: {sample}')

# Построение гистограммы
plt.figure(figsize=(10, 5))
plt.hist(sample, bins=range(0, max+1), color='blue', edgecolor='black')
plt.title('Гистограмма распределения Бернулли')
plt.xlabel('Значения')
plt.ylabel('Частота')
plt.xticks(range(0, max+1, int(max/10)))
plt.grid(axis='y')

# Построение эмпирической функции распределения
sample_sorted = np.sort(sample)
F = np.arange(1, n+1) / n
plt.figure(figsize=(10, 5))
plt.step(sample_sorted, F, where='mid')
plt.title('Эмпирическая функция распределения')
plt.xlabel('Значения')
plt.ylabel('Вероятность')
plt.xticks(range(0, max+1, int(max/10)))
plt.yticks(np.linspace(0, 1, 11))
plt.grid(axis='y')

# Отображение графиков
plt.show()
