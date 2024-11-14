from algorithms.helper import *
import gmpy2
import concurrent.futures
import math


# Helper function to convert integer to string using custom decryption

def choose_e(phi):
    e = phi - 1
    if math.gcd(phi, e) == 1:
        return e
    else:
        for candidate in range(phi, 2, -2):  # Start from 3, check odd numbers
            if math.gcd(phi, candidate) == 1:
                return candidate
        raise ValueError("Could not find a suitable 'e' that is coprime to phi.")


def get_decryption_key(e, phi):
    return pow(e, -1, phi)


def enc(p, e, n):
    return pow(p, e, n)


def dec(c, d, n):
    return pow(c, d, n)


def rsa_encrypt(message):
    bound = 1024 #8192
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_p = executor.submit(generate_n_bit_prime, bound)
        future_q = executor.submit(generate_n_bit_prime, bound)
        p = gmpy2.mpz(future_p.result())
        q = gmpy2.mpz(future_q.result())

    n = gmpy2.mul(p, q)
    phi = gmpy2.mul((p - 1), (q - 1))
    e = choose_e(phi)

    plaintext = int_encrypt(message)
    encrypted = enc(plaintext, e, n)
    private_key = get_decryption_key(e, phi)
    public_key = e
    decrypted = rsa_decrypt(encrypted, private_key, n)
    return encrypted, private_key, n, public_key, decrypted


def rsa_decrypt(encrypted, private_key, n):
    decrypted_num = dec(encrypted, private_key, n)
    return decrypt_to_str(decrypted_num)


def rsa_signature(message):
    bound = 1024 #8192
    p = gmpy2.mpz(generate_n_bit_prime(bound))
    q = gmpy2.mpz(generate_n_bit_prime(bound))

    n = gmpy2.mul(p, q)
    phi = gmpy2.mul((p - 1), (q - 1))
    e = choose_e(phi)

    plaintext = int_encrypt(message)
    signature = enc(plaintext, e, n)
    private_key = get_decryption_key(e, phi)

    return signature, private_key, n


def rsa_verify(message, signature, private_key, n):
    plaintext = int_encrypt(message)
    decrypted_signature = dec(signature, private_key, n)

    return plaintext == decrypted_signature



