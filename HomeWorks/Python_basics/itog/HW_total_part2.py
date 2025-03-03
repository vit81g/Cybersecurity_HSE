import os  # для работы с файловой системой и переменными окружения
import json  # для работы с JSON-форматом данных
import requests  # HTTP-запросы к API
from dotenv import load_dotenv  # переменные из файла .env
from typing import List, Dict, Any, Optional  # для аннотации типов

# Загружаем переменные окружения из .env
load_dotenv()
VULNERS_API: str = os.getenv("VULNERS_API", "")  # API-ключ Vulners из .env

# Константы
VULNERS_API_URL: str = "https://vulners.com/api/v3/search/lucene/"  # URL API Vulners
HEADERS: Dict[str, str] = {"X-Vulners-API-Key": VULNERS_API}  # заголовки с API-ключом
OUTPUT_FILE: str = "vulnerability_report.txt"  # имя файла отчёта
JSON_REPORT_FILE: str = "vulnerability_report.json"  # имя JSON-файла отчёта

# Список программного обеспечения для анализа. Можно попробовать брать из файла
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
    Запрашивает уязвимости для указанного ПО и версии через Vulners API.
    :param program: название программы
    :param version: версия
    :return: список уязвимостей или None в случае ошибки
    """
    query: str = f"{program} {version}"  # формирование поискового запроса
    params: Dict[str, Any] = {
        "query": query,
        "size": 100,  # максимальное количество результатов
        "sort": "cvss.score"  # сортируем по CVSS
    }
    print(f"Запрос к Vulners API: {query}")
    try:
        response = requests.get(VULNERS_API_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        search_results: List[Dict[str, Any]] = data.get("data", {}).get("search", [])
        print(f"Получено {len(search_results)} результатов для {program} {version}")
        return search_results
    except requests.RequestException as e:
        print(f"Ошибка при запросе к Vulners API для {program} {version}: {e}")
        return None


def analyze_vulnerabilities(vuln_data: Optional[List[Dict[str, Any]]]) -> Dict[str, List[str]]:
    """
    Анализирует данные уязвимостей и возвращает список CVE и информацию об эксплойтах.
    :param vuln_data: данные от Vulners API
    :return: словарь с CVE и эксплойтами
    """
    cve_list: List[str] = []
    exploits_available: List[str] = []

    if not vuln_data:
        print("Нет данных для анализа уязвимостей")
        return {"cve": [], "exploits": []}

    for vuln in vuln_data:
        source: Dict[str, Any] = vuln.get("_source", {})
        cve_entries: List[str] = source.get("cvelist", [])

        for cve in cve_entries:
            if cve.startswith("CVE-") and cve not in cve_list:
                cve_list.append(cve)
                if source.get("is_exploit", False) or "exploit" in source.get("type", "").lower():
                    exploits_available.append(cve)

    print(f"Найдено CVE: {len(cve_list)}, с эксплойтами: {len(exploits_available)}")
    return {"cve": cve_list, "exploits": exploits_available}


if __name__ == "__main__":  # запуск
    if not VULNERS_API:  # проверка наличия API
        print("Ошибка: API-ключ Vulners не найден. Укажите его в .env файле как VULNERS_API_KEY.")
        exit(1)

    report_data: Dict[str, Dict[str, Any]] = {}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        output.write("Отчёт по уязвимостям программного обеспечения\n")
        output.write("=" * 50 + "\n\n")

        for software in SOFTWARE_LIST:
            program: str = software["Program"]
            version: str = software["Version"]
            print(f"\nАнализирую: {program} {version}")

            vuln_data: Optional[List[Dict[str, Any]]] = get_vulnerabilities(program, version)
            analysis: Dict[str, List[str]] = analyze_vulnerabilities(vuln_data)

            report_data[f"{program} {version}"] = {
                "vulnerable": bool(analysis["cve"]),
                "cve_list": analysis["cve"],
                "exploits_available": analysis["exploits"]
            }

    with open(JSON_REPORT_FILE, "w", encoding="utf-8") as json_output:
        json.dump(report_data, json_output, indent=4, ensure_ascii=False)

    print(f"Отчёты сохранены в {OUTPUT_FILE} и {JSON_REPORT_FILE}")
