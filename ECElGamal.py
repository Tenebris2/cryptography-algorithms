from hashlib import sha256
from curves import SECP521r1

# Các tham số đường cong secp256k1

p, a, b, G, n = SECP521r1()


# Hàm tính nghịch đảo modulo sử dụng Thuật toán Euclid mở rộng
def generate_keys():
    pass


def mod_inv(x, p):
    if x == 0:
        raise ZeroDivisionError("Không tồn tại nghịch đảo")
    lm, hm = 1, 0
    low, high = x % p, p
    while low > 1:
        ratio = high // low
        nm, new = hm - lm * ratio, high - low * ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % p


# Phép cộng điểm trên đường cong elliptic
def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        if P[1] == 0:
            raise ValueError("Point P is at infinity or vertical tangent.")
        l = (3 * P[0] * P[0] + a) * mod_inv(2 * P[1], p) % p
    else:
        l = (Q[1] - P[1]) * mod_inv(Q[0] - P[0], p) % p
    x = (l * l - P[0] - Q[0]) % p
    y = (l * (P[0] - x) - P[1]) % p
    return (x, y)


# Phép nhân điểm (dùng kỹ thuật nhân đôi và cộng - Double and Add)
def scalar_mult(k, P):
    R = None
    while k:
        if k & 1:
            R = point_add(R, P)
        P = point_add(P, P)
        k >>= 1
    return R


import random


def encrypt(plain_point, public_key):
    k = random.randint(1, n - 1)
    C1 = scalar_mult(k, G)
    shared_secret = scalar_mult(k, public_key)
    C2 = point_add(plain_point, shared_secret)
    return (C1, C2)


def decrypt(ciphertext, private_key):
    C1, C2 = ciphertext
    shared_secret = scalar_mult(private_key, C1)
    neg_shared_secret = (shared_secret[0], -shared_secret[1] % p)
    plain_point = point_add(C2, neg_shared_secret)
    return plain_point


def ecdsa_sig(msg, private_key):
    z = sha256(msg)
    while True:
        k = random.randint(1, N - 1)
        R = elliptic_multiply(k, G)
        r = r[0] % n
        if r == 0:
            continue
        s = (pow(k, -1, n) * (z + r * private_key)) % n
        if s != 0:
            break
    return (r, s)


def ecdsa_ver(msg, signature, public_key):
    r, s = signature
    if not (1 <= r < n and 1 <= s < n):
        return false
    z = sha256(msg)
    w = pow(s, -1, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    p = elliptic_add(elliptic_multiply(u1, g), elliptic_multiply(u2, public_key))
    return p[0] % n == r


def main():
    private_key = random.randint(1, n - 1)
    public_key = scalar_mult(private_key, G)

    plain_point = (1234567890, 987654321)

    ciphertext = encrypt(plain_point, public_key)
    print("Ciphertext:", ciphertext)

    decrypted_point = decrypt(ciphertext, private_key)
    print("Decrypted point:", decrypted_point)


main()
