import requests
import json

# URL API Vulners
VULNERS_API_URL = "https://vulners.com/api/v3/search/lucene/"

# Список ПО для анализа
software_list = [
    {"Program": "LibreOffice", "Version": "6.0.7"},
    {"Program": "7zip", "Version": "18.05"},
    {"Program": "Adobe Reader", "Version": "2018.011.20035"},
    {"Program": "nginx", "Version": "1.14.0"},
    {"Program": "Apache HTTP Server", "Version": "2.4.29"},
    {"Program": "DjVu Reader", "Version": "2.0.0.27"},
    {"Program": "Wireshark", "Version": "2.6.1"},
    {"Program": "Notepad++", "Version": "7.5.6"},
    {"Program": "Google Chrome", "Version": "68.0.3440.106"},
    {"Program": "Mozilla Firefox", "Version": "61.0.1"},
]


# Функция запроса уязвимостей
def check_vulnerabilities(program, version):
    query = f"{program} {version}"

    params = {
        "query": query,  # Улучшенный поиск по названию
        "type": "software",  # Уточнение, что это ПО
        "limit": 10,  # Ограничение числа записей
    }

    try:
        response = requests.get(VULNERS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        vulnerabilities = data.get("data", {}).get("search", [])

        if vulnerabilities:
            cve_list = [vuln["id"] for vuln in vulnerabilities if "id" in vuln]
            exploits = [vuln for vuln in vulnerabilities if "exploit" in vuln.get("type", "")]
            return {"CVE": cve_list, "Exploits": bool(exploits)}
        else:
            return {"CVE": [], "Exploits": False}

    except requests.RequestException as e:
        print(f"Ошибка запроса для {program} {version}: {e}")
        return {"CVE": [], "Exploits": False}


# Анализ всех программ
report = {}
for software in software_list:
    program = software["Program"]
    version = software["Version"]
    print(f"🔍 Проверяем {program} {version}...")
    report[program] = check_vulnerabilities(program, version)

# Сохранение отчета
with open("fixed_vulnerability_report.json", "w") as f:
    json.dump(report, f, indent=4)

print("Отчет сохранен в 'fixed_vulnerability_report.json'")
