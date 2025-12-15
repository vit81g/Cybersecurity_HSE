"""
Этап 4. Анализ результатов
● Используя Scapy, проанализируйте, как XSS-атака отображается в сетевом трафике (проанализируйте ответ на HTTP-запрос).
● Опишите, какие изменения в трафике произошли во время XSS-атаки.
"""

#!/usr/bin/env python3
# импорт библиотек
import threading
from scapy.all import sniff, TCP, Raw


def packet_callback(packet):
    """
    Функция для обработки перехваченных пакетов:
      - Если пакет содержит Raw-данные, декодируем их.
      - Если payload начинается с "HTTP/", считаем его ответом,
        разделяем на заголовки и тело, и ищем в теле XSS-пейлоад.
      - Если payload содержит "GET" или "POST", считаем это запросом.
      - Остальные пакеты (если нужны) можно записывать в debug-файл.
    """
    if packet.haslayer(Raw):
        # обработка ошибок и декодирование байтов в строку
        try:
            payload = packet[Raw].load.decode('utf-8', errors='ignore')
        # если возникает ошибка, то просто пропускаем пакет
        except Exception as e:
            payload = ""
            print("Ошибка декодирования:", e)

        if payload.startswith("HTTP/"):
            # Разделим заголовки и тело (используем разделитель CRLFCRLF)
            parts = payload.split("\r\n\r\n", 1)
            headers = parts[0]
            body = parts[1] if len(parts) > 1 else ""

            # Простейшая проверка на наличие XSS-пейлоада в теле
            if "<script>alert(" in body:
                analysis = "XSS найден в теле ответа!"
            else:
                analysis = "XSS-пейлоад не обнаружен в теле ответа."

            output = (
                    "=" * 60 + "\n" +
                    "HTTP Response Analysis:\n" +
                    headers + "\n\n" +
                    "Тело (первые 200 символов):\n" + body[:200] + "\n\n" +
                    "Анализ: " + analysis + "\n" +
                    "=" * 60 + "\n\n"
            )
            print(output)
            with open("http_responses.txt", "a", encoding="utf-8") as f:
                f.write(output)

        # Если это запрос (ищем GET или POST)
        elif "GET" in payload or "POST" in payload:
            output = (
                    "=" * 60 + "\n" +
                    "HTTP Request:\n" +
                    payload + "\n" +
                    "=" * 60 + "\n\n"
            )
            print(output)
            with open("http_requests.txt", "a", encoding="utf-8") as f:
                f.write(output)

        # Остальные пакеты (если нужно, можно записывать в debug)
        else:
            with open("debug_payloads.txt", "a", encoding="utf-8") as f:
                f.write(payload + "\n" + "=" * 40 + "\n")


def start_sniffing():
    print("Запуск перехвата трафика на порту 8008 через loopback-интерфейс (lo)...")
    sniff(filter="tcp port 8008", iface="lo", prn=packet_callback, store=0)


if __name__ == "__main__":
    # Можно запускать перехват в отдельном потоке, если нужно выполнять параллельные задачи.
    sniff_thread = threading.Thread(target=start_sniffing)
    sniff_thread.daemon = True
    sniff_thread.start()

    # Оставляем основной поток активным (например, на 60 секунд), чтобы успеть собрать данные.
    import time

    time_to_listen = 60  # можно изменить при необходимости
    print(f"Перехват трафика запущен на {time_to_listen} секунд...")
    time.sleep(time_to_listen)
    print("Завершение работы скрипта.")
