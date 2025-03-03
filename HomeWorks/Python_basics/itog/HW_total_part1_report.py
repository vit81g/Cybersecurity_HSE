import os
import zipfile
import requests
import time
import sys

# Константы
API_KEY_VIRUSTOTAL = "7a0ddb1b01d85a21a1236cdcfc25978f99b33e3e55e4f6a2a154d3eebd24d594"
VT_SCAN_URL = "https://www.virustotal.com/api/v3/files"
VT_REPORT_URL = "https://www.virustotal.com/api/v3/analyses/{}"
HEADERS = {"x-apikey": API_KEY_VIRUSTOTAL}

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
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        try:
            zip_ref.extractall(extract_to, pwd=bytes(password, 'utf-8') if password else None)
            print("Файлы успешно извлечены.")
        except RuntimeError:
            print("Ошибка: неверный пароль или архив не защищен паролем.")


# 2. Загрузка файлов в VirusTotal и получение scan_id
def upload_file_to_vt(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(VT_SCAN_URL, headers=HEADERS, files=files)
    return response.json().get("data", {}).get("id", "")


# 3. Получение отчета о сканировании
def get_scan_report(scan_id):
    response = requests.get(VT_REPORT_URL.format(scan_id), headers=HEADERS)
    return response.json()


# Основная логика
if __name__ == "__main__":
    if not os.path.exists(EXTRACTED_DIR):
        os.makedirs(EXTRACTED_DIR)

    extract_zip(ZIP_FILE, EXTRACTED_DIR, PASSWORD)
    scan_ids = []

    for file in os.listdir(EXTRACTED_DIR):
        file_path = os.path.join(EXTRACTED_DIR, file)
        scan_id = upload_file_to_vt(file_path)
        print(f"Файл {file} отправлен. Scan ID: {scan_id}")
        scan_ids.append(scan_id)
        time.sleep(15)  # Ожидание между запросами

    results = {}
    for scan_id in scan_ids:
        report = get_scan_report(scan_id)
        results[scan_id] = report
        time.sleep(15)  # Ожидание перед следующим запросом

    print("Результаты анализа:")
    for scan_id, report in results.items():
        print(report)