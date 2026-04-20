def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i*i <=n:
        if n % i == 0:
            return False
        i += 2     # увеличиваем на 2 , четніе не будут простіми
    return True

def find_primes(start, end):
    result = []
    for i in range(start, end+1):
        if is_prime(i):
            result.append(i)
    return result
print(find_primes(1,10))
print(find_primes(1,20))
print(find_primes(1,30))
print("="*30)




#3
from threading import Thread

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def find_primes_range(start, end, result):
    for n in range(start, end + 1):
        if is_prime(n):
            result.append(n)


def find_primes_multi_thread(start, end):
    mid = (start + end) // 2

    result1 = []
    result2 = []

    t1 = Thread(target=find_primes_range, args=(start, mid, result1))
    t2 = Thread(target=find_primes_range, args=(mid +1 , end, result2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return result1 + result2


print(find_primes_multi_thread(1, 10))
print(find_primes_multi_thread(1, 20))
print(find_primes_multi_thread(1, 30))
print("================Вимірювання часу================")

import time

def measure():
    ranges = [(1, 10000), (1, 20000), (1, 50000)]

    for start, end in ranges:
        print(f"\nДіапазон: {start}-{end}")

        t1 = time.time()
        find_primes(start, end)
        t2 = time.time()

        t3 = time.time()
        find_primes_multi_thread(start, end)
        t4 = time.time()

        print(f"Single thread: {t2 - t1:.4f} сек")
        print(f"Multi thread:  {t4 - t3:.4f} сек")


measure()
# ================= ВИСНОВОК =================
# Маленькі діапазони (наприклад 1–1000):
# Однопотоковий варіант працює швидше,
# оскільки не має витрат на створення та керування потоками.
#
# Середні діапазони:
# Різниця між однопотоковим і багатопотоковим підходами мінімальна
# або однопотоковий варіант залишається трохи швидшим.
#
# Великі діапазони:
# Багатопотоковий підхід у Python не дає значного приросту
# продуктивності через GIL (Global Interpreter Lock).
# У деяких випадках він може працювати навіть повільніше
# за однопотоковий через додаткові витрати на керування потоками.
# ============================================