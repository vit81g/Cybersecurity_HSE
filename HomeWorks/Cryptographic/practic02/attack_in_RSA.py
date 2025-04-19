import math # Импортируем модуль math для выполнения математических операций
from typing import Tuple, Optional # Импортируем аннотации типов Tuple и Optional

def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Реализует расширенный алгоритм Евклида для нахождения НОД и коэффициентов.
    Аргументы: a (int): первое число; b (int): второе число.
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

def factorize_small_n(n: int) -> Tuple[int, int]:
    """Факторизует маленькое число n на два простых множителя p и q.
    Аргументы: n (int): число для факторизации (предполагается, что n = p * q).
    Возвращает: Tuple[int, int]: пара простых множителей (p, q).
    Обработка ошибок: ValueError: если не удалось найти множители.
    """
    # Проверяем делители до sqrt(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            p = i
            q = n // i
            # Проверяем, что p и q — простые (для простоты)
            if all(p % j != 0 for j in range(2, int(math.sqrt(p)) + 1)) and \
               all(q % j != 0 for j in range(2, int(math.sqrt(q)) + 1)):
                return p, q
    raise ValueError("Не удалось факторизовать n")

def attack_rsa(e: int, n: int, ciphertext: int) -> int:
    """Выполняет атаку на RSA, факторизуя n и восстанавливая закрытый ключ.
    Аргументы:
        e (int): открытая экспонента.
        n (int): модуль (n = p * q).
        ciphertext (int): зашифрованное сообщение.
    Возвращает: int: расшифрованное сообщение.
    Обработка ошибок: ValueError: если атака не удалась (например, не удалось факторизовать n).
    """
    # Шаг 1: Факторизуем n на p и q
    p, q = factorize_small_n(n)
    print(f"Факторизация: n = {n} = {p} * {q}")

    # Шаг 2: Вычисляем phi(n)
    phi = (p - 1) * (q - 1)
    print(f"phi(n) = {phi}")

    # Шаг 3: Находим закрытую экспоненту d
    d = mod_inverse(e, phi)
    if d is None:
        raise ValueError("Не удалось вычислить закрытую экспоненту")
    print(f"Закрытая экспонента: d = {d}")

    # Шаг 4: Расшифровываем шифртекст
    plaintext = pow(ciphertext, d, n)
    print(f"Расшифрованное сообщение (число): {plaintext}")

    return plaintext

def main() -> None:
    """Основная функция: демонстрирует атаку на RSA с малыми числами."""
    print("Демонстрация атаки на RSA с малыми числами")
    print("-----------------------------------------")

    # Пример с малыми числами
    # Открытый ключ: e = 7, n = 77 (p = 7, q = 11)
    # Зашифрованное сообщение: c = 33 (m = 33, символ '!')
    e = 7
    n = 77
    ciphertext = 33

    print(f"Открытый ключ: e = {e}, n = {n}")
    print(f"Шифртекст: c = {ciphertext}")

    try:
        plaintext = attack_rsa(e, n, ciphertext)
        # Пробуем декодировать как текст
        try:
            plaintext_bytes = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big')
            plaintext_text = plaintext_bytes.decode('utf-8')
            print(f"Расшифрованный текст: {plaintext_text}")
        except UnicodeDecodeError:
            print("Расшифрованное сообщение не является текстом UTF-8")
    except Exception as e:
        print(f"Ошибка при атаке: {e}")

# запуск
if __name__ == "__main__":
    main()