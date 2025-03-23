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

# Распаковка архива
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

# Загрузка файлов в VirusTotal и получение scan_id
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

# Получение отчета о сканировании
def get_scan_report(scan_id):
    """
    Получает отчет о сканировании файла в VirusTotal.
    :param scan_id: Уникальный идентификатор сканирования
    :return: JSON-ответ от VirusTotal
    """
    response = requests.get(VT_REPORT_URL.format(scan_id), headers=HEADERS)
    return response.json()

# Получение данных о поведении
def get_behaviors(file_id):
    """
    Получает данные о поведении файла из VirusTotal.
    :param file_id: SHA256 хэш файла
    :return: JSON-данные о поведении или None в случае ошибки
    """
    response = requests.get(VT_BEHAVIORS_URL.format(file_id), headers=HEADERS)
    # Проверяем, успешен ли запрос (код 200)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при получении данных о поведении: {response.status_code}")
        return None

# Анализ данных поведения (Sandbox и MITRE ATT&CK)
def analyze_behaviors(behaviors):
    """
    Анализирует данные о поведении файла, включая сетевые взаимодействия и техники MITRE ATT&CK.
    :param behaviors: данные о поведении из VirusTotal
    :return: словарь с хостами, IP-адресами и техниками MITRE ATT&CK
    """
    hostnames = set()  # Множество для уникальных имен хостов
    resolved_ips = set()  # Множество для уникальных IP-адресов
    mitre_techniques = []  # Список для хранения техник MITRE ATT&CK

    # Проверяем, есть ли данные о поведении
    if behaviors and behaviors.get("data"):
        # Проходим по каждому элементу данных о поведении
        for entry in behaviors["data"]:
            attributes = entry.get("attributes", {})  # Получаем атрибуты поведения
            dns_lookups = attributes.get("dns_lookups", [])  # Список DNS-запросов
            # Извлекаем хосты и IP из DNS-запросов
            for lookup in dns_lookups:
                # Если есть имя хоста, добавляем его
                if "hostname" in lookup:
                    hostnames.add(lookup["hostname"])
                # Если есть разрешённые IP, добавляем их
                if "resolved_ips" in lookup:
                    resolved_ips.update(lookup["resolved_ips"])
            # Извлекаем техники MITRE ATT&CK
            mitre_attack_techniques = attributes.get("mitre_attack_techniques", [])
            # Проходим по списку техник и добавляем их в результат
            for technique in mitre_attack_techniques:
                mitre_techniques.append({
                    "id": technique.get("id"),
                    "description": technique.get("signature_description", "No description")
                })
    return {
        "hostnames": list(hostnames),
        "resolved_ips": list(resolved_ips),
        "mitre_techniques": mitre_techniques
    }

if __name__ == "__main__":
    # Создаем директорию для извлечения файлов, если её нет
    if not os.path.exists(EXTRACTED_DIR):
        os.makedirs(EXTRACTED_DIR)

    extract_zip(ZIP_FILE, EXTRACTED_DIR, PASSWORD)  # Распаковываем архив
    scan_ids = []  # Список для хранения идентификаторов сканирования
    report_data = {}  # Словарь для итоговых данных отчета

    # Открываем файл для записи результатов
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        # Проходим по всем файлам в директории extracted_files
        for file in os.listdir(EXTRACTED_DIR):
            file_path = os.path.join(EXTRACTED_DIR, file)  # Формируем полный путь к файлу
            scan_id = upload_file_to_vt(file_path)  # Отправляем файл на анализ
            print(f"Файл {file} отправлен. Scan ID: {scan_id}")
            output.write(f"Файл {file} отправлен. Scan ID: {scan_id}\n")
            scan_ids.append(scan_id)  # Добавляем scan_id в список
            time.sleep(15)  # Задержка для соблюдения лимитов API

        # Обрабатываем каждый scan_id для получения отчета
        for scan_id in scan_ids:
            time.sleep(15)  # Задержка перед запросом отчета
            report = get_scan_report(scan_id)  # Получаем отчет о сканировании
            # Проверяем, получили ли мы отчет
            if not report:
                continue  # Пропускаем, если отчет пустой

            # Извлекаем статистику и результаты обнаружения
            stats = report.get("data", {}).get("attributes", {}).get("stats", {})
            detections = report.get("data", {}).get("attributes", {}).get("results", {})
            file_id = report.get("meta", {}).get("file_info", {}).get("sha256", "")

            # Получаем данные о поведении файла
            behaviors = get_behaviors(file_id)
            behavior_analysis = analyze_behaviors(behaviors)  # Анализируем поведение

            # Формируем список антивирусов, обнаруживших угрозы
            detected_avs = {av for av, details in detections.items() if details.get("category") == "malicious"}
            detected_check_avs = detected_avs.intersection(CHECK_AVS)  # Пересечение с CHECK_AVS
            missed_check_avs = CHECK_AVS - detected_avs  # Не обнаружившие из CHECK_AVS

            # Сохраняем данные в словарь отчета
            report_data[scan_id] = {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "detected_antiviruses": list(detected_avs),
                "detected_check_avs": list(detected_check_avs),
                "missed_check_avs": list(missed_check_avs),
                "behavior_analysis": behavior_analysis
            }

            # Записываем базовые результаты сканирования
            output.write(f"\nScan ID: {scan_id}\n")
            output.write(f"Malicious: {stats.get('malicious', 0)}\n")
            output.write(f"Suspicious: {stats.get('suspicious', 0)}\n")
            output.write(f"Harmless: {stats.get('harmless', 0)}\n")
            output.write("Обнаруженные антивирусами угрозы:\n")
            output.write(", ".join(detected_avs) + "\n")

            # Вывод Sandbox анализа
            output.write(f"\nSandbox Анализ для файла {file_id}:\n")
            # Проверяем, есть ли данные о хостах или IP
            if behavior_analysis["hostnames"] or behavior_analysis["resolved_ips"]:
                # Если есть хосты, выводим их
                if behavior_analysis["hostnames"]:
                    output.write("Hostnames:\n")
                    # Проходим по списку хостов и записываем каждый
                    for hostname in behavior_analysis["hostnames"]:
                        output.write(f"- {hostname}\n")
                # Если есть IP, выводим их
                if behavior_analysis["resolved_ips"]:
                    output.write("Resolved IPs:\n")
                    # Проходим по списку IP и записываем каждый
                    for ip in behavior_analysis["resolved_ips"]:
                        output.write(f"- {ip}\n")
            else:
                output.write("Данные Sandbox отсутствуют.\n")

            # Вывод MITRE ATT&CK анализа
            output.write(f"\nMITRE ATT&CK Анализ для файла {file_id}:\n")
            # Проверяем, есть ли техники MITRE ATT&CK
            if behavior_analysis["mitre_techniques"]:
                output.write("MITRE Attack Techniques:\n")
                # Проходим по списку техник и записываем каждую
                for technique in behavior_analysis["mitre_techniques"]:
                    output.write(f"- {technique['id']}: {technique['description']}\n")
            else:
                output.write("Данные MITRE ATT&CK отсутствуют.\n")

    # Сохраняем полный отчет в JSON-файл
    with open(REPORT_FILE, "w", encoding="utf-8") as report_output:
        json.dump(report_data, report_output, indent=4, ensure_ascii=False)

    print(f"Результаты анализа сохранены в {OUTPUT_FILE} и {REPORT_FILE}")