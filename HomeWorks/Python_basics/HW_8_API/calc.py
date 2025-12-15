"""
напиши код для калькулятора
"""

first_num = int(input("Введите первое число: "))
second_num = int(input("Введите второе число: "))
operation = input("Введите операцию (+, -, *, /): ")

if operation == "+":
    print(first_num + second_num)
elif operation == "-":
    print(first_num - second_num)
elif operation == "*":
    print(first_num * second_num)
elif operation == "/":
    print(first_num / second_num)
else:
    print("Неверная операция")


