import logging
import time
import psutil
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os

# ================= 1. НАЛАШТУВАННЯ ЛОГУВАННЯ =================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("experiment.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)


# ================= 2. АЛГОРИТМИ =================
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def timsort_wrapper(arr):
    return sorted(arr)


# ================= 3. ГЕНЕРАЦІЯ ДАНИХ ТА ПОМИЛОК =================
random.seed(42)


def generate_data(size, data_type="random"):
    if data_type == "corrupted":
        # Навмисна генерація помилки: масив містить рядок замість числа
        return [random.randint(0, 100) for _ in range(size - 1)] + ["ERROR_STRING"]
    elif data_type == "random":
        return [random.randint(0, 1_000_000) for _ in range(size)]
    elif data_type == "partially_sorted":
        arr = list(range(size))
        shuffle_len = int(size * 0.2)
        arr[-shuffle_len:] = [random.randint(0, size) for _ in range(shuffle_len)]
        return arr


# ================= 4. СИСТЕМА ЗБОРУ МЕТРИК =================
def measure_performance(sizes, data_types, algorithms, runs=30):
    results = []
    process = psutil.Process(os.getpid())

    logging.info("Початок серії експериментів...")

    for size in sizes:
        for dtype in data_types:
            for i in range(runs):
                test_arr = generate_data(size, dtype)

                for alg_name, alg_func in algorithms.items():
                    try:
                        arr_copy = test_arr.copy()

                        # Зняття метрик ДО
                        mem_before = process.memory_info().rss
                        psutil.cpu_percent(interval=None)  # Ініціалізація лічильника

                        start = time.perf_counter()
                        alg_func(arr_copy)
                        duration = time.perf_counter() - start

                        # Зняття метрик ПІСЛЯ
                        cpu_used = psutil.cpu_percent(interval=None)
                        mem_after = process.memory_info().rss
                        memory_used = max(0, (mem_after - mem_before) / (1024 * 1024))  # У Мегабайтах

                        logging.debug(f"Успіх: {alg_name} | Size={size} | Тип={dtype} | Час={duration:.4f}с")

                        results.append({
                            "Run": i + 1, "Algorithm": alg_name, "Size": size, "Type": dtype,
                            "Time_sec": duration, "Memory_MB": memory_used, "CPU_percent": cpu_used,
                            "Status": "Success"
                        })

                    except TypeError as e:
                        logging.error(f"Помилка типів у {alg_name} (Тип={dtype}): {str(e)}")
                        results.append({
                            "Run": i + 1, "Algorithm": alg_name, "Size": size, "Type": dtype,
                            "Time_sec": None, "Memory_MB": None, "CPU_percent": None,
                            "Status": "Failed"
                        })
                    except Exception as e:
                        logging.critical(f"Критична помилка: {str(e)}", exc_info=True)

    logging.info("Експерименти завершено.")
    return pd.DataFrame(results)


# ================= ПУСК ТА АНАЛІЗ =================
sizes = [10000, 50000, 100000]
data_types = ["random", "partially_sorted", "corrupted"]  # corrupted згенерує помилку в лог
algorithms = {'Quick Sort': quick_sort, 'Timsort': timsort_wrapper}

# 1. Збір даних
df = measure_performance(sizes, data_types, algorithms, runs=30)

# Збереження
df.to_csv("performance_metrics.csv", index=False)
logging.info("Дані збережено у performance_metrics.csv")

# Відфільтруємо лише успішні запуски для статистики та графіків
df_success = df[df['Status'] == 'Success'].copy()

# ================= 5. ВІЗУАЛІЗАЦІЯ (4 ГРАФІКИ) =================
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Аналіз метрик продуктивності алгоритмів сортування', fontsize=16)

# Графік 1: Line plot + error bars (Час від розміру)
sns.lineplot(ax=axes[0, 0], data=df_success, x='Size', y='Time_sec', hue='Algorithm', err_style='band', marker='o')
axes[0, 0].set_title('1. Залежність часу від обсягу даних')
axes[0, 0].set_ylabel('Час (секунди)')

# Графік 2: Box plot (Розподіл часу для масиву 100k)
df_100k = df_success[df_success['Size'] == 100000]
sns.boxplot(ax=axes[0, 1], data=df_100k, x='Type', y='Time_sec', hue='Algorithm')
axes[0, 1].set_title('2. Розподіл часу виконання (Розмір: 100 000)')
axes[0, 1].set_ylabel('Час (секунди)')

# Графік 3: Bar plot (Використання пам'яті)
sns.barplot(ax=axes[1, 0], data=df_100k, x='Algorithm', y='Memory_MB', estimator='mean', errorbar='sd', capsize=.1)
axes[1, 0].set_title('3. Середнє споживання оперативної пам\'яті (MB)')

# Графік 4: Гістограма (Розподіл навантаження на CPU)
sns.histplot(ax=axes[1, 1], data=df_100k, x='CPU_percent', hue='Algorithm', kde=True, bins=15)
axes[1, 1].set_title('4. Розподіл навантаження на CPU (%)')

plt.tight_layout()
plt.savefig("performance_plots.png", dpi=300)
logging.info("Графіки збережено у performance_plots.png")
print("Усі розрахунки та візуалізації успішно завершено! Перевірте файли у папці.")