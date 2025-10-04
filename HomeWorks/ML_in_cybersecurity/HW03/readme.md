# Домашнее задание: Практическая работа 3

**Дисциплина:** Применение ML в кибербезопасности  
**Тема:** Машинное обучение в контексте кибербезопасности  
**Имя преподавателя:** Юрий Иванов  
**Цель задания:** Научиться методологии анализа и решения задачи ML  
**Инструменты:** Google, Medium.com, arXiv.org, GitHub  

**Важно:** Это обзорное аналитическое исследование проводится перед практическим решением задачи ML. Данные актуальны на октябрь 2025 года.

## Повтор материалов предыдущих лекций и вебинаров (Этап 1)

На основе предоставленных материалов лекций Юрия Иванова:  
- Основы статистики в ML включают применение распределений, корреляций и визуализации для анализа данных, что критично для выбора признаков в задачах обнаружения malware.  
- Сбор и обработка данных подразумевают очистку от шумов и нормализацию, применимо к PE-файлам для удаления аномалий в заголовках.  
- В контексте кибербезопасности ML используется для обнаружения аномалий в файлах, с акцентом на статический и динамический анализ.  

## Погружение в предметную область

### Сравнение методов обнаружения вирусов
- **Статический анализ:** Анализирует PE-файл без выполнения (заголовки, секции, импорты). Преимущества: быстрый, безопасный, низкие ресурсы; недостатки: не выявляет полиморфный или обфусцированный malware. Подтверждено в статье "Static Malware Detection and Classification Using Machine Learning" (2025), где точность достигает 98% на статических признаках, но снижается при обфускации. Источник: https://www.mdpi.com/2673-4591/107/1/76 .  
- **Динамический анализ:** Запускает файл в песочнице (sandbox), наблюдает поведение (API-вызовы, сетевые запросы). Преимущества: выявляет runtime-аномалии, эффективен против zero-day угроз; недостатки: ресурсоёмкий, риск прорыва из sandbox, медленный. Подтверждено в "Binary and multiclass malware classification of windows portable ..." (2025), где динамические модели показывают F1-score 0.97, но требуют до 10x больше времени. Источник: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1539519/full .  

Выбранный метод: Статический анализ, так как он подходит для начального скрининга в реальном времени без рисков выполнения. Обоснование: В "Machine Learning-Based Static Analysis for Malware Detection" (2025) статический подход рекомендуется для масштабируемых систем. Источник: https://www.ijfmr.com/research-paper.php?id=43163 .  

### Что такое вредоносный файл
Вредоносный PE-файл отличается от безопасного по признакам: высокая энтропия секций (указывает на обфускацию), подозрительные импорты (e.g., kernel32.dll для инъекций кода), аномальный размер заголовков, необычные API-вызовы. Подтверждено в "Machine Learning for Detecting Malware in PE Files" (2024, но актуально для 2025), где эти признаки используются для классификации с accuracy 96%. Источник: https://ieeexplore.ieee.org/document/10460035/ .  

## Этапы выполнения задания

### Этап 2: Анализ существующих подходов (google.com, medium.com, arxiv.org)
Найдено 5 подходов (3-5 предложений на каждый, на основе поиска 2025 года):  

1. **Ensemble Approach (MalDitectist):** Использует ансамбль ML и DL для статического анализа PE-файлов. Модели: Random Forest + CNN. Особенности: Высокая устойчивость к новым угрозам, F1-score 0.98; подходит для zero-day malware. Преимущества: Снижает false positives; недостатки: Требует больших данных. Источник: https://www.researchgate.net/publication/379108984_Machine_Learning_for_Detecting_Malware_in_PE_Files .  
2. **Static ML-Based Detection:** Статический анализ с ML на заголовках и импортах. Модели: SVM, Decision Trees. Особенности: Точность 97%, быстрое inference; использует feature engineering. Преимущества: Масштабируемость; недостатки: Уязвим к обфускации. Источник: https://www.ijfmr.com/research-paper.php?id=43163 .  
3. **Static Malware Classification:** Классификация с ML на датасетах типа EMBER. Модели: Gradient Boosting. Особенности: Accuracy 98.5%, фокус на интерпретируемости. Преимущества: Эффективен для больших объёмов; недостатки: Зависит от качества данных. Источник: https://www.mdpi.com/2673-4591/107/1/76 .  
4. **EMBER2024 Update:** Улучшенный датасет с ML для evasive malware. Модели: LightGBM. Особенности: Обучение на 1M+ сэмплах, detection rate 99%. Преимущества: Адаптация к эволюционирующим угрозам; недостатки: Высокие вычисления. Источник: https://www.crowdstrike.com/en-us/blog/ember-2024-advancing-cybersecurity-ml-training-on-evasive-malware/ .  
5. **Multi-Model Framework:** Гибридный подход для PE и PDF. Модели: XGBoost + Neural Nets. Особенности: Feature selection для detection 97%. Преимущества: Универсальность; недостатки: Сложность интеграции. Источник: https://norma.ncirl.ie/8065/ .  

### Этап 3: Анализ решений на github.com
Топ-5 репозиториев (по stars, описание 3-5 предложений):  

1. **Machine-Learning-Malware-Detection (obarrera):** Анализирует PE-информацию exe-файлов для detection. Создание датасета, ML workflow. Stars: 40. Ключевые: Jupyter Notebook, модели не указаны явно. Источник: https://github.com/obarrera/Machine-Learning-Malware-Detection .  
2. **Malware-Detection-in-PE-files-using-Machine-Learning (DasariJayanth):** ML workflow для PE данных, создание prediction модели. Stars: 26. Ключевые: Jupyter Notebook. Источник: https://github.com/DasariJayanth/Malware-Detection-in-PE-files-using-Machine-Learning .  
3. **Malware-Detection-Using-Machine-Learning (emr4h):** Модуль для PE и ELF detection. Stars: 12. Ключевые: Python. Источник: https://github.com/emr4h/Malware-Detection-Using-Machine-Learning .  
4. **ML-malware-detection (umasolution):** Solution на features из PE файлов. Stars: 5. Ключевые: Python. Источник: https://github.com/umasolution/ML-malware-detection .  
5. **bitcamo (juburr):** AML tool для модификации PE для evasion. Stars: 4. Ключевые: Python. Источник: https://github.com/juburr/bitcamo .  

### Этап 4: Поиск наборов данных
3-5 датасетов (объём, авторы, признаки):  

1. **Microsoft Malware Classification Challenge (BIG 2015):** Автор: Microsoft. Объём: 20,000 train + 8,000 test. Признаки: Byte histogram, PE headers, strings, DLL. Описание: Дисассемблированные PE с labels по семьям malware; для ML/DL classification. Источник: https://www.kaggle.com/datasets/crowdflower/microsoft-malware-classification-challenge-big-2015 .  
2. **Ember 2017:** Автор: Ember. Объём: 900,000 train + 200,000 test (1.1M PE). Признаки: Byte histogram, imports, exports, entropy. Описание: Для static detection; features для ML training на unseen malware. Источник: https://www.kaggle.com/datasets/ember/ember-2017 .  
3. **Ember 2018:** Автор: Ember. Объём: 1,000,000 train + 200,000 test. Признаки: Byte histogram, imports, exports, entropy. Описание: Расширение 2017; для оценки ML моделей в dynamic threats. Источник: https://www.kaggle.com/datasets/ember/ember-2018 .  

### Этап 5: Анализ и обобщение подходов
3-5 основных подходов (1-2 абзаца):  

1. **Статический на features extraction:** Извлечение из PE headers (size, entropy, imports) с pefile.py. Модели: Random Forest/XGBoost. Подход эффективен для large-scale, accuracy >95%, но уязвим к mutations. Обоснование: В "Static Malware Detection" (2025) используется для classification с low overhead. Источник: https://www.mdpi.com/2673-4591/107/1/76 .  
2. **Динамический с API monitoring:** Анализ sequences в sandbox (Cuckoo). Модели: LSTM/CNN. Выявляет behavior threats, accuracy ~98%, но resource-intensive. Обоснование: В "Binary and multiclass" (2025) для polymorphic malware. Источник: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1539519/full .  
3. **Гибридный ensemble:** Комбинация static/dynamic. Модели: Ensemble (RF + DL). Улучшает robustness, accuracy 99%; complex deploy. Обоснование: В "MalDitectist" (2025) для evasion-resistant detection. Источник: https://www.researchgate.net/publication/379108984_Machine_Learning_for_Detecting_Malware_in_PE_Files .  

## Этап 6: Таблица результатов исследования

| Действие | Результат исследования |
|----------|-------------------------|
| Повтор материалов предыдущих лекций и вебинаров | Освежены знания по статистике, обработке данных и ML в cybersecurity (см. Этап 1 выше). |
| Анализ существующих подходов (google.com, medium.com, arxiv.org) | 5 подходов описаны в Этапе 2 с источниками. |
| Анализ решений на github.com | 5 репозиториев в Этапе 3 с links. |
| Поиск наборов данных | 3 датасета в Этапе 4 с details. |
| Анализ и обобщение подходов | 3 обобщённых подхода в Этапе 5. |

## Этап 7: Описание предлагаемого решения (План ML)

1. **Подход:** Статический анализ PE-файлов. Почему: Безопасный и быстрый для initial screening. Обоснование: Рекомендовано в "Machine Learning-Based Static Analysis" (2025). Источник: https://www.ijfmr.com/research-paper.php?id=43163 .  
2. **Данные:** Ember 2018 (1M+ samples). Сбор: Скачать с Kaggle. Обоснование: Large, labeled для training. Источник: https://www.kaggle.com/datasets/ember/ember-2018 .  
3. **Валидация/очистка:** Да, удалить duplicates, normalize (MinMaxScaler). Способ: Pandas в Python. Обоснование: Из лекции по обработке данных. Источник: "Тема 2 (Иванов).pdf", страница 2.  
4. **Признаки:** Headers, imports, entropy. Извлечение: pefile library. Обоснование: Стандарт для PE. Источник: https://ieeexplore.ieee.org/document/10460035/ .  
5. **Модели:** Random Forest baseline, XGBoost для улучшения. Обоснование: High accuracy на tabular data. Источник: https://www.mdpi.com/2673-4591/107/1/76 .  
6. **Ансамблирование:** Да, stacking (RF + CNN). Обоснование: Для robustness. Источник: https://www.researchgate.net/publication/379108984_Machine_Learning_for_Detecting_Malware_in_PE_Files .  
7. **Метрики:** F1-score, ROC-AUC. Почему: Баланс precision/recall в cybersecurity. Обоснование: В "Binary and multiclass" (2025). Источник: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1539519/full .  

