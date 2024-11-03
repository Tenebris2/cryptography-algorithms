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
    for i in range(0, len(x)):
        X += (ord(x[i]) - 65) * (26 ** (len(x) - i))
    return X


def generate_random_number(bound):
    # Generate a random integer with 'bound' digits
    lower_bound = 1  # Smallest number with 'bound' digits
    upper_bound = bound - 1  # Largest number with 'bound' digits
    a = random.randint(lower_bound, upper_bound)
    return a
