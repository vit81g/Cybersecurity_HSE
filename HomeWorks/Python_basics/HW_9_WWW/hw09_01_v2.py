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
import threading
import time
from scapy.all import sniff, IP, TCP, sr1, send, Raw


def packet_callback(packet):
    """
    Обработка перехваченных пакетов.
    Если пакет содержит данные и в них обнаруживается HTTP-трафик,
    выводим информацию в консоль и записываем её в файл captured_traffic.txt.
    """
    if packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
        except Exception:
            payload = ""
        if "HTTP" in payload or "GET" in payload or "POST" in payload:
            output = (
                    "=" * 60 + "\n" +
                    "Перехваченный пакет:\n" +
                    payload + "\n" +
                    "=" * 60 + "\n\n"
            )
            print(output)
            with open("captured_traffic.txt", "a", encoding="utf-8") as f:
                f.write(output)


def start_sniffing():
    """
    Запускает перехват трафика на TCP порту 80.
    При необходимости можно явно указать сетевой интерфейс (например, iface="eth0").
    """
    print("Запуск прослушивания HTTP-трафика на порту 80...")
    sniff(filter="tcp port 80", prn=packet_callback, store=0)


def send_http_request():
    """
    Отправляет HTTP GET-запрос через Scapy:
      - Выполняет установление TCP-соединения (SYN, SYN/ACK, ACK).
      - Отправляет HTTP GET-запрос.
    Лог действий записывается в файл sent_requests.txt.
    """
    # Небольшая задержка, чтобы прослушивание уже запустилось
    time.sleep(1)

    target_ip = "93.184.216.34"  # IP-адрес example.com
    target_port = 80

    ip_packet = IP(dst=target_ip)

    # Логируем последовательность действий
    log_lines = []

    # 1. Отправка SYN для начала TCP-рукопожатия
    syn_packet = TCP(dport=target_port, flags="S", seq=1000)
    log_lines.append("Отправка SYN...\n")
    syn_ack = sr1(ip_packet / syn_packet, timeout=2)
    if not syn_ack:
        log_lines.append("SYN/ACK не получен. Проверьте адрес или настройки сети.\n")
        with open("sent_requests.txt", "a", encoding="utf-8") as f:
            f.writelines(log_lines)
        print("SYN/ACK не получен.")
        return
    log_lines.append("Получен SYN/ACK:\n" + str(syn_ack.summary()) + "\n")

    # 2. Завершение рукопожатия отправкой ACK
    ack_packet = TCP(dport=target_port, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
    send(ip_packet / ack_packet)
    log_lines.append("Отправлен ACK для завершения рукопожатия.\n")

    # 3. Отправка HTTP GET-запроса
    http_payload = "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
    data_packet = TCP(dport=target_port, flags="PA", seq=syn_ack.ack, ack=syn_ack.seq + 1)
    log_lines.append("Отправка HTTP GET запроса:\n" + http_payload + "\n")
    send(ip_packet / data_packet / http_payload)
    log_lines.append("HTTP запрос отправлен.\n")

    # Запись логов в файл sent_requests.txt
    with open("sent_requests.txt", "a", encoding="utf-8") as f:
        f.writelines(log_lines)

    print("HTTP-запрос отправлен и лог записан в sent_requests.txt.")


if __name__ == "__main__":
    # Запускаем перехват трафика в отдельном потоке
    sniff_thread = threading.Thread(target=start_sniffing)
    sniff_thread.daemon = True  # Поток-демон завершится вместе с основным потоком
    sniff_thread.start()

    # Отправляем HTTP-запрос и логируем процесс
    send_http_request()

    # Даем время на получение и перехват ответов (например, 5 секунд)
    time.sleep(5)
    print("Завершение работы скрипта.")
