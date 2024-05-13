import numpy as np
import pandas as pd

# Вариант
TYPES = [1, 2, 3, 4]
P_i = [0.09, 0.68, 0.04, 0.19]
P_ij = {
    1: [0.52, 0.27, 0.09, 0.07, 0.05],
    2: [0.34, 0.44, 0.07, 0.12, 0.03],
    3: [0.63, 0.11, 0.08, 0.17, 0.01],
    4: [0.51, 0.02, 0.23, 0.12, 0.12]
}
A, B = 22, 254
MEAN_TIME = 0.4
VARIANCE = 4.2
previous_timestamp = 0

def get_timestamp(mean=MEAN_TIME, variance=VARIANCE):
    global previous_timestamp
    interval = np.random.normal(mean, np.sqrt(variance))
    timestamp = previous_timestamp + max(0, interval)  # Время должно быть положительным
    previous_timestamp = timestamp
    return timestamp

def generate_messages(n=100):
    messages = []
    for _ in range(n):
        # Тип сообщения
        message_type = np.random.choice(TYPES, p=P_i)        
        # Адрес абонента
        recipient = np.random.choice(range(1, 6), p=P_ij[message_type])        
        # Длина сообщения
        if message_type % 2 == 0:  # Для чётных - равномерное распределение
            length = np.random.randint(A, B+1)
        else:  # Для нечётных - нормальное распределение
            length = int(np.random.normal((A+B)//2, (B-A)/6))
            length = max(A, min(length, B))
        # Время поступления сообщения
        timestamp = get_timestamp()
        
        messages.append({
            "тип сообщения": message_type,
            "адрес абонента": recipient,
            "длина сообщения": length,
            "время поступления сообщения": timestamp
        })        
    return messages

# Генерация сообщений
messages = generate_messages()
df = pd.DataFrame(messages)
df.to_excel("result.xlsx", index=False)
print("Моделирование выполнено")

# Таблица 1
types_df = pd.DataFrame({
    'Тип': TYPES,
    'Теор. вероятность': P_i
}).set_index('Тип')
types_df['Практ. вероятность'] = df['тип сообщения'].value_counts(normalize=True).sort_index()
types_df['Кол-во'] = df['тип сообщения'].value_counts().sort_index()
types_df['Средняя длина'] = df.groupby('тип сообщения')['длина сообщения'].mean()
types_df['Максимальная длина'] = df.groupby('тип сообщения')['длина сообщения'].max()
types_df['Частота'] = 1 / df.sort_values('время поступления сообщения').groupby('тип сообщения')['время поступления сообщения'].diff().groupby(df['тип сообщения']).mean()
with pd.ExcelWriter('tab1.xlsx', engine='xlsxwriter') as writer:
    types_df.to_excel(writer, sheet_name='Сравнение данных по типам')
# Таблица 2
recipient_probabilities = pd.crosstab(df['тип сообщения'], df['адрес абонента'], normalize='index')
theoretical_probs_df = pd.DataFrame(P_ij).transpose()
theoretical_probs_df.index.name = "тип сообщения"
theoretical_probs_df.columns = [f'Теор. вероятность для получателя {i + 1}' for i in range(len(theoretical_probs_df.columns))]
comparison_probs_df = recipient_probabilities.copy()
for col in theoretical_probs_df.columns:
    recipient_num = int(col.split()[-1])
    comparison_probs_df[f'Практ. вероятность для получателя {recipient_num}'] = recipient_probabilities[recipient_num]
    comparison_probs_df[col] = theoretical_probs_df[col]
columns_order = [f'{desc} {num}' for num in range(1, 6) for desc in ['Практ. вероятность для получателя', 'Теор. вероятность для получателя']]
comparison_probs_df = comparison_probs_df[columns_order]
comparison_probs_df.to_excel('tab2.xlsx')
comparison_probs_df
# Таблица 3
practical_counts = df['адрес абонента'].value_counts().sort_index()
total_time = df['время поступления сообщения'].max() - df['время поступления сообщения'].min()
practical_frequency = practical_counts / total_time
total_messages = len(df)
theoretical_counts = {recipient: sum([P_ij[type_][recipient - 1] * P_i[type_-1] * total_messages for type_ in TYPES]) for recipient in range(1, 6)}
theoretical_frequency = {recipient: theoretical_counts[recipient] / total_time for recipient in range(1, 6)}
comparison_df = pd.DataFrame({
    'Практическое количество': practical_counts,
    'Теоретическое количество': [theoretical_counts[i] for i in range(1, 6)],
    'Практическая частота': practical_frequency,
    'Теоретическая частота': [theoretical_frequency[i] for i in range(1, 6)],
}).transpose()
comparison_df.to_excel('tab3.xlsx')
comparison_df
# Таблица 4
stream_stats_df = pd.DataFrame(index=['Сообщение', 'Получатель', 'Длина', 'Время'])
stream_stats_df['Мат ожидание'] = [
    df['тип сообщения'].mean(), 
    df['адрес абонента'].mean(), 
    df['длина сообщения'].mean(), 
    df['время поступления сообщения'].mean()
]
stream_stats_df['Дисперсия'] = [
    df['тип сообщения'].var(), 
    df['адрес абонента'].var(), 
    df['длина сообщения'].var(), 
    df['время поступления сообщения'].var()
]
stream_stats_df['Ср кв отклонение'] = [
    df['тип сообщения'].std(), 
    df['адрес абонента'].std(), 
    df['длина сообщения'].std(), 
    df['время поступления сообщения'].std()
]

stream_stats_df.to_excel('tab4.xlsx')
stream_stats_df

average_time = df['время поступления сообщения'].mean()

intensity = 1 / average_time
print(f'Среднее время между поступлением сообщений: {average_time}')
print(f'Интенсивность: {intensity}')
