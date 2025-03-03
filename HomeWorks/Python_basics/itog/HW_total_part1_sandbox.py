import os  # Работа с файловой системой (создание директорий, проверка существования файлов)
import zipfile  # Работа с ZIP-архивами (распаковка файлов)
import requests  # Отправка HTTP-запросов к API VirusTotal
import time  # Добавление задержек между запросами (чтобы не превысить лимит API)
import sys  # Получение аргументов командной строки
import json  # Работа с JSON-данными (сохранение и обработка отчетов)
from dotenv import load_dotenv  # Загрузка переменных окружения из .env файла

# Загружаем .env файл
load_dotenv()
API_KEY = os.getenv("VT_API_KEY", "")  # API-ключ теперь берется из .env
VT_SCAN_URL = "https://www.virustotal.com/api/v3/files"  # URL для загрузки файлов на анализ
VT_REPORT_URL = "https://www.virustotal.com/api/v3/analyses/{}"  # URL для получения отчета по scan_id
HEADERS = {"x-apikey": API_KEY}  # Заголовки запроса с API-ключом
OUTPUT_FILE = "scan_results.txt"  # Файл для сохранения текстового отчета
REPORT_FILE = "scan_report.json"  # Файл для сохранения отчета в JSON-формате
SCREENSHOT_FILE = "scan_results.png"  # (Не используется в коде, возможно, для будущего функционала)

# Список антивирусов для проверки
CHECK_AVS = {"Fortinet", "McAfee", "Yandex", "Sophos"}

# Проверка аргументов командной строки (должен быть передан путь к ZIP-файлу)
if len(sys.argv) != 2:
    print("Использование: script.py <name_file>.zip")
    sys.exit(1)

ZIP_FILE = sys.argv[1]  # Получение пути к архиву из аргумента командной строки
EXTRACTED_DIR = "extracted_files"  # Директория для извлечения файлов

# Запрос пароля у пользователя для распаковки архива
password_input = input("Введите пароль для архива (нажмите Enter, чтобы пропустить): ")
PASSWORD = password_input if password_input else None  # Используется введенный пароль или None

# 1. Распаковка архива
def extract_zip(zip_path, extract_to, password):
    """
    Извлекает файлы из ZIP-архива в указанную директорию.
    :param zip_path: Путь к ZIP-файлу
    :param extract_to: Директория для извлечения
    :param password: Пароль для архива (если есть)
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        try:
            zip_ref.extractall(extract_to, pwd=bytes(password, 'utf-8') if password else None)
            print("Файлы успешно извлечены.")
        except RuntimeError:
            print("Ошибка: неверный пароль или архив не защищен паролем.")

# 2. Загрузка файлов в VirusTotal и получение scan_id
def upload_file_to_vt(file_path):
    """
    Загружает файл в VirusTotal для анализа и возвращает scan_id.
    :param file_path: Путь к файлу
    :return: scan_id или пустая строка в случае ошибки
    """
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(VT_SCAN_URL, headers=HEADERS, files=files)
    return response.json().get("data", {}).get("id", "")

# 3. Получение отчета о сканировании
def get_scan_report(scan_id):
    """
    Получает отчет о сканировании файла в VirusTotal.
    :param scan_id: Уникальный идентификатор сканирования
    :return: JSON-ответ от VirusTotal
    """
    response = requests.get(VT_REPORT_URL.format(scan_id), headers=HEADERS)
    return response.json()

# Новая функция: Анализ данных Sandbox
def analyze_sandbox_data(sandbox_verdicts):
    """
    Анализирует данные VirusTotal Sandbox и извлекает домены, IP-адреса и поведение.
    :param sandbox_verdicts: Список вердиктов Sandbox из отчета
    :return: Словарь с доменами, IP-адресами и описанием поведения
    """
    domains = set()
    ip_addresses = set()
    behavior_summary = []

    for verdict in sandbox_verdicts:
        # Извлечение сетевых взаимодействий (если доступны)
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
            elif "tcp_connections" in network_data:  # Проверка TCP-соединений
                for conn in network_data["tcp_connections"]:
                    ip_addresses.add(conn.get("destination_ip"))

        # Описание поведения
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

# Основная логика выполнения скрипта
if __name__ == "__main__":
    if not os.path.exists(EXTRACTED_DIR):
        os.makedirs(EXTRACTED_DIR)

    extract_zip(ZIP_FILE, EXTRACTED_DIR, PASSWORD)  # Распаковка архива
    scan_ids = []  # Список scan_id отправленных файлов
    report_data = {}  # Итоговые данные отчета

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        for file in os.listdir(EXTRACTED_DIR):
            file_path = os.path.join(EXTRACTED_DIR, file)
            scan_id = upload_file_to_vt(file_path)
            print(f"Файл {file} отправлен. Scan ID: {scan_id}")
            output.write(f"Файл {file} отправлен. Scan ID: {scan_id}\n")
            scan_ids.append(scan_id)
            time.sleep(15)  # Ожидание между запросами

        results = {}  # Хранение полученных отчетов
        for scan_id in scan_ids:
            report = get_scan_report(scan_id)
            results[scan_id] = report
            time.sleep(15)  # Ожидание перед следующим запросом

        output.write("Результаты анализа:\n")
        for scan_id, report in results.items():
            stats = report.get("data", {}).get("attributes", {}).get("stats", {})
            detections = report.get("data", {}).get("attributes", {}).get("results", {})
            sandbox_data = report.get("data", {}).get("attributes", {}).get("sandbox_verdicts", [])

            detected_avs = {av for av, details in detections.items() if details.get("category") == "malicious"}
            detected_check_avs = detected_avs.intersection(CHECK_AVS)
            missed_check_avs = CHECK_AVS - detected_avs

            # Анализ данных Sandbox
            sandbox_analysis = analyze_sandbox_data(sandbox_data)

            report_data[scan_id] = {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "detected_antiviruses": list(detected_avs),
                "detected_check_avs": list(detected_check_avs),
                "missed_check_avs": list(missed_check_avs),
                "sandbox_verdicts": sandbox_data,
                "sandbox_analysis": sandbox_analysis  # Добавляем результаты анализа Sandbox
            }

            output.write(f"Scan ID: {scan_id}\n")
            output.write(f"Malicious: {stats.get('malicious', 0)}\n")
            output.write(f"Suspicious: {stats.get('suspicious', 0)}\n")
            output.write(f"Harmless: {stats.get('harmless', 0)}\n")
            output.write("Обнаруженные антивирусами угрозы:\n")
            output.write(", ".join(detected_avs) + "\n")

            # Добавляем информацию из Sandbox в текстовый отчёт
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
            output.write("\n")  # Разделитель между отчётами

    with open(REPORT_FILE, "w", encoding="utf-8") as report_output:
        json.dump(report_data, report_output, indent=4, ensure_ascii=False)

    print(f"Результаты анализа сохранены в {OUTPUT_FILE} и {REPORT_FILE}")