import os
import random
from typing import Tuple, Optional
from pygost.gost34112012 import GOST34112012


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """Расширенный алгоритм Евклида для нахождения НОД и коэффициентов.

    Args:
        a (int): Первое число.
        b (int): Второе число.

    Returns:
        Tuple[int, int, int]: НОД(a, b) и коэффициенты x, y, такие что ax + by = НОД.
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a: int, m: int) -> Optional[int]:
    """Находит мультипликативное обратное a по модулю m.

    Args:
        a (int): Число, для которого ищется обратное.
        m (int): Модуль.

    Returns:
        Optional[int]: Обратное число или None, если оно не существует.
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m


class EllipticCurve:
    """Класс для работы с эллиптической кривой y^2 = x^3 + ax + b (mod p)."""

    def __init__(self, a: int, b: int, p: int):
        """Инициализация кривой.

        Args:
            a (int): Коэффициент a в уравнении кривой.
            b (int): Коэффициент b в уравнении кривой.
            p (int): Модуль поля.
        """
        self.a = a
        self.b = b
        self.p = p

    def add_points(self, P: Optional[Tuple[int, int]], Q: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """Сложение двух точек на эллиптической кривой.

        Args:
            P (Optional[Tuple[int, int]]): Первая точка (x1, y1) или None (бесконечная точка).
            Q (Optional[Tuple[int, int]]): Вторая точка (x2, y2) или None (бесконечная точка).

        Returns:
            Optional[Tuple[int, int]]: Сумма точек или None (бесконечная точка).
        """
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and y1 == (-y2 % self.p):
            return None  # Сумма даёт бесконечно удалённую точку
        if P == Q:
            # Удвоение точки
            if y1 == 0:
                return None
            lam = ((3 * x1 * x1 + self.a) * mod_inverse(2 * y1, self.p)) % self.p
        else:
            # Сложение разных точек
            if x1 == x2:
                return None
            lam = ((y2 - y1) * mod_inverse(x2 - x1, self.p)) % self.p
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return x3, y3

    def multiply_point(self, P: Tuple[int, int], k: int) -> Optional[Tuple[int, int]]:
        """Умножение точки на скаляр k.

        Args:
            P (Tuple[int, int]): Точка (x, y).
            k (int): Скаляр.

        Returns:
            Optional[Tuple[int, int]]: k * P или None (бесконечная точка).
        """
        result = None
        temp = P
        while k:
            if k & 1:
                result = self.add_points(result, temp)
            temp = self.add_points(temp, temp)
            k >>= 1
        return result


def hash_message(message: bytes) -> int:
    """Хэширование сообщения с использованием ГОСТ Р 34.11-2012.

    Args:
        message (bytes): Входное сообщение.

    Returns:
        int: Хэш, преобразованный в целое число (первые 32 бита).
    """
    h = GOST34112012(message).digest()
    return int.from_bytes(h[:4], 'big')  # Берём первые 32 бита для упрощения


def generate_keypair(curve: EllipticCurve, G: Tuple[int, int], q: int) -> Tuple[int, Tuple[int, int]]:
    """Генерация ключевой пары: закрытый ключ d, открытый ключ Q.

    Args:
        curve (EllipticCurve): Эллиптическая кривая.
        G (Tuple[int, int]): Базовая точка.
        q (int): Порядок подгруппы.

    Returns:
        Tuple[int, Tuple[int, int]]: Закрытый ключ d и открытый ключ Q = d * G.
    """
    d = random.randint(1, q - 1)  # Закрытый ключ
    Q = curve.multiply_point(G, d)  # Открытый ключ
    if Q is None:
        raise ValueError("Ошибка генерации ключа: Q является бесконечной точкой")
    return d, Q


def sign_message(message: bytes, curve: EllipticCurve, G: Tuple[int, int], q: int, d: int) -> Tuple[int, int]:
    """Формирование подписи для сообщения по ГОСТ Р 34.10-2012.

    Args:
        message (bytes): Сообщение для подписи.
        curve (EllipticCurve): Эллиптическая кривая.
        G (Tuple[int, int]): Базовая точка.
        q (int): Порядок подгруппы.
        d (int): Закрытый ключ.

    Returns:
        Tuple[int, int]: Подпись (r, s).

    Raises:
        ValueError: Если не удалось сформировать подпись.
    """
    h = hash_message(message)
    e = h % q
    if e == 0:
        e = 1
    while True:
        k = random.randint(1, q - 1)
        R = curve.multiply_point(G, k)
        if R is None:
            continue
        r = R[0] % q
        if r == 0:
            continue
        s = (r * d + k * e) % q
        if s == 0:
            continue
        return r, s


def verify_signature(message: bytes, signature: Tuple[int, int], curve: EllipticCurve, G: Tuple[int, int], q: int,
                     Q: Tuple[int, int]) -> bool:
    """Проверка подписи для сообщения по ГОСТ Р 34.10-2012.

    Args:
        message (bytes): Сообщение.
        signature (Tuple[int, int]): Подпись (r, s).
        curve (EllipticCurve): Эллиптическая кривая.
        G (Tuple[int, int]): Базовая точка.
        q (int): Порядок подгруппы.
        Q (Tuple[int, int]): Открытый ключ.

    Returns:
        bool: True, если подпись верна, иначе False.
    """
    r, s = signature
    if not (0 < r < q and 0 < s < q):
        return False
    h = hash_message(message)
    e = h % q
    if e == 0:
        e = 1
    v = mod_inverse(s, q)
    if v is None:
        return False
    z1 = (e * v) % q
    z2 = (r * v) % q
    R = curve.add_points(curve.multiply_point(G, z1), curve.multiply_point(Q, z2))
    if R is None:
        return False
    return (R[0] % q) == r


def process_file(input_file: str, output_file: str, curve: EllipticCurve, G: Tuple[int, int], q: int,
                 key: Tuple[int, Tuple[int, int]], mode: str = "sign") -> None:
    """Обработка файла: подпись или проверка.

    Args:
        input_file (str): Путь к файлу сообщения.
        output_file (str): Путь к файлу подписи.
        curve (EllipticCurve): Эллиптическая кривая.
        G (Tuple[int, int]): Базовая точка.
        q (int): Порядок подгруппы.
        key (Tuple[int, Tuple[int, int]]): Ключ (d, Q) для подписи или (0, Q) для проверки.
        mode (str): Режим ("sign" или "verify").

    Raises:
        FileNotFoundError: Если входной файл не найден.
        ValueError: Если подпись некорректна.
    """
    with open(input_file, 'rb') as f:
        message = f.read()
    if mode == "sign":
        d, _ = key
        r, s = sign_message(message, curve, G, q, d)
        with open(output_file, 'w') as f:
            f.write(f"{r} {s}")
    else:
        with open(output_file, 'r') as f:
            r, s = map(int, f.read().split())
        _, Q = key
        result = verify_signature(message, (r, s), curve, G, q, Q)
        with open("verify_result.txt", 'w') as f:
            f.write("Подпись верна" if result else "Подпись неверна")


def main() -> None:
    """Основная функция: интерфейс для генерации ключей, подписи и проверки."""
    # Параметры эллиптической кривой (демонстрационные, малое поле)
    p = 17  # Модуль поля
    a, b = 2, 2  # y^2 = x^3 + 2x + 2 (mod 17)
    curve = EllipticCurve(a, b, p)
    G = (5, 1)  # Базовая точка
    q = 19  # Порядок подгруппы
    print("Программа электронной подписи по ГОСТ Р 34.10-2012")
    print("-------------------------------------------------")
    while True:
        action = input("Выберите действие (generate/sign/verify): ").strip().lower()
        if action in ["generate", "sign", "verify"]:
            break
        print("Ошибка: введите 'generate', 'sign' или 'verify'")
    try:
        if action == "generate":
            d, Q = generate_keypair(curve, G, q)
            print(f"Закрытый ключ (d): {d}")
            print(f"Открытый ключ (Q): {Q}")
            return
        input_file = input("Введите путь к файлу сообщения: ").strip()
        if not os.path.exists(input_file):
            raise FileNotFoundError("Файл сообщения не найден")
        output_file = input("Введите путь к файлу подписи: ").strip()
        if action == "sign":
            d = int(input("Введите закрытый ключ d: "))
            Q_input = input("Введите открытый ключ Q (x y): ").strip()
            Q = tuple(map(int, Q_input.split()))
            process_file(input_file, output_file, curve, G, q, (d, Q), "sign")
            print(f"Подпись сохранена в {output_file}")
        else:
            Q_input = input("Введите открытый ключ Q (x y): ").strip()
            Q = tuple(map(int, Q_input.split()))
            process_file(input_file, output_file, curve, G, q, (0, Q), "verify")
            with open("verify_result.txt", 'r') as f:
                print(f"Результат проверки: {f.read()}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()