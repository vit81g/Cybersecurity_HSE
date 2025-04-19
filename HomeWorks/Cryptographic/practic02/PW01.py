import os  # Импортируем модуль os для взаимодействия с операционной системой
import sys  # Импортируем модуль sys для доступа к системным функциям
import random  # Импортируем модуль random для генерации случайных чисел и случайного выбора
import math  # Импортируем модуль math для выполнения математических операций
from typing import Tuple, Optional  # Импортируем аннотации типов Tuple и Optional


def is_prime(n: int, k: int = 5) -> bool:
    """Проверяет, является ли число простым, используя тест Ферма.
    Аргументы: n (int): число для проверки; k (int): количество итераций теста (по умолчанию 5).
    Возвращает: bool: True, если число вероятно простое, False — если составное.
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Проводим k итераций теста Ферма
    for _ in range(k):
        a = random.randint(2, n - 2)
        # Если a^(n-1) ≠ 1 mod n, то n составное
        if pow(a, n - 1, n) != 1:
            return False
    return True

def generate_prime(bits: int) -> int:
    """Генерирует случайное простое число заданной битовой длины.
    Аргументы: bits (int): битовая длина числа.
    Возвращает: int: случайное простое число.
    """
    # Определяем диапазон для чисел заданной длины
    min_val = 1 << (bits - 1)  # 2^(bits-1)
    max_val = (1 << bits) - 1   # 2^bits - 1

    while True:
        n = random.randint(min_val, max_val)
        # Убедимся, что число нечётное
        if n % 2 == 0:
            n += 1
        if is_prime(n):
            return n

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Реализует расширенный алгоритм Евклида для нахождения НОД и коэффициентов.
    Аргументы: a (int): первое число; b (int): Второе число.
    Возвращает: Tuple[int, int, int]: НОД(a, b) и коэффициенты x, y, такие что ax + by = НОД.
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e: int, phi: int) -> Optional[int]:
    """Находит мультипликативное обратное e по модулю phi.
    Аргументы: e (int): число, для которого ищется обратное; phi (int): модуль (функция Эйлера).
    Возвращает: Optional[int]: обратное число или None, если оно не существует.
    """
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        return None  # e и phi не взаимно простые
    return (x % phi + phi) % phi

def generate_keypair(bits: int = 512) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Генерирует пару ключей RSA: открытый (e, n) и закрытый (d, n).
    Аргументы: bits (int): битовая длина модуля n (по умолчанию 512).
    Возвращает: Tuple[Tuple[int, int], Tuple[int, int]]: открытый ключ (e, n) и закрытый ключ (d, n).
    Обработка ошибок: ValueError - если не удалось сгенерировать ключи.
    """
    # Генерируем два простых числа p и q
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)

    # Вычисляем модуль n
    n = p * q

    # Вычисляем функцию Эйлера phi(n)
    phi = (p - 1) * (q - 1)

    # Выбираем открытую экспоненту e
    e = 65537  # Популярное значение, простое и эффективное
    if math.gcd(e, phi) != 1:
        # Если e не взаимно простое с phi, пробуем другое
        for possible_e in range(3, phi, 2):
            if math.gcd(possible_e, phi) == 1:
                e = possible_e
                break
        else:
            raise ValueError("Не удалось найти подходящую открытую экспоненту")

    # Находим закрытую экспоненту d
    d = mod_inverse(e, phi)
    if d is None:
        raise ValueError("Не удалось вычислить закрытую экспоненту")

    return (e, n), (d, n)

def add_padding(data: bytes, block_size: int) -> bytes:
    """Добавляет PKCS#5/PKCS#7 дополнение к данным для кратности блока.
    Аргументы: data (bytes): исходные данные; block_size (int): размер блока в байтах.
    Возвращает: bytes: данные с дополнением.
    """
    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def remove_padding(data: bytes) -> bytes:
    """Удаляет PKCS#5/PKCS#7 дополнение из данных.
    Аргументы: data (bytes): данные с дополнением.
    Возвращает: bytes: данные без дополнения.

    Raises:
        ValueError: Если дополнение некорректно.
    """
    if not data:
        return data
    padding_length = data[-1]
    if padding_length > len(data) or padding_length == 0:
        raise ValueError("Некорректное дополнение")
    if not all(b == padding_length for b in data[-padding_length:]):
        raise ValueError("Некорректное дополнение")
    return data[:-padding_length]

def encrypt_block(message: int, e: int, n: int) -> int:
    """Шифрует один блок сообщения с использованием RSA.
    Аргументы:
        message (int): число, представляющее блок сообщения (меньше n).
        e (int): открытая экспонента.
        n (int): модуль.
    Возвращает: int: зашифрованное число.
    Обработка ошибок: ValueError - если message >= n.
    """
    if message >= n:
        raise ValueError("Сообщение должно быть меньше модуля n")
    # c = m^e mod n
    return pow(message, e, n)

def decrypt_block(ciphertext: int, d: int, n: int) -> int:
    """Расшифровывает один блок шифртекста с использованием RSA.
    Аргументы:
        ciphertext (int): число, представляющее блок шифртекста.
        d (int): акрытая экспонента.
        n (int): модуль.
    Возвращает: int: расшифрованное число.
    Обработка ошибок: ValueError - если ciphertext >= n.
    """
    if ciphertext >= n:
        raise ValueError("Шифртекст должен быть меньше модуля n")
    # m = c^d mod n
    return pow(ciphertext, d, n)

def process_file(input_file: str, output_file: str, key: Tuple[int, int], mode: str = "encrypt") -> None:
    """Обрабатывает файл: шифрует или расшифровывает его поблочно с использованием RSA.
    Аргументы:
        input_file (str): путь к входному файлу.
        output_file (str): путь к выходному файлу.
        key (Tuple[int, int]): ключ (e, n) для шифрования или (d, n) для расшифрования.
        mode (str): режим работы ('encrypt' или 'decrypt').
    Обработка ошибок:
        FileNotFoundError: если входной файл не найден.
        ValueError: если ключ или данные некорректны.
    """
    exp, n = key
    # Определяем размер блока в байтах (чтобы число помещалось в n)
    block_size = (n.bit_length() // 8) - 1  # Минус 1 байт для безопасности

    with open(input_file, 'rb') as f_in:
        data = f_in.read()
        result = b""

        if mode == "encrypt":
            # Добавляем дополнение для шифрования
            data = add_padding(data, block_size)
            # Шифруем поблочно
            for i in range(0, len(data), block_size):
                block = data[i:i + block_size]
                # Преобразуем блок в число
                m = int.from_bytes(block, 'big')
                c = encrypt_block(m, exp, n)
                # Преобразуем шифртекст в байты
                c_bytes = c.to_bytes((n.bit_length() + 7) // 8, 'big')
                result += c_bytes
        else:  # mode == "decrypt"
            # Читаем поблочно, размер блока равен длине n в байтах
            cipher_block_size = (n.bit_length() + 7) // 8
            if len(data) % cipher_block_size != 0:
                raise ValueError("Размер входного файла для расшифровки должен быть кратен размеру блока")
            temp_result = b""
            for i in range(0, len(data), cipher_block_size):
                block = data[i:i + cipher_block_size]
                # Преобразуем блок в число
                c = int.from_bytes(block, 'big')
                m = decrypt_block(c, exp, n)
                # Преобразуем расшифрованное число в байты
                m_bytes = m.to_bytes(block_size, 'big')
                temp_result += m_bytes
            # Удаляем дополнение после расшифровки
            result = remove_padding(temp_result)

        with open(output_file, 'wb') as f_out:
            f_out.write(result)

def print_help() -> None:
    """Выводит инструкцию по использованию программы."""
    print("Программа шифрования/расшифрования с использованием криптосистемы RSA")
    print("-----------------------------------------------------------")
    print("Эта программа реализует асимметричную криптосистему RSA.")
    print("Шифрование и расшифрование выполняются с использованием открытого (e, n) и закрытого (d, n) ключей.")
    print("\nИспользование: python3 rsa_cipher.py [параметры]")
    print("Параметры:")
    print("  -h                Показать эту справку и выйти")
    print("\nИнтерактивный режим:")
    print("1. Запустите программу без параметров: python3 rsa_cipher.py")
    print("2. Выберите действие:")
    print("   - 'generate' для генерации новой ключевой пары.")
    print("   - 'encrypt' для шифрования файла.")
    print("   - 'decrypt' для расшифрования файла.")
    print("3. Следуйте инструкциям на экране:")
    print("   - Для генерации: укажите битовую длину ключей (например, 512).")
    print("   - Для шифрования/расшифрования:")
    print("     - Укажите путь к входному файлу.")
    print("     - Укажите путь к выходному файлу.")
    print("     - Введите ключ (e и n для шифрования, d и n для расшифрования).")
    print("\nПример ключей:")
    print("  Открытый ключ: e=65537, n=12345678901234567890")
    print("  Закрытый ключ: d=98765432109876543210, n=12345678901234567890")
    print("\nПример использования:")
    print("1. Генерация ключей:")
    print("   - Действие: generate")
    print("   - Битовая длина: 512")
    print("2. Шифрование файла plaintext.txt в encrypted.bin:")
    print("   - Действие: encrypt")
    print("   - Входной файл: plaintext.txt")
    print("   - Выходной файл: encrypted.bin")
    print("   - Ключ: e=65537, n=12345678901234567890")
    print("3. Расшифрование файла encrypted.bin в decrypted.txt:")
    print("   - Действие: decrypt")
    print("   - Входной файл: encrypted.bin")
    print("   - Выходной файл: decrypted.txt")
    print("   - Ключ: d=98765432109876543210, n=12345678901234567890")
    print("\nПримечания:")
    print("- Входной файл для шифрования может быть текстовым (UTF-8) или бинарным.")
    print("- Для расшифровки используйте тот же модуль n, что при шифровании.")
    print("- Ключи вводятся как два числа через пробел (например, '65537 12345678901234567890').")
    print("- Результат шифрования — бинарные данные, не открывайте их как текст.")

def main() -> None:
    """Основная функция программы: обрабатывает параметры командной строки и запускает обработку."""
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print_help()
        sys.exit(0)

    print("Программа шифрования/расшифрования с использованием криптосистемы RSA")
    print("-----------------------------------------------------------")

    while True:
        action = input("Выберите действие (generate/encrypt/decrypt): ").strip().lower()
        if action in ["generate", "encrypt", "decrypt"]:
            break
        print("Ошибка: введите 'generate', 'encrypt' или 'decrypt'")

    if action == "generate":
        while True:
            try:
                bits = int(input("Введите битовую длину ключей (например, 512): ").strip())
                if bits < 64:
                    print("Ошибка: битовая длина должна быть не менее 64")
                    continue
                break
            except ValueError:
                print("Ошибка: введите целое число")
        try:
            public_key, private_key = generate_keypair(bits)
            print(f"Открытый ключ: e={public_key[0]}, n={public_key[1]}")
            print(f"Закрытый ключ: d={private_key[0]}, n={private_key[1]}")
        except Exception as e:
            print(f"Ошибка при генерации ключей: {e}")
        return

    while True:
        input_file = input("Введите путь к входному файлу: ").strip()
        if os.path.exists(input_file):
            break
        print("Ошибка: файл не найден")

    output_file = input("Введите путь к выходному файлу: ").strip()

    while True:
        key_input = input(f"Введите ключ ({'e n' if action == 'encrypt' else 'd n'}): ").strip()
        try:
            exp, n = map(int, key_input.split())
            if exp <= 0 or n <= 0:
                raise ValueError("Ключи должны быть положительными числами")
            break
        except ValueError:
            print("Ошибка: введите два числа через пробел (например, '65537 12345678901234567890')")

    try:
        process_file(input_file, output_file, (exp, n), action)
        print(f"Операция завершена! Результат сохранён в {output_file}")
        if action == "decrypt":
            with open(output_file, 'rb') as f:
                decrypted_data = f.read()
                try:
                    decrypted_text = decrypted_data.decode('utf-8')
                    print(f"Расшифрованный текст: {decrypted_text}")
                except UnicodeDecodeError:
                    print("Результат не является текстом в кодировке UTF-8")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# запуск
if __name__ == "__main__":
    main()