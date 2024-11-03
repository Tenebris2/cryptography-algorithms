# p: 6 chu so nguyen tu => Tim phan tu nguyen thuy
# a: 5 chu so

from helper import generate_prime, generate_random_number, int_encrypt
from ecc import EllipticCurve, Point
from hashlib import sha256
import requests


class ElGamal:
    def __init__(self, p, q, a, k):
        self.p = p  # prime number self.a = a  # random number
        self.alpha = primitive_root(p, q)
        self.beta = pow(self.alpha, a, p)
        self.a = a
        self.k = k

    def encrypt(self, message: int) -> (int, int):
        c_1 = pow(self.alpha, self.k, self.p)
        c_2 = (message * pow(self.beta, self.k, self.p)) % self.p
        return (c_1, c_2)

    def decrypt(self, c_1, c_2) -> int:
        temp = pow(pow(c_1, self.a, self.p), -1, self.p) % self.p
        return c_2 * (temp) % self.p


def primitive_root(p, q):
    for i in range(2, p):
        if is_primitive_root(i, p, q):
            return i


def is_primitive_root(a, p, q):
    if pow(a, 2, p) == 1:
        return False

    if pow(a, p, q) == 1:
        return False

    return True


def generate_safe_prime(bit_size):
    response = requests.get(f"https://2ton.com.au/getprimes/random/{bit_size}")

    p, q = 0, 0
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        safe_primes_data = response.json()

        p = int(safe_primes_data["p"]["base10"])
        q = int(safe_primes_data["q"]["base10"])
    else:
        print(f"Error: {response.status_code}")

    return p, q


def generate_keys(key_size: int):
    # generate safe prime
    p, q = generate_safe_prime(key_size)
    a = generate_random_number(p)
    k = generate_random_number(p)

    return p, q, a, k


class EllipticElGamal(ElGamal):
    def __init__(self, a_, b_, p, a, k):
        super().__init__(p, a, k)
        self.elliptic_curve = EllipticCurve(p, a_, b_)

    def find_point(self, x):
        points = self.elliptic_curve.find_points_on_curve()
        for point in points:
            if point.x == x:
                return point

    def encode_message_as_point(self, message):
        x = int(message) % self.p
        result = self.elliptic_curve.self_multiply_generator(Point(0, 376), 85)
        print(result)

    def encrypt(self, message: int) -> (int, int):
        return super().encrypt(message)


class SigningElGamal(ElGamal):
    def sign(self, message: int) -> (int, int):
        sig_1 = pow(self.alpha, self.k, self.p)
        sig_2 = ((message - self.a * sig_1) * pow(self.k, -1, self.p - 1)) % (
            self.p - 1
        )

        return (sig_1, sig_2)

    def verify(self, message: int, sig_1, sig_2) -> bool:
        lhs = pow(self.beta, sig_1, self.p) * pow(sig_1, sig_2, self.p) % self.p
        rhs = pow(self.alpha, message, self.p)

        return lhs == rhs


def elgamal_cryptography():
    x = int_encrypt("BUIDUCANH")

    p, q, a, k = generate_keys(4096 * 2)
    elgamal = ElGamal(p, q, a, k)
    c_1, c_2 = elgamal.encrypt(x)
    print(elgamal.decrypt(c_1, c_2))


# def ecc_elgamal_main():
#     p = 751
#     a = 85
#     k = 101
#     a_ = -1
#     b_ = 188
#     secret_key = 85
#     ecc_elgamal = EllipticElGamal(a_, b_, p, a, k)
#     ecc_elgamal.encode_message_as_point(12)
#


def signed_elgamal_main():
    p, q, a, k = generate_keys(4096 * 2)

    signed_elgamal = SigningElGamal(p, q, a, k)
    message = 2000
    c_1, c_2 = signed_elgamal.encrypt(message)
    print(signed_elgamal.decrypt(c_1, c_2))
    sig_1, sig_2 = signed_elgamal.sign(message)
    print(signed_elgamal.verify(message, sig_1, sig_2))


# signed_elgamal_main()
elgamal_cryptography()
