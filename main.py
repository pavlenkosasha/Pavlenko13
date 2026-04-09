
import sys
from functools import wraps

def check_division_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
           print("Помилка: ділення на нуль!")
           sys.exit(1)
    return wrapper



#=======================2=========================

import sys
from functools import wraps
def check_index_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            print("Помилка: індекс виходить за межі списку!")
            sys.exit(1)  # завершення програми
    return wrapper


#=====================3================================================================
@check_division_error
def divide(a,b):
    return a / b

#====================4===================================================================
@check_index_error
def get_element(lst, index):
    return lst[index]

#===========Тести для divide=============================================================
print("=== Тести для divide ===")
print(divide(10, 2))   # нормальний випадок, очікуємо 5.0
print(divide(7, 1))    # нормальний випадок, очікуємо 7.0
#print(divide(5, 0))  # помилка: ділення на нуль (розкоментуй для перевірки)
#В ЦЬОМУ ВИПАДКУ ВИВОДИТЬ ПОМИЛКУ І ЗАВЕРШАЄ ВИКОНАННЯ ПРОГРАМИ ,ТОМУ Я ЗАКОМЕНТУВАВ ,
#ЩОБ ПОДИВИТИСЯ ЯК ТЕСТ ПРАЦЮЄ ДАЛІ ДЛЯ get_element

#===========Тести для get_element========================================================
print("=== \nТести для get_element ===")
lst = [10, 20, 30, 40]

print(get_element(lst, 0))  # нормальний випадок, очікуємо 10
print(get_element(lst, 2))  # нормальний випадок, очікуємо 30
print(get_element(lst, 5))  # помилка: індекс поза межами списку (розкоментуй для перевірки)