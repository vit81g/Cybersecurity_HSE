import os  # работа с файловой системой (создание директорий, проверка существования файлов)
import zipfile  # для ZIP-архивов (распаковка файлов)
import requests  # HTTP-запросы
import time  # задержки между запросами (чтобы не превысить лимит API)
import sys  # скрипт и аргументы
import json  # JSON-данные
from dotenv import load_dotenv  # переменные окружения из .env файла

# Загружаем .env файл
load_dotenv()
API_KEY = os.getenv("VT_API_KEY", "")  # API-ключ теперь берется из .env
VT_SCAN_URL = "https://www.virustotal.com/api/v3/files"  # URL для загрузки файлов на анализ
VT_REPORT_URL = "https://www.virustotal.com/api/v3/analyses/{}"  # URL для получения отчета по scan_id
VT_BEHAVIORS_URL = "https://www.virustotal.com/api/v3/files/{}/behaviours"  # URL для данных о поведении
HEADERS = {"x-apikey": API_KEY}  # заголовки запроса с API-ключом
OUTPUT_FILE = "scan_results.txt"  # Файл для отчета
REPORT_FILE = "scan_report.json"  # Файл для JSON
SCREENSHOT_FILE = "scan_results.png"  # (не используется в коде, возможно, для будущего функционала)

# Список антивирусов для проверки из задания
CHECK_AVS = {"Fortinet", "McAfee", "Yandex", "Sophos"}

# Проверка аргументов командной строки (не более одного аргумента)
if len(sys.argv) != 2:
    print("Использование: script.py <name_file>.zip")
    sys.exit(1)

ZIP_FILE = sys.argv[1]  # из аргумента командной строки берется путь
EXTRACTED_DIR = "extracted_files"  # директория для распаковки

# Запрос пароля, если есть или без пароля
password_input = input("Введите пароль для архива (нажмите Enter, чтобы пропустить): ")
PASSWORD = password_input if password_input else None  # пароль или None

# 1. Распаковка архива
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

# 2. Загрузка файлов в VirusTotal и получение scan_id
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

# 3. Получение отчета о сканировании
def get_scan_report(scan_id):
    """
    Получает отчет о сканировании файла в VirusTotal.
    :param scan_id: Уникальный идентификатор сканирования
    :return: JSON-ответ от VirusTotal
    """
    response = requests.get(VT_REPORT_URL.format(scan_id), headers=HEADERS)
    return response.json()

# 4. Получение данных о поведении (новая функция)
def get_behaviors(file_id):
    """
    Получает данные о поведении файла из VirusTotal.
    :param file_id: SHA256 хэш файла
    :return: JSON-данные о поведении или None в случае ошибки
    """
    response = requests.get(VT_BEHAVIORS_URL.format(file_id), headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при получении данных о поведении: {response.status_code}")
        return None

# 5. Анализ данных Sandbox и MITRE ATT&CK (обновленная функция)
def analyze_sandbox_data(sandbox_verdicts, behaviors):
    """
    Анализирует данные VirusTotal Sandbox и MITRE ATT&CK.
    :param sandbox_verdicts: список вердиктов Sandbox из отчета
    :param behaviors: данные о поведении из отдельного запроса
    :return: словарь с доменами, IP-адресами, описанием поведения и техниками MITRE
    """
    domains = set()
    ip_addresses = set()
    behavior_summary = []
    mitre_techniques = []

    # Анализ sandbox_verdicts
    for verdict in sandbox_verdicts:
        network_data = verdict.get("network", {})
        if network_data:
            if "dns_requests" in network_data:
                for request in network_data["dns_requests"]:
                    domain = request.get("domain")
                    if domain:
                        domains.add(domain)
            if "ip_addresses" in network_data:
                for ip in network_data["ip_addresses"]:
                    ip_addresses.add(ip.get("ip_address"))
            elif "tcp_connections" in network_data:
                for conn in network_data["tcp_connections"]:
                    ip_addresses.add(conn.get("destination_ip"))

        behavior = verdict.get("behavior", {})
        if behavior:
            behavior_summary.append({
                "sandbox_name": verdict.get("sandbox_name", "Unknown"),
                "description": behavior.get("description", "No detailed behavior description available")
            })

    # Анализ MITRE ATT&CK из behaviors
    if behaviors and behaviors.get("data"):
        for entry in behaviors["data"]:
            attributes = entry.get("attributes", {})
            mitre_attack_techniques = attributes.get("mitre_attack_techniques", [])
            for technique in mitre_attack_techniques:
                mitre_techniques.append({
                    "id": technique.get("id"),
                    "description": technique.get("signature_description", "No description")
                })

    return {
        "domains": list(domains),
        "ip_addresses": list(ip_addresses),
        "behavior_summary": behavior_summary,
        "mitre_techniques": mitre_techniques
    }

# Выполнение скрипта
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
            time.sleep(15)  # ожидание между запросами

        results = {}  # хранение полученных отчетов
        for scan_id in scan_ids:
            time.sleep(15)  # ожидание перед следующим запросом
            report = get_scan_report(scan_id)
            results[scan_id] = report

        output.write("Результаты анализа:\n")
        for scan_id, report in results.items():
            stats = report.get("data", {}).get("attributes", {}).get("stats", {})
            detections = report.get("data", {}).get("attributes", {}).get("results", {})
            sandbox_verdicts = report.get("data", {}).get("attributes", {}).get("sandbox_verdicts", [])
            file_id = report.get("meta", {}).get("file_info", {}).get("sha256", "")  # SHA256 для behaviors

            detected_avs = {av for av, details in detections.items() if details.get("category") == "malicious"}
            detected_check_avs = detected_avs.intersection(CHECK_AVS)
            missed_check_avs = CHECK_AVS - detected_avs

            # Получение данных о поведении и анализ
            behaviors = get_behaviors(file_id)
            sandbox_analysis = analyze_sandbox_data(sandbox_verdicts, behaviors)

            report_data[scan_id] = {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "detected_antiviruses": list(detected_avs),
                "detected_check_avs": list(detected_check_avs),
                "missed_check_avs": list(missed_check_avs),
                "sandbox_verdicts": sandbox_verdicts,
                "sandbox_analysis": sandbox_analysis  # добавляем результаты (платная версия)
            }

            output.write(f"Scan ID: {scan_id}\n")
            output.write(f"Malicious: {stats.get('malicious', 0)}\n")
            output.write(f"Suspicious: {stats.get('suspicious', 0)}\n")
            output.write(f"Harmless: {stats.get('harmless', 0)}\n")
            output.write("Обнаруженные антивирусами угрозы:\n")
            output.write(", ".join(detected_avs) + "\n")

            # Вывод информации из Sandbox и MITRE ATT&CK
            output.write("Sandbox и MITRE ATT&CK Анализ:\n")
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
            if sandbox_analysis["mitre_techniques"]:
                output.write("MITRE ATT&CK Техники:\n")
                for technique in sandbox_analysis["mitre_techniques"]:
                    output.write(f"{technique['id']}: {technique['description']}\n")
            if not any(sandbox_analysis.values()):
                output.write("Данные о поведении в Sandbox и MITRE ATT&CK отсутствуют.\n")
            output.write("\n")  # новая строка

    with open(REPORT_FILE, "w", encoding="utf-8") as report_output:
        json.dump(report_data, report_output, indent=4, ensure_ascii=False)

    print(f"Результаты анализа сохранены в {OUTPUT_FILE} и {REPORT_FILE}")