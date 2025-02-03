"""
Предварительные действия перед запуском скрипта
1. активация venv
source venv/bin/activate

2. установка
pip install scapy

3. запуск скрипта
sudo python hw09.py
"""


#!/usr/bin/env python3
from scapy.all import sniff, TCP, Raw

def packet_callback(packet):
    if packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
        except Exception:
            payload = ""
        if "HTTP" in payload or "GET" in payload or "POST" in payload:
            with open("http_traffic.txt", "a", encoding="utf-8") as f:
                f.write("="*60 + "\n")
                f.write("Перехваченный пакет:\n")
                f.write(payload + "\n")
                f.write("="*60 + "\n\n")
            print("Пакет записан в файл.")

if __name__ == "__main__":
    print("Запуск прослушивания HTTP-трафика на порту 80...")
    sniff(filter="tcp port 80", prn=packet_callback, store=0)
