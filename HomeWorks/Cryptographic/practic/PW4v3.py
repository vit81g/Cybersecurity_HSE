import os  # Импортируем модуль os для работы с файловой системой
import sys  # Импортируем модуль sys для работы с аргументами командной строки
import secrets  # Импортируем модуль secrets для генерации случайного ключа
from typing import List  # Импортируем List для аннотаций типов

# Фиксированная таблица замен (S-box) из ГОСТ Р 34.12-2015, Приложение А
SBOX: List[List[int]] = [
    [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
    [6, 8, 2, 3, 9, 10, 5, 12, 1, 11, 7, 13, 0, 4, 15, 14],
    [7, 11, 5, 8, 12, 4, 2, 0, 14, 1, 3, 10, 9, 15, 6, 13],
    [13, 1, 7, 4, 11, 5, 0, 15, 3, 12, 14, 6, 9, 10, 2, 8],
    [5, 10, 15, 12, 1, 13, 14, 11, 8, 3, 6, 0, 4, 7, 9, 2],
    [14, 5, 0, 15, 13, 11, 3, 6, 9, 2, 12, 7, 1, 8, 10, 4],
    [11, 13, 12, 3, 7, 14, 10, 5, 0, 9, 4, 15, 2, 8, 1, 6],
    [15, 12, 9, 7, 3, 0, 11, 4, 1, 14, 2, 13, 6, 10, 8, 5]
]


def generate_round_keys(key: bytes) -> List[int]:
    """Генерирует 32 раундовых ключа из 256-битного исходного ключа для шифра Магма.
    Args: key (bytes): Исходный ключ длиной 256 бит (32 байта).
    Returns: List[int]: Список из 32 раундовых ключей, каждый по 32 бита.
    Raises: ValueError: Если длина ключа не равна 32 байтам.
    """
    # проверяем длину ключа
    if len(key) != 32:
        raise ValueError("Ключ должен быть длиной 256 бит (32 байта)")
    round_keys: List[int] = []
    # Генерируем 32 раундовых ключей
    for i in range(0, 32, 4):
        chunk: bytes = key[i:i + 4]
        k: int = int.from_bytes(chunk, 'big')
        round_keys.append(k)
    schedule: List[int] = round_keys * 3 + round_keys[::-1]
    return schedule


def G(a: int, k: int) -> int:
    """Выполняет преобразование G в сети Фейстеля для шифра Магма.
    Args:
        a (int): Правая часть блока (32 бита).
        k (int): Раундовый ключ (32 бита).
    Returns: int: Результат преобразования (32 бита).
    """
    t: int = (a + k) % (2 ** 32)
    left_shift: int = t << 11
    right_shift: int = t >> 21
    t = (left_shift | right_shift) & 0xFFFFFFFF
    result: int = 0
    # Применяем таблицу замен SBOX
    for i in range(8):
        nibble: int = (t >> (4 * i)) & 0xF
        subst: int = SBOX[i][nibble]
        result |= (subst << (4 * i))
    return result


def encrypt_block(block: bytes, round_keys: List[int]) -> bytes:
    """Шифрует один 64-битовый блок данных с использованием шифра Магма.
    Args:
        block (bytes): Входной блок длиной 64 бита (8 байт).
        round_keys (List[int]): Список из 32 раундовых ключей.
    Returns: bytes: Зашифрованный блок (8 байт).
    Raises: ValueError: Если длина блока не равна 8 байтам.
    """
    # проверяем длину блока
    if len(block) != 8:
        raise ValueError("Блок должен быть длиной 64 бита (8 байт)")
    L: int = int.from_bytes(block[:4], 'big')
    R: int = int.from_bytes(block[4:], 'big')
    # 32 раунда сети Фейстеля, каждый с использованием раундового ключа
    for i in range(32):
        old_R: int = R
        R = L ^ G(R, round_keys[i])
        L = old_R
    encrypted: bytes = R.to_bytes(4, 'big') + L.to_bytes(4, 'big')
    # возвращаем зашифрованный блок
    return encrypted


def decrypt_block(block: bytes, round_keys: List[int]) -> bytes:
    """Расшифровывает один 64-битовый блок данных с использованием шифра Магма.
    Args:
        block (bytes): Входной блок длиной 64 бита (8 байт).
        round_keys (List[int]): Список из 32 раундовых ключей.
    Returns: bytes: Расшифрованный блок (8 байт).
    Raises: ValueError: Если длина блока не равна 8 байтам.
    """
    # проверяем длину блока
    if len(block) != 8:
        raise ValueError("Блок должен быть длиной 64 бита (8 байт)")
    L: int = int.from_bytes(block[:4], 'big')
    R: int = int.from_bytes(block[4:], 'big')
    # 32 раунда в обратном порядке
    for i in range(31, -1, -1):
        old_R: int = R
        R = L ^ G(R, round_keys[i])
        L = old_R
    decrypted: bytes = R.to_bytes(4, 'big') + L.to_bytes(4, 'big')
    # возврат расшифрованного блока
    return decrypted


def process_file(input_file: str, output_file: str, key: bytes, mode: str = "encrypt") -> None:
    """Обрабатывает файл: шифрует или расшифровывает его поблочно.
    Args:
        input_file (str): Путь к входному файлу.
        output_file (str): Путь к выходному файлу.
        key (bytes): Ключ шифрования (256 бит).
        mode (str, optional): Режим работы ('encrypt' или 'decrypt'). Defaults to "encrypt".
    Raises: FileNotFoundError: Если входной файл не найден.
    """
    round_keys: List[int] = generate_round_keys(key)
    with open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            # цикл для чтения файла поблочно
            while True:
                block: bytes = f_in.read(8)
                # если данных нет, выходим
                if not block:
                    break
                # если блок меньше 8 байт (последний блок), дополняем нулями
                if len(block) < 8:
                    block += b'\x00' * (8 - len(block))
                # выбираем режим работы
                if mode == "encrypt":
                    result: bytes = encrypt_block(block, round_keys)
                # расшифровываем
                else:
                    result: bytes = decrypt_block(block, round_keys)
                f_out.write(result)


def print_help() -> None:
    """Выводит инструкцию по использованию программы."""
    print("Программа шифрования/расшифрования с использованием шифра Магма")
    print("-----------------------------------------------------------")
    print("Использование: python3 script.py [параметры]")
    print("Параметры:")
    print("  -h                Показать эту справку и выйти")
    print("\nИнтерактивный режим:")
    print("1. Запустите программу без параметров: python3 script.py")
    print("2. Следуйте инструкциям на экране:")
    print("   - Выберите режим (encrypt/decrypt)")
    print("   - Укажите путь к входному файлу")
    print("   - Укажите путь к выходному файлу")
    print("   - Введите ключ шифрования (256 бит в формате hex, 64 символа)")
    print("\nПример ключа: ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff")


def main() -> None:
    """Основная функция программы: обрабатывает параметры командной строки и запускает обработку."""
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        print_help()
        sys.exit(0)

    print("Программа шифрования/расшифрования с использованием шифра Магма")
    print("-----------------------------------------------------------")
    # цикл выбора режима
    while True:
        mode: str = input("Выберите режим (encrypt/decrypt): ").strip().lower()
        if mode in ["encrypt", "decrypt"]:
            break
        print("Ошибка: введите 'encrypt' или 'decrypt'")
    # цикл обработки файлов
    while True:
        input_file: str = input("Введите путь к входному файлу: ").strip()
        if os.path.exists(input_file):
            break
        print("Ошибка: файл не найден")

    output_file: str = input("Введите путь к выходному файлу: ").strip()

    # генерация случайного ключа
    while True:
        random_key: str = secrets.token_hex(32)
        print(f"Пример случайного ключа: {random_key}")
        key_hex: str = input("Введите ключ (256 бит в hex, 64 символа): ").strip()
        # проверка длины ключа, обработка ошибок
        try:
            key: bytes = bytes.fromhex(key_hex)
            if len(key) == 32:
                break
            print("Ошибка: ключ должен быть длиной 256 бит (64 символа в hex)")
        except ValueError:
            print("Ошибка: неверный формат hex-строки")
    # обработка ошибок
    try:
        process_file(input_file, output_file, key, mode)
        print(f"Операция завершена! Результат сохранён в {output_file}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск программы
if __name__ == "__main__":
    main()