# -*- coding: utf-8 -*-
"""
Подробная реализация схемы электронной цифровой подписи по стандарту ГОСТ Р 34.10-2012
на языке Python. Допускается использование готовой реализации хэш-функции ГОСТ Р 34.11-2012
или другой подходящей.
"""
import os # Импортируем модуль os для взаимодействия с операционной системой
import random # Импортируем модуль random для генерации случайных чисел и случайного выбора
import hashlib # Библиотека hashlib из стандартной библиотеки Python была выбрана для реализации хэш-функции в скрипте
from typing import Tuple, Optional # Импортируем аннотации типов Tuple и Optional


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Расширенный алгоритм Евклида для вычисления НОД и коэффициентов Безу.
    Вычисляет gcd(a, b) и находит x, y такие, что a * x + b * y = gcd(a, b)
    Аргументы: a (int): первое целое число; b (int): второе целое число.
    Возвращает:
        Tuple[int, int, int]:
            gcd (int): наибольший общий делитель a и b
            x (int): коэффициент при a в уравнении Безу.
            y (int): коэффициент при b в уравнении Безу.
    """
    if a == 0:
        # азовый случай: gcd(0, b) = b; 0*x + 1*b = b
        return b, 0, 1
    # рекурсивный вызов: gcd(b mod a, a)
    gcd, x1, y1 = extended_gcd(b % a, a)
    # переход к исходным коэффициентам x, y
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a: int, m: int) -> Optional[int]:
    """
    Вычисление мультипликативного обратного элемента a по модулю m.
    Ищет x такое, что a * x ≡ 1 (mod m).
    Аргументы: a (int): число, для которого ищем обратное; m (int): модуль.
    Возвращает: int или None: обратное a^{-1} mod m, либо None, если gcd(a, m) ≠ 1
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        # обратного не существует
        return None
    # нормализуем в диапазон [0, m-1]
    return x % m


class EllipticCurve:
    """
    Класс для работы с эллиптической кривой над конечным полем F_p.
    Уравнение: y^2 = x^3 + a*x + b (mod p)
    """

    def __init__(self, a: int, b: int, p: int):
        """
        Инициализация параметров кривой.
        Аргументы:
            a (int): коэффициент a в уравнении кривой.
            b (int): коэффициент b в уравнении кривой.
            p (int): простое основание конечного поля F_p.
        """
        self.a = a
        self.b = b
        self.p = p

    def is_point_on_curve(self, P: Tuple[int, int]) -> bool:
        """
        Проверяет, лежит ли точка P = (x, y) на кривой.
        Возвращает True, если y^2 mod p == (x^3 + a*x + b) mod p
        """
        x, y = P
        left = (y * y) % self.p
        right = (x * x * x + self.a * x + self.b) % self.p
        return left == right

    def add_points(self,
                   P: Optional[Tuple[int, int]],
                   Q: Optional[Tuple[int, int]]
                   ) -> Optional[Tuple[int, int]]:
        """
        Сложение двух точек P и Q на эллиптической кривой.
        Реализованы все случаи:
        - P = None или Q = None (точка на бесконечности)
        - P == Q (удвоение точки)
        - P == -Q (результат — точка на бесконечности)
        - обычное сложение разных точек
        Аргументы: P, Q: координаты точек или None
        Возвращает: новую точку на кривой или None (точка на бесконечности)
        """
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        # P + (-P) = бесконечность
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        if P == Q:
            # удвоение точки P
            if y1 == 0:
                # касательная вертикальна => бесконечность
                return None
            # вычисляем λ = (3*x1^2 + a) / (2*y1) mod p
            inv = mod_inverse((2 * y1) % self.p, self.p)
            if inv is None:
                return None
            lam = ((3 * x1 * x1 + self.a) * inv) % self.p
        else:
            # сложение P и Q, P != Q
            denom = (x2 - x1) % self.p
            inv = mod_inverse(denom, self.p)
            if inv is None:
                return None
            lam = ((y2 - y1) * inv) % self.p

        # координаты результирующей точки R = (x3, y3)
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return x3, y3

    def multiply_point(self, P: Tuple[int, int], k: int) -> Optional[Tuple[int, int]]:
        """
        Умножение точки P на скаляр k методом двойного и сложения.
        Алгоритм двоичного разложения k:
        - инициализируем R = None (0·P)
        - для каждого бита k, если бит=1, R = R + P
        - P = 2P при каждом шаге
        Аргументы:
            P (Tuple[int,int]): исходная точка на кривой
            k (int): скалярный множитель
        Возвращает: k·P как точку на кривой или None
        """
        result: Optional[Tuple[int, int]] = None  # накопитель
        addend = P
        while k > 0:
            if k & 1:
                result = self.add_points(result, addend)
            addend = self.add_points(addend, addend)
            k >>= 1
        return result


def hash_message(message: bytes) -> int:
    """
    Хэширует сообщение в целое число.
    Здесь для примера используется SHA-256 из hashlib.
    В реальной системе рекомендуется ГОСТ Р 34.11-2012, но проблема с установкой в Windows.
    Аргументы: message (bytes): данные для хэширования
    Возвращает: int: целочисленное представление хэша (big-endian)
    """
    digest = hashlib.sha256(message).digest()
    return int.from_bytes(digest, 'big')


def generate_keypair(curve: EllipticCurve,
                     G: Tuple[int, int],
                     q: int
                     ) -> Tuple[int, Tuple[int, int]]:
    """
    Генерация ключевой пары (секретного и публичного ключей).
    Процесс:
    1. Выбираем случайный d ∈ [1, q-1]
    2. Вычисляем Q = d·G
    3. Проверяем, что Q лежит на кривой и Q ≠ ∞
    4. Возвращаем (d, Q)
    Аргументы:
        curve (EllipticCurve): параметры кривой
        G (Tuple[int,int]): базовая точка порядка q
        q (int): порядок подгруппы
    Возвращает:
        Tuple[int, Tuple[int,int]]:
            d (int): секретный ключ
            Q (Tuple[int,int]): публичный ключ
    """
    while True:
        d = random.randrange(1, q)
        Q = curve.multiply_point(G, d)
        if Q is not None and curve.is_point_on_curve(Q):
            return d, Q


def sign_message(message: bytes,
                 curve: EllipticCurve,
                 G: Tuple[int, int],
                 q: int,
                 d: int
                 ) -> Tuple[int, int]:
    """
    Формирование ЭЦП (r, s) по ГОСТ Р 34.10-2012.
    Алгоритм:
    1. h = H(message), e = h mod q (если e=0, e=1)
    2. выбираем случайный k ∈ [1, q-1]
    3. вычисляем P = k·G
    4. r = P.x mod q (если r=0 — повторяем с новым k)
    5. s = (r*d + k*e) mod q (если s=0 — повторяем)
    Аргументы:
        message (bytes): данные для подписи.
        curve (EllipticCurve): параметры кривой.
        G (Tuple[int,int]): базовая точка.
        q (int): порядок подгруппы.
        d (int): секретный ключ.
    Возвращает: Tuple[int,int]: подпись (r, s)
    """
    h = hash_message(message)
    e = h % q
    if e == 0:
        e = 1

    while True:
        k = random.randrange(1, q)
        P = curve.multiply_point(G, k)
        if P is None:
            continue
        r = P[0] % q
        if r == 0:
            continue
        s = (r * d + k * e) % q
        if s == 0:
            continue
        return r, s


def verify_signature(message: bytes,
                     signature: Tuple[int, int],
                     curve: EllipticCurve,
                     G: Tuple[int, int],
                     q: int,
                     Q: Tuple[int, int]
                     ) -> bool:
    """
    Проверка ЭЦП по ГОСТ Р 34.10-2012.
    Шаги проверки:
    1. Проверяем диапазон: 0 < r, s < q
    2. Проверяем, лежит ли Q (публичный ключ) на кривой
    3. Вычисляем h = H(message), e = h mod q (если e=0, e=1)
    4. Вычисляем обратное v = e^{-1} mod q
    5. Вычисляем z1 = s·v mod q и z2 = (-r)·v mod q
    6. Строим точку C = z1·G + z2·Q
    7. Подпись считается валидной, если C ≠ ∞ и (C.x mod q) == r
    Аргументы:
        message (bytes): подписанные данные.
        signature (Tuple[int,int]): полученная подпись (r, s)
        curve (EllipticCurve): параметры кривой.
        G (Tuple[int,int]): базовая точка.
        q (int): порядок подгруппы.
        Q (Tuple[int,int]): публичный ключ.
    Возвращает: bool: True, если подпись верна, иначе False
    """
    r, s = signature
    # 1. проверяем корректность r и s
    if not (0 < r < q and 0 < s < q):
        return False

    # 2. убеждаемся, что Q лежит на кривой
    if not curve.is_point_on_curve(Q):
        return False

    # 3. хэшируем сообщение
    h = hash_message(message)
    e = h % q
    if e == 0:
        e = 1

    # 4. обратное e по модулю q
    v = mod_inverse(e, q)
    if v is None:
        return False

    # 5. вычисляем вспомогательные множители
    z1 = (s * v) % q
    z2 = (-r * v) % q

    # 6. C = z1·G + z2·Q
    P1 = curve.multiply_point(G, z1)
    P2 = curve.multiply_point(Q, z2)
    C = curve.add_points(P1, P2)

    # 7. проверяем соответствие координаты
    if C is None:
        return False
    return (C[0] % q) == r


def process_file(input_file: str,
                 output_file: str,
                 curve: EllipticCurve,
                 G: Tuple[int, int],
                 q: int,
                 key: Tuple[int, Tuple[int, int]],
                 mode: str = "sign"
                 ) -> None:
    """
    Упрощённый интерфейс для подписи и проверки файловой подписи.
    Аргументы:
        input_file (str): путь к файлу с исходным сообщением.
        output_file (str): путь к файлу подписи (для sign) или к выводу результатов проверки.
        curve, G, q: параметры эллиптической кривой.
        key: для mode="sign" — (d, _), для mode="verify" — (_, Q)
        mode (str): "sign" или "verify"
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Не найден файл сообщения: {input_file}")
    with open(input_file, "rb") as f:
        msg = f.read()

    if mode == "sign":
        d, _ = key
        # создаём подпись и сохраняем r и s в output_file
        r, s = sign_message(msg, curve, G, q, d)
        with open(output_file, "w") as f:
            f.write(f"{r} {s}")
    else:
        # проверяем существование файла подписи
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"Не найден файл подписи: {output_file}")
        with open(output_file, "r") as f:
            r_str, s_str = f.read().split()
            r, s = int(r_str), int(s_str)
        _, Q = key
        # выполняем проверку и записываем результат в verify_result.txt
        ok = verify_signature(msg, (r, s), curve, G, q, Q)
        with open("verify_result.txt", "w", encoding="utf-8") as f:
            f.write("Подпись верна" if ok else "Подпись неверна")


def main() -> None:
    """
    Основная функция: интерактивный CLI для генерации ключей, подписи и проверки.
    Пользователь по шагам выбирает операцию и вводит необходимые параметры.
    """
    # --- Пример параметров для тестов (малое поле) ---
    p = 17  # простое
    a, b = 2, 2
    curve = EllipticCurve(a, b, p)
    G = (5, 1)
    q = 19
    # -----------------------------------------------

    print("ГОСТ Р 34.10-2012: электронная подпись на Python")
    while True:
        mode = input("Выберите операцию (generate/sign/verify): ").strip().lower()
        if mode in {"generate", "sign", "verify"}:
            break

    if mode == "generate":
        # генерация новой пары ключей
        d, Q = generate_keypair(curve, G, q)
        print(f"Секретный ключ d = {d}")
        print(f"Публичный ключ Q = {Q}")
        return

    msg_file = input("Путь к файлу сообщения: ").strip()
    sig_file = input("Путь к файлу подписи:   ").strip()

    if mode == "sign":
        d = int(input("Введите секретный ключ d: ").strip())
        process_file(msg_file, sig_file, curve, G, q, (d, None), "sign")
        print("Подпись успешно сформирована.")
    else:
        x, y = map(int, input("Введите публичный ключ Q (x y): ").split())
        process_file(msg_file, sig_file, curve, G, q, (0, (x, y)), "verify")
        with open("verify_result.txt", encoding="utf-8") as f:
            print("Результат проверки:", f.read())

# запуск
if __name__ == "__main__":
    main()
