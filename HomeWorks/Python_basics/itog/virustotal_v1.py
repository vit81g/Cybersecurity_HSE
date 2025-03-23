import os  # работа с файловой системой (создание директорий, проверка существования файлов)
import zipfile  # для ZIP-архивов (распаковка файлов)
import requests  # HTTP-запросы
import time  # задержки между запросами (чтобы не превысить лимит API, не понятно надо или нет)
import sys  # скрипт и аргументы
import json  # JSON-данные
from dotenv import load_dotenv  # переменные окружения из .env файла

# загружаем .env файл
load_dotenv()
API_KEY = os.getenv("VT_API_KEY", "")  # API-ключ теперь берется из .env
VT_SCAN_URL = "https://www.virustotal.com/api/v3/files"  # URL для загрузки файлов на анализ
VT_REPORT_URL = "https://www.virustotal.com/api/v3/analyses/{}"  # URL для получения отчета по scan_id
HEADERS = {"x-apikey": API_KEY}  # заголовки запроса с API-ключом
OUTPUT_FILE = "scan_results.txt"  # Файл для отчета
REPORT_FILE = "scan_report.json"  # Файл для JSON
SCREENSHOT_FILE = "scan_results.png"  # (не используется в коде, возможно, для будущего функционала)

# список антивирусов для проверки из задания
CHECK_AVS = {"Fortinet", "McAfee", "Yandex", "Sophos"}

# проверка аргументов командной строки (не более одного аргумента)
if len(sys.argv) != 2:
    print("Использование: script.py <name_file>.zip")
    sys.exit(1)

ZIP_FILE = sys.argv[1]  # из аргумента командной строки берется путь
EXTRACTED_DIR = "extracted_files"  # директория для распаковки (в linux без проблем, винда в исключение добавить)

# запрос пароля, если есть или без пароля
password_input = input("Введите пароль для архива (нажмите Enter, чтобы пропустить): ")
PASSWORD = password_input if password_input else None  # пароль или None

# 1. распаковка архива
def extract_zip(zip_path, extract_to, password):
    """
    Извлекает файлы из ZIP-архива в указанную директорию.
    :param zip_path: путь к ZIP-файлу
    :param extract_to: директория для извлечения
    :param password: пароль для архива (если есть)
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        try:
            zip_ref.extractall(extract_to, pwd=bytes(password, 'utf-8') if password else None)
            print("Файлы успешно извлечены.")
        except RuntimeError:
            print("Ошибка: неверный пароль или архив не защищен паролем.")

# 2. загрузка файлов в VirusTotal и получение scan_id (можно другие методы)
def upload_file_to_vt(file_path):
    """
    Загружает файл в VirusTotal для анализа и возвращает scan_id.
    :param file_path: путь к файлу
    :return: scan_id или пустая строка в случае ошибки
    """
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(VT_SCAN_URL, headers=HEADERS, files=files)
    return response.json().get("data", {}).get("id", "")

# 3. получение отчета о сканировании
def get_scan_report(scan_id):
    """
    Получает отчет о сканировании файла в VirusTotal.
    :param scan_id: Уникальный идентификатор сканирования
    :return: JSON-ответ от VirusTotal
    """
    response = requests.get(VT_REPORT_URL.format(scan_id), headers=HEADERS)
    return response.json()

# анализ данных Sandbox (работает в платной версии, не смог проверить, на сайте норм)
def analyze_sandbox_data(sandbox_verdicts):
    """
    Анализирует данные VirusTotal Sandbox и извлекает домены, IP-адреса и поведение.
    :param sandbox_verdicts: список вердиктов Sandbox из отчета
    :return: словарь с доменами, IP-адресами и описанием поведения
    """
    domains = set()
    ip_addresses = set()
    behavior_summary = []

    for verdict in sandbox_verdicts:
        # извлечение сетевых взаимодействий (платная версия)
        network_data = verdict.get("network", {})
        if network_data:
            # Домены
            if "dns_requests" in network_data:
                for request in network_data["dns_requests"]:
                    domain = request.get("domain")
                    if domain:
                        domains.add(domain)
            # IP-адреса
            if "ip_addresses" in network_data:
                for ip in network_data["ip_addresses"]:
                    ip_addresses.add(ip.get("ip_address"))
            elif "tcp_connections" in network_data:  # проверка TCP-соединений
                for conn in network_data["tcp_connections"]:
                    ip_addresses.add(conn.get("destination_ip"))

        # описание поведения (платная версия)
        behavior = verdict.get("behavior", {})
        if behavior:
            behavior_summary.append({
                "sandbox_name": verdict.get("sandbox_name", "Unknown"),
                "description": behavior.get("description", "No detailed behavior description available")
            })

    return {
        "domains": list(domains),
        "ip_addresses": list(ip_addresses),
        "behavior_summary": behavior_summary
    }

# выполнение скрипта
if __name__ == "__main__":
    if not os.path.exists(EXTRACTED_DIR):
        os.makedirs(EXTRACTED_DIR)

    extract_zip(ZIP_FILE, EXTRACTED_DIR, PASSWORD)  # распаковка архива
    scan_ids = []  # список scan_id отправленных файлов
    report_data = {}  # итоговые данные отчета

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        for file in os.listdir(EXTRACTED_DIR):
            file_path = os.path.join(EXTRACTED_DIR, file)
            scan_id = upload_file_to_vt(file_path)
            print(f"Файл {file} отправлен. Scan ID: {scan_id}")
            output.write(f"Файл {file} отправлен. Scan ID: {scan_id}\n")
            scan_ids.append(scan_id)
            time.sleep(15)  # ожидание между запросами, может надо увеличить для точного ответа

        results = {}  # хранение полученных отчетов
        for scan_id in scan_ids:
            report = get_scan_report(scan_id)
            results[scan_id] = report
            time.sleep(15)  # ожидание перед следующим запросом, может надо увеличить

        output.write("Результаты анализа:\n")
        for scan_id, report in results.items():
            stats = report.get("data", {}).get("attributes", {}).get("stats", {})
            detections = report.get("data", {}).get("attributes", {}).get("results", {})
            sandbox_data = report.get("data", {}).get("attributes", {}).get("sandbox_verdicts", [])

            detected_avs = {av for av, details in detections.items() if details.get("category") == "malicious"}
            detected_check_avs = detected_avs.intersection(CHECK_AVS)
            missed_check_avs = CHECK_AVS - detected_avs

            # анализ данных Sandbox (платная версия)
            sandbox_analysis = analyze_sandbox_data(sandbox_data)

            report_data[scan_id] = {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "detected_antiviruses": list(detected_avs),
                "detected_check_avs": list(detected_check_avs),
                "missed_check_avs": list(missed_check_avs),
                "sandbox_verdicts": sandbox_data,
                "sandbox_analysis": sandbox_analysis  # добавляем результаты (платная версия)
            }

            output.write(f"Scan ID: {scan_id}\n")
            output.write(f"Malicious: {stats.get('malicious', 0)}\n")
            output.write(f"Suspicious: {stats.get('suspicious', 0)}\n")
            output.write(f"Harmless: {stats.get('harmless', 0)}\n")
            output.write("Обнаруженные антивирусами угрозы:\n")
            output.write(", ".join(detected_avs) + "\n")

            # вывод информации из Sandbox в отчёт
            output.write("Sandbox Analysis:\n")
            if sandbox_analysis["domains"]:
                output.write("Сетевые домены для блокировки:\n")
                output.write(", ".join(sandbox_analysis["domains"]) + "\n")
            if sandbox_analysis["ip_addresses"]:
                output.write("IP-адреса для блокировки:\n")
                output.write(", ".join(sandbox_analysis["ip_addresses"]) + "\n")
            if sandbox_analysis["behavior_summary"]:
                output.write("Поведение вредоноса:\n")
                for behavior in sandbox_analysis["behavior_summary"]:
                    output.write(f"{behavior['sandbox_name']}: {behavior['description']}\n")
            else:
                output.write("Данные о поведении в Sandbox отсутствуют.\n")
            output.write("\n")  # новая строка

    with open(REPORT_FILE, "w", encoding="utf-8") as report_output:
        json.dump(report_data, report_output, indent=4, ensure_ascii=False)

    print(f"Результаты анализа сохранены в {OUTPUT_FILE} и {REPORT_FILE}")