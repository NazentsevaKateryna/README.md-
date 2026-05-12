# 📊 Sorting Algorithms Performance Benchmark

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Completed-success.svg)]()

> Професійний інструмент для тестування, логування та статистичного аналізу продуктивності алгоритмів сортування.

Цей проєкт реалізований у межах курсу практичних робіт. Основна мета — порівняти ефективність алгоритмів **Quick Sort** та **Timsort** (вбудований `sorted()`) при обробці черг даних за допомогою системних метрик (CPU, RAM, Wall time).

---

## ✨ Основні можливості
- [cite_start]**⏱️ Метрики реального часу:** Вимірювання часу виконання за допомогою `time.perf_counter()`.
- [cite_start]**🧠 Моніторинг ресурсів:** Відстеження споживання оперативної пам'яті (RAM) та навантаження на процесор (CPU) через `psutil`.
- [cite_start]**🛡️ Обробка винятків:** Надійна система перехоплення помилок при роботі з "битими" даними.
- [cite_start]**📝 Логування:** Повна історія подій та збоїв записується у файл `experiment.log`.
- **📈 Візуалізація:** Побудова 4 типів графіків для глибокого аналізу (Line, Box, Bar, Hist).

## 🛠 Технології
- **Python 3.11+**
- **Pandas** — обробка результатів.
- **SciPy** — статистичний аналіз (U-тест Манна-Уїтні).
- **Matplotlib & Seaborn** — візуалізація даних.

## 🚀 Встановлення та запуск

1. Склонуйте репозиторій:
   ```bash
   git clone [https://github.com/NazentsevaKateryna/README.md-/edit/main/README.md.git](https://github.com/NazentsevaKateryna/README.md-/edit/main/README.md.git)
   2. Встановіть бібліотеки: 
   Bashpip install psutil pandas scipy matplotlib seaborn
3. Запустіть основний скрипт:Bashpython practice_4.py
📊 Результати бенчмаркінгу (N=100,000)
Ми порівняли алгоритми на частково відсортованих даних (імітація реальних черг):
Алгоритм,Середній час (мс),Медіана (мс),Стабільність (Std)
Quick Sort,~195.45,~193.91,6.75
Timsort,~4.86,~4.85,0.42

Структура проєкту
practice_4.py — головний код експерименту.

experiment.log — лог-файл із записами подій та помилок.

performance_metrics.csv — сирі дані для аналізу.

performance_plots.png — згенеровані графіки результатів.


