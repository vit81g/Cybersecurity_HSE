"""
Этап 2. Анализ трафика
● Ознакомьтесь с инструментом Google Gruyere и запустите его.
● Запустите Scapy и начните собирать трафик, взаимодействуя с сайтом Google Gruyere.
● Проанализируйте полученные данные, обращая внимание на запросы и ответы HTTP.
"""

#!/usr/bin/env python3
# импорт библиотек
import threading
import time
from scapy.all import sniff, TCP, Raw


def packet_callback(packet):
    """
    Обработка перехваченных пакетов. Если пакет содержит данные и в них обнаруживается HTTP-трафик,
    разбиваем его на запрос или ответ и записываем в отдельные файлы.
    """
    if packet.haslayer(Raw):
        # обработка ошибок
        try:
            # декодирование байтов в строку
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
        # если возникает ошибка, то просто пропускаем пакет
        except Exception:
            payload = ""

        # Если в пакете обнаруживается HTTP-запрос
        if "GET" in payload or "POST" in payload:
            output = (
                    "=" * 60 + "\n" +
                    "HTTP-запрос:\n" +
                    payload + "\n" +
                    "=" * 60 + "\n\n"
            )
            print(output)
            with open("http_requests.txt", "a", encoding="utf-8") as f:
                f.write(output)

        # Если пакет содержит HTTP-ответ
        elif "HTTP/1.1" in payload or "HTTP/1.0" in payload:
            output = (
                    "=" * 60 + "\n" +
                    "HTTP-ответ:\n" +
                    payload + "\n" +
                    "=" * 60 + "\n\n"
            )
            print(output)
            with open("http_responses.txt", "a", encoding="utf-8") as f:
                f.write(output)


def start_sniffing():
    """
    Запускает перехват трафика на порту 80. При необходимости можно явно указать интерфейс (например, iface="eth0").
    """
    print("Запуск прослушивания HTTP-трафика на порту 8008...")
    # для Windows захват всех пакетов, без указания порта
#    sniff(prn=packet_callback, store=0)
    # указываем интерфейс, иначе не снимает трафик (только для Linux)
    sniff(filter="tcp port 8008", iface="lo", prn=packet_callback, store=0)
    # захват только трафика с порта 8008
#   sniff(filter="tcp port 8008", prn=packet_callback, store=0)



# if __name__ == "__main__": модуль для запуска скрипта
if __name__ == "__main__":
    # Запускаем перехват трафика в отдельном потоке
    sniff_thread = threading.Thread(target=start_sniffing)
    sniff_thread.daemon = True
    sniff_thread.start()

    # Даем время для взаимодействия с сайтом Google Gruyere.
    # Запустите браузер, выполните действия на сайте, затем через нужное время скрипт завершится.
    time_to_listen = 60  # слушаем трафик 60 секунд (поменяйте при необходимости)
    print(f"Прослушивание трафика в течение {time_to_listen} секунд. Выполните действия на Google Gruyere.")
    time.sleep(time_to_listen)

    print("Завершение работы скрипта.")
