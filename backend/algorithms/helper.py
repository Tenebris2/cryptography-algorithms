from sympy import randprime
from sympy import isprime, factorint
from sympy import prime
import random


def generate_prime(digit_bound):
    upper_bound = 2  # Smallest 6-digit number
    lower_bound = digit_bound
    prime_number = randprime(lower_bound, upper_bound)
    return prime_number


def generate_n_bit_prime(n):
    lower_bound = 1 << (n - 1)  # Smallest n-bit number (e.g., 2^(n-1))
    upper_bound = (1 << n) - 1  # Largest n-bit number (e.g., 2^n - 1)
    return randprime(lower_bound, upper_bound)


def int_encrypt(x):
    X = 0
    base = 256  # Sử dụng hệ cơ số 256 cho ký tự ASCII
    for i in range(len(x)):
        X += ord(x[i]) * (base ** (len(x) - i - 1))
    return X

def decrypt_to_str(n):
    result = []
    base = 256
    while n > 0:
        remainder = n % base  # Get the remainder in base 256 (for a-z)
        char = chr(remainder)  # Convert remainder to uppercase letter
        result.append(char)
        n = n // base  # Move to the next "digit"
    return "".join(result[::-1])  # Reverse the list and join to get the string


def generate_random_number(bound):
    # Generate a random integer with 'bound' digits
    lower_bound = 1  # Smallest number with 'bound' digits
    upper_bound = bound - 1  # Largest number with 'bound' digits
    a = random.randint(lower_bound, upper_bound)
    return a
