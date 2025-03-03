import os
import zipfile
import requests
import time
import sys
import json

# Константы
API_KEY_VIRUSTOTAL = "7a0ddb1b01d85a21a1236cdcfc25978f99b33e3e55e4f6a2a154d3eebd24d594"
VT_SCAN_URL = "https://www.virustotal.com/api/v3/files"
VT_REPORT_URL = "https://www.virustotal.com/api/v3/analyses/{}"
HEADERS = {"x-apikey": API_KEY_VIRUSTOTAL}
OUTPUT_FILE = "scan_results.txt"
REPORT_FILE = "scan_report.json"
SCREENSHOT_FILE = "scan_results.png"

# Антивирусы для сравнения
CHECK_AVS = {"Fortinet", "McAfee", "Yandex", "Sophos"}

# Проверка аргументов командной строки
if len(sys.argv) != 2:
    print("Использование: script.py <name_file>.zip")
    sys.exit(1)

ZIP_FILE = sys.argv[1]
EXTRACTED_DIR = "extracted_files"

# Запрос пароля у пользователя
password_input = input("Введите пароль для архива (нажмите Enter, чтобы пропустить): ")
PASSWORD = password_input if password_input else None


# 1. Распаковка архива
def extract_zip(zip_path, extract_to, password):
    """
    Извлекает файлы из ZIP-архива.
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
    Загружает файл в VirusTotal для анализа.
    """
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(VT_SCAN_URL, headers=HEADERS, files=files)
    return response.json().get("data", {}).get("id", "")


# 3. Получение отчета о сканировании
def get_scan_report(scan_id):
    """
    Получает отчет о сканировании файла в VirusTotal.
    """
    response = requests.get(VT_REPORT_URL.format(scan_id), headers=HEADERS)
    return response.json()


# Основная логика
if __name__ == "__main__":
    if not os.path.exists(EXTRACTED_DIR):
        os.makedirs(EXTRACTED_DIR)

    extract_zip(ZIP_FILE, EXTRACTED_DIR, PASSWORD)
    scan_ids = []
    report_data = {}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        for file in os.listdir(EXTRACTED_DIR):
            file_path = os.path.join(EXTRACTED_DIR, file)
            scan_id = upload_file_to_vt(file_path)
            print(f"Файл {file} отправлен. Scan ID: {scan_id}")
            output.write(f"Файл {file} отправлен. Scan ID: {scan_id}\n")
            scan_ids.append(scan_id)
            time.sleep(15)  # Ожидание между запросами

        results = {}
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

            report_data[scan_id] = {
                "malicious": stats.get("malicious", 0),
                "suspicious": stats.get("suspicious", 0),
                "harmless": stats.get("harmless", 0),
                "detected_antiviruses": list(detected_avs),
                "detected_check_avs": list(detected_check_avs),
                "missed_check_avs": list(missed_check_avs),
                "sandbox_verdicts": sandbox_data,
            }

            output.write(f"Scan ID: {scan_id}\n")
            output.write(f"Malicious: {stats.get('malicious', 0)}\n")
            output.write(f"Suspicious: {stats.get('suspicious', 0)}\n")
            output.write(f"Harmless: {stats.get('harmless', 0)}\n")
            output.write("Обнаруженные антивирусами угрозы:\n")
            output.write(", ".join(detected_avs) + "\n")
            output.write("Антивирусы, обнаружившие угрозу: " + ", ".join(detected_check_avs) + "\n")
            output.write("Антивирусы, НЕ обнаружившие угрозу: " + ", ".join(missed_check_avs) + "\n")
            output.write("Sandbox Verdicts: " + json.dumps(sandbox_data, indent=4) + "\n\n")

    with open(REPORT_FILE, "w", encoding="utf-8") as report_output:
        json.dump(report_data, report_output, indent=4, ensure_ascii=False)

    print(f"Результаты анализа сохранены в {OUTPUT_FILE} и {REPORT_FILE}")