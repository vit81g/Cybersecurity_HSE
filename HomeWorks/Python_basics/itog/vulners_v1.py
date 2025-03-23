import os # Импорт модуля os для работы с ОС
import json # для работы с данными в формате JSON
import requests # для выполнения HTTP-запросов
from dotenv import load_dotenv # переменные окружения из файла .env.
from typing import List, Dict, Any, Optional #  для аннотации типов переменных и функций, по фен-шую

# загружаем переменные окружения из файла .env. Исключаем отображение ключа в коде
load_dotenv()

# Константы
VULNERS_API: str = os.getenv("VULNERS_API", "") # получаем API-ключ Vulners
VULNERS_API_URL: str = "https://vulners.com/api/v3/search/lucene/" # URL API Vulners
HEADERS: Dict[str, str] = {"X-Vulners-API-Key": VULNERS_API} # заголовки запроса с API
OUTPUT_FILE: str = "vulnerability_report.txt" # файл для текстового отчета
JSON_REPORT_FILE: str = "vulnerability_report.json" # файл для JSON-отчета

# список ПО для анализа. Можно попробовать брать из файла, удобнее будет
SOFTWARE_LIST: List[Dict[str, str]] = [
    {"Program": "LibreOffice", "Version": "6.0.7"},
    {"Program": "7zip", "Version": "18.05"},
    {"Program": "Adobe Reader", "Version": "2018.011.20035"},
    {"Program": "nginx", "Version": "1.14.0"},
    {"Program": "Apache HTTP Server", "Version": "2.4.29"},
    {"Program": "DjVu Reader", "Version": "2.0.0.27"},
    {"Program": "Wireshark", "Version": "2.6.1"},
    {"Program": "Notepad++", "Version": "7.5.6"},
    {"Program": "Google Chrome", "Version": "68.0.3440.106"},
    {"Program": "Mozilla Firefox", "Version": "61.0.1"}
]


def get_vulnerabilities(program: str, version: str) -> Optional[List[Dict[str, Any]]]:
    """
    Функция отправляет запрос к Vulners API для получения данных об уязвимостях указанной программы и версии.
    :param program: строка с названием программы
    :param version: строка с версией программы
    :return: список словарей с данными об уязвимостях или None, если запрос не удался.
    """
    # строка запроса, соединяя имя программы и версию пробелом
    query: str = f"{program} {version}"

    # параметры запроса к API
    params: Dict[str, Any] = {
        "query": query,  # строка поиска
        "size": 100,  # ограничиваем количество возвращаемых результатов
        "sort": "cvss.score"  # сортируем по значению CVSS
    }

    # Проверка работы - вывод в консоль информацию.
    print(f"Запрос к Vulners API: {query}")

    # GET-запрос к API с указанным URL
    try:
        response = requests.get(VULNERS_API_URL, headers=HEADERS, params=params, timeout=10)

        # Проверка (код ответа 200) и исключение.
        response.raise_for_status()

        # преобразуем ответ API из JSON в словарь
        data: Dict[str, Any] = response.json()

        # извлечение результатов поиска из структуры ответа: data -> search (может быть пустым).
        search_results: List[Dict[str, Any]] = data.get("data", {}).get("search", [])

        # проверка - вывод в консоль количество полученных результатов
        print(f"Получено {len(search_results)} результатов для {program} {version}")

        # список результатов.
        return search_results

    # обработка ошибок.
    except requests.RequestException as e:
        # вывод сообщение об ошибке с прогой
        print(f"Ошибка при запросе к Vulners API для {program} {version}: {e}")
        # None, чтобы обозначить сбой в получении данных.
        return None


def analyze_vulnerabilities(vuln_data: Optional[List[Dict[str, Any]]]) -> Dict[str, List[str]]:
    """
    Функция анализирует данные об уязвимостях из API и извлекает CVE и информацию об эксплойтах.
    :param vuln_data: список словарей с данными об уязвимостях или None, если данных нет.
    :return: словарь с двумя ключами: "cve" и "exploits".
    """
    # заполняем пустые списки для хранения всех CVE и CVE с доступными эксплойтами.
    cve_list: List[str] = []  # список всех найденных CVE
    exploits_available: List[str] = []  # список CVE, для которых есть эксплойты

    # проверяем, есть ли данные для анализа. Если нет (None или пустой список), возвращаем пустой результат
    if not vuln_data:
        # выводим в консоль - отсутствие данных
        print("Нет данных для анализа уязвимостей")
        # возвращаем словарь с пустыми списками для CVE и эксплойтов
        return {"cve": [], "exploits": []}

    # цикл проходит по каждому элементу в списке уязвимостей
    for vuln in vuln_data:
        # извлекаем словарь "_source" из текущего элемента
        source: Dict[str, Any] = vuln.get("_source", {})

        # извлекаем список "cvelist" из словаря "_source"
        cve_entries: List[str] = source.get("cvelist", [])

        # цикл проходит по каждому CVE в списке
        for cve in cve_entries:
            # проверка если CVE начинается с "CVE-"
            if cve.startswith("CVE-") and cve not in cve_list:
                # добавляем CVE в список
                cve_list.append(cve)

                # проверяем, есть ли эксплойт для этого CVE:
                # - "is_exploit" = True или слово "exploit" есть в поле "type"
                if source.get("is_exploit", False) or "exploit" in source.get("type", "").lower():
                    # проверка если - CVE не в списке эксплойтов
                    exploits_available.append(cve)

    # Контроль - выводим в консоль количество найденных CVE и CVE с эксплойтами
    print(f"Найдено CVE: {len(cve_list)}, с эксплойтами: {len(exploits_available)}")

    # возвращаем словарь с списками CVE и эксплойтов
    return {"cve": cve_list, "exploits": exploits_available}


# запуск скрипта
if __name__ == "__main__":
    # проверка если - файл .env существует
    if not VULNERS_API:
        # вывод сообщение об ошибке
        print("Ошибка: API-ключ Vulners не найден. Укажите его в .env файле как VULNERS_API.")
        # выход с кодом ошибки, чтобы программа завершилась
        exit(1)

    # список программ для анализа
    report_data: Dict[str, Dict[str, Any]] = {}

    # проходим по каждому элементу списка программ в кодировке UTF-8
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        # записываем заголовок
        output.write("Отчёт по уязвимостям программного обеспечения\n")
        # записываем разделитель (50 звезд)
        output.write("=" * 50 + "\n\n")

        # Цикл проходит по каждому словарю в SOFTWARE_LIST
        for software in SOFTWARE_LIST:
            # извлекаем название программы из словаря.
            program: str = software["Program"]
            # извлекаем версию программы из словаря.
            version: str = software["Version"]

            # Контроль - выводим в консоль название и версию программы
            print(f"\nАнализирую: {program} {version}")

            # получаем данные об уязвимостях для программы и версии
            vuln_data: Optional[List[Dict[str, Any]]] = get_vulnerabilities(program, version)

            # анализируем уязвимости
            analysis: Dict[str, List[str]] = analyze_vulnerabilities(vuln_data)

            # добавляем информацию о программе в словарь
            report_data[f"{program} {version}"] = {
                "vulnerable": bool(analysis["cve"]),  # True, если есть CVE, иначе False
                "cve_list": analysis["cve"],  # список всех CVE
                "exploits_available": analysis["exploits"]  # список CVE с эксплойтами
            }

            # записываем информацию о программе в текстовый файл.
            output.write(f"Программа: {program} {version}\n")

            # условие если - есть уязвимости
            if analysis["cve"]:
                # если уязвимости есть, записываем "Уязвима: Да".
                output.write(f"Уязвима: Да\n")
                # записываем список всех CVE, объединённый через запятую.
                output.write(f"Найденные CVE: {', '.join(analysis['cve'])}\n")

                # проверка если - есть эксплойты
                if analysis["exploits"]:
                    # если эксплойты есть, записываем их список.
                    output.write(f"Эксплойты доступны для: {', '.join(analysis['exploits'])}\n")
                else:
                    # если эксплойтов нет, записываем соответствующее сообщение.
                    output.write("Эксплойты: Нет\n")
            else:
                # иначе - если уязвимостей нет, записываем "Уязвима: Нет".
                output.write("Уязвима: Нет\n")

            # записываем разделитель
            output.write("-" * 50 + "\n\n")

    # открываем JSON-файл для записи данных в формате JSON с кодировкой UTF-8.
    with open(JSON_REPORT_FILE, "w", encoding="utf-8") as json_output:
        # записываем словарь report_data в JSON с отступами (4 пробела) и поддержкой не-ASCII символов (на просторах инета)
        json.dump(report_data, json_output, indent=4, ensure_ascii=False)

    # выводим в консоль сообщение о том, что отчеты успешно сохранены, с указанием имен файлов.
    print(f"Отчёты сохранены в {OUTPUT_FILE} и {JSON_REPORT_FILE}")