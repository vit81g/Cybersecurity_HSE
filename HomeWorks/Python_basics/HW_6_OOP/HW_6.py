"""
Задание
Нужно реализовать класс Account, который отражает абстракцию базового
поведения банковского аккаунта:
● создать банковский аккаунт с параметрами: имя; стартовый баланс с
которым зарегистрирован аккаунт; история операций*;
● реализовать два метода, которые позволяют положить деньги на счёт
или снять деньги со счёта;
● продумать, как можно хранить историю поступления или снятия
денег, чтобы с ней было удобно работать*.
*Задачи повышенной сложности на 9 и 10 баллов
"""

# Класс Account
class Account:
    # Инициализация банковского аккаунта с параметрами name и balance
    def __init__(self, name, balance=1000):
        """
        Инициализация банковского аккаунта.
        :param name: Имя владельца аккаунта.
        :param balance: Стартовый баланс.
        """
        # Создание атрибутов name и balance, а transaction_history и add_transaction
        self.name = name
        self.balance = balance
        self.transaction_history = []  # Список для хранения истории операций
        self.add_transaction("Создан счет", balance)

    # Метод для внесения денег на счёт "Зачсисление"
    def deposit(self, amount):
        """
        Метод для внесения денег на счёт.
        :param amount: Сумма, которую нужно положить.
        """
        # Проверка, что сумма больше нуля
        if amount <= 0:
            # Вывод сообщения об ошибке и вывод исключения
            raise ValueError("Сумма для внесения должна быть больше нуля.")
        self.balance += amount
        self.add_transaction("Зачисление", amount)

    # Метод для снятия денег со счёта "Вывод средств"
    def withdraw(self, amount):
        """
        Метод для снятия денег со счёта.
        :param amount: Сумма, которую нужно снять.
        """
        # Проверка, что сумма больше нуля и что на счету достаточно денег
        if amount <= 0:
            # Вывод сообщения об ошибке и вывод исключения
            raise ValueError("Сумма для снятия должна быть больше нуля.")
        if amount > self.balance:
            # Вывод сообщения об ошибке и вывод исключения
            raise ValueError("Недостаточно средств на счёте.")
        self.balance -= amount
        self.add_transaction("Вывод средств", -amount)

    def add_transaction(self, transaction_type, amount):
        """
        Метод для добавления записи в историю операций.
        :param transaction_type: Тип операции (например, 'Зачисление', 'Вывод').
        :param amount: Сумма операции.
        """
        # импорт модуля datetime из библиотеки datetime
        from datetime import datetime

        # создание словаря с информацией о транзакции с описанием типа операции, суммой, датой и балансом
        transaction = {
            "Тип операции": transaction_type,
            "Сумма": amount,
            "Дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Баланс": self.balance
        }
        self.transaction_history.append(transaction)

    # Метод для получения истории операций
    def get_transaction_history(self):
        """
        Метод для получения истории операций.
        :return: История операций в виде списка словарей.
        """
        # Возврат списка истории операций
        return self.transaction_history

    # Метод для представления объекта в виде строки
    def __str__(self):
        """
        Представление объекта в виде строки.
        """
        return f"Account(name={self.name}, balance={self.balance})"

def print_transaction():
    for transaction in account.transaction_history:
        print(transaction)

# Пример использования
account = Account("Иванов Иван", 1000)
print(account)
print_transaction()
#print(account.transaction_history[0])

# Операции
account.deposit(500)
print(account)
print_transaction()

account.withdraw(300)
print(account)
print_transaction()

# История операций
# вывод типа account.get_transaction_history()
# print(type(account.get_transaction_history()))
#print(account.get_transaction_history())
# цикл for вывода истории, путем перебора списка account.get_transaction_history и вывода значения каждого элемента
#for transaction in account.get_transaction_history():
#    print(transaction)
