from helper import int_encrypt, generate_n_bit_prime
import gmpy2
import concurrent.futures
import math


def int_encrypt(x):
    X = 0
    for i in range(0, len(x)):
        X += (ord(x[i]) - 65) * (26 ** (len(x) - i))
    return X


def decrypt(X):
    result = ""

    while X > 0:
        remainder = X % 26
        # Convert remainder to corresponding character
        char = chr(remainder + 65)  # 65 is the ASCII value for 'A'
        result = char + result  # Prepend the character to the result
        X //= 26  # Integer division to move to the next position

    return result


encrypts = []


def decrypt_to_str(n):
    result = []
    while n > 0:
        remainder = n % 26  # Get the remainder in base 26 (for a-z)
        char = chr(
            remainder + ord("a")
        )  # Convert remainder to a letter (0 -> 'a', 25 -> 'z')
        result.append(char)
        n = n // 26  # Move to the next "digit"
    return "".join(result[::-1])  # Rev


def enc(p, e, n):
    en = pow(p, e, n)
    return en


def get_decryption_key(e, phi):
    return pow(e, -1, phi)


def dec(c, d, n):
    de = pow(c, d, n)
    return de


def choose_e(phi):
    # Commonly used prime exponent in RSA for efficiency and security
    e = phi - 1

    # Ensure e is coprime to phi
    if math.gcd(phi, e) == 1:
        return e
    else:
        # Fallback: find an alternative if 65537 isn't suitable
        for candidate in range(phi, 2, -2):  # Start from 3, check odd numbers
            if math.gcd(phi, candidate) == 1:
                return candidate
        raise ValueError("Could not find a suitable 'e' that is coprime to phi.")


# Function to create gmpy2 mpz object
def to_mpz(num):
    return gmpy2.mpz(num)


# 1000 chu so: rsa
def rsa_cryptography():

    bound = 2048 * 2 * 2
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Parallel generation of primes p and q
        future_p = executor.submit(generate_n_bit_prime, bound)
        future_q = executor.submit(generate_n_bit_prime, bound)

        # Wait for results and convert them to gmpy2 mpz
        p = to_mpz(future_p.result())
        q = to_mpz(future_q.result())
    # p = generate_n_bit_prime(bound)
    # q = generate_n_bit_prime(bound)

    p = gmpy2.mpz(p)
    q = gmpy2.mpz(q)
    # print(p, q)
    # p = 123
    # q = 149
    # p = 6464557691
    # q = 9272675903

    n = gmpy2.mul(p, q)
    phi = gmpy2.mul((p - 1), (q - 1))
    e = choose_e(phi)
    print(f"n : {n}")
    print(f"e: {e}")
    print(f"p: {p}\n q: {q}\n phi: {phi}")

    # e = generate_coprime_numbers(phi)
    plaintext = int_encrypt("BUIDUCANH")
    print("Plaintext: ", plaintext)
    encrypted = enc(plaintext, e, n)
    print("encrypted ciphertext:", encrypted)
    decryption_key = get_decryption_key(e, phi)
    print("decryption key", decryption_key)
    decrypted = dec(encrypted, decryption_key, n)
    print(f"decrypted plaintext:", decrypted)


def rsa_sign():
    bound = 2048 * 2 * 2
    p = to_mpz(generate_n_bit_prime(bound))
    q = to_mpz(generate_n_bit_prime(bound))
    # print(aks_primality_test(p))
    p = gmpy2.mpz(p)
    q = gmpy2.mpz(q)

    n = gmpy2.mul(p, q)
    phi = gmpy2.mul((p - 1), (q - 1))
    e = choose_e(phi)
    print(f"n : {n.bit_length()}")
    print(f"e: {e.bit_length()}")
    print(f"p: {p.bit_length()}\nq: {q.bit_length()}\n phi: {phi.bit_length()}")

    # e = generate_coprime_numbers(phi)
    plaintext = int_encrypt("BUIDUCANH")
    print("Plaintext: ", plaintext.bit_length())
    sig = enc(plaintext, e, n)
    print("Signed text:", sig.bit_length())
    decryption_key = get_decryption_key(e, phi)
    print("Decryption key for checking the signature", decryption_key.bit_length())
    decrypted = dec(sig, decryption_key, n)

    if plaintext == decrypted:
        print(True)
    else:
        print(False)
