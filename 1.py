import random
import statistics
import matplotlib.pyplot as plt

# Функция для генерации последовательности случайных чисел и расчета их характеристик
def generate_and_analyze_sequences(sequence_lengths):
    results = {}
    for N in sequence_lengths:
        sequence = [random.random() for _ in range(N)]
        M = statistics.mean(sequence)
        D = statistics.variance(sequence)
        sigma = statistics.stdev(sequence)

        results[N] = {'sequence': sequence, 'M': M, 'D': D, 'sigma': sigma}
    return results

# Функция для проверки частотности генератора
def test_frequency(sequences, intervals):
    for N, data in sequences.items():
        plt.hist(data['sequence'], bins=intervals, edgecolor='black')
        plt.title(f'Frequency distribution for N={N}')
        plt.show()

# Функция для проверки равномерности генератора
def test_uniformity(sequences, theoretical_mean):
    differences = []
    for N, data in sequences.items():
        mean_diff = abs(theoretical_mean - data['M'])
        differences.append(mean_diff)
    
    plt.plot(sequences.keys(), differences, marker='o')
    plt.title('Difference between theoretical and empirical means')
    plt.xlabel('Sequence length N')
    plt.ylabel('Difference (M - Mi)')
    plt.show()

# Главная функция для запуска анализа
def main():
    sequence_lengths = [100, 1000, 10000]
    sequences = generate_and_analyze_sequences(sequence_lengths)
    for N in sequence_lengths:
        print(f'N={N}: M={sequences[N]["M"]}, D={sequences[N]["D"]}, sigma={sequences[N]["sigma"]}')

    # Исходя из теоретического равномерного распределения
    theoretical_mean = 0.5

    test_frequency(sequences, intervals=10)
    test_uniformity(sequences, theoretical_mean)

if __name__ == "__main__":
    main()
