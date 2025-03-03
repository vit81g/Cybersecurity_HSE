import os
import json
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
VULNERS_API_KEY = os.getenv("VULNERS_API_KEY", "")  # API-ключ Vulners из .env

# Константы
VULNERS_API_URL = "https://vulners.com/api/v3/search/lucene/"  # URL API Vulners
HEADERS = {"X-Vulners-API-Key": VULNERS_API_KEY}  # Заголовки с API-ключом
OUTPUT_FILE = "vulnerability_report.txt"  # Текстовый файл отчёта
JSON_REPORT_FILE = "vulnerability_report.json"  # JSON-файл отчёта

# Список программного обеспечения для анализа
SOFTWARE_LIST = [
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


# Функция для запроса уязвимостей через Vulners API
def get_vulnerabilities(program, version):
    """
    Запрашивает уязвимости для указанного ПО и версии через Vulners API.
    :param program: Название программы
    :param version: Версия программы
    :return: Список уязвимостей или None в случае ошибки
    """
    query = f"{program} {version}"  # Формируем запрос
    params = {
        "query": query,
        "size": 100,  # Максимальное количество результатов
        "sort": "cvss.score"  # Сортировка по CVSS-оценке
    }
    print(f"Запрос к Vulners API: {query}")
    try:
        response = requests.get(VULNERS_API_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        search_results = data.get("data", {}).get("search", [])
        print(f"Получено {len(search_results)} результатов для {program} {version}")
        return search_results
    except requests.RequestException as e:
        print(f"Ошибка при запросе к Vulners API для {program} {version}: {e}")
        return None


# Функция для анализа уязвимостей и извлечения CVE и эксплойтов
def analyze_vulnerabilities(vuln_data):
    """
    Анализирует данные уязвимостей и возвращает список CVE и информацию об эксплойтах.
    :param vuln_data: Данные от Vulners API
    :return: Словарь с CVE и эксплойтами
    """
    cve_list = []
    exploits_available = []

    if not vuln_data:
        print("Нет данных для анализа уязвимостей")
        return {"cve": [], "exploits": []}

    for vuln in vuln_data:
        # Извлекаем CVE из поля _source.cvelist
        source = vuln.get("_source", {})
        cve_entries = source.get("cvelist", [])

        # Добавляем все CVE из cvelist
        for cve in cve_entries:
            if cve.startswith("CVE-") and cve not in cve_list:
                cve_list.append(cve)
                # Проверяем наличие эксплойтов
                if source.get("is_exploit", False) or "exploit" in source.get("type", "").lower():
                    exploits_available.append(cve)

    print(f"Найдено CVE: {len(cve_list)}, с эксплойтами: {len(exploits_available)}")
    if not cve_list and vuln_data:
        print("Пример записи без CVE в cvelist:", json.dumps(vuln_data[0], indent=4))

    return {
        "cve": cve_list,
        "exploits": exploits_available
    }


# Основная логика
if __name__ == "__main__":
    if not VULNERS_API_KEY:
        print("Ошибка: API-ключ Vulners не найден. Укажите его в .env файле как VULNERS_API_KEY.")
        exit(1)

    report_data = {}  # Структура для JSON-отчёта

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        output.write("Отчёт по уязвимостям программного обеспечения\n")
        output.write("=" * 50 + "\n\n")

        for software in SOFTWARE_LIST:
            program = software["Program"]
            version = software["Version"]
            print(f"\nАнализирую: {program} {version}")

            # Запрос уязвимостей
            vuln_data = get_vulnerabilities(program, version)
            analysis = analyze_vulnerabilities(vuln_data)

            # Заполняем отчёт
            report_data[f"{program} {version}"] = {
                "vulnerable": bool(analysis["cve"]),
                "cve_list": analysis["cve"],
                "exploits_available": analysis["exploits"]
            }

            # Вывод в текстовый файл
            output.write(f"Программа: {program} {version}\n")
            if analysis["cve"]:
                output.write("Уязвимости обнаружены:\n")
                output.write("Список CVE:\n")
                for cve in analysis["cve"]:
                    output.write(f"  - {cve}\n")
                if analysis["exploits"]:
                    output.write("CVE с общедоступными эксплойтами:\n")
                    for exploit_cve in analysis["exploits"]:
                        output.write(f"  - {exploit_cve}\n")
                else:
                    output.write("Общедоступных эксплойтов не найдено.\n")
            else:
                output.write("Уязвимости не обнаружены.\n")
            output.write("-" * 50 + "\n\n")

    # Сохранение отчёта в JSON
    with open(JSON_REPORT_FILE, "w", encoding="utf-8") as json_output:
        json.dump(report_data, json_output, indent=4, ensure_ascii=False)

    print(f"Отчёты сохранены в {OUTPUT_FILE} и {JSON_REPORT_FILE}")