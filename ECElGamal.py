from hashlib import sha256
from cryptography.hazmat.primitives.asymmetric import ec

curve = ec.SECP521R1()
# Các tham số đường cong secp256k1
p = 2**521 - 1
a = 0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC
b = 0x0051953EB9618E1C9A1F929A21A0B68540EEA2DA725B99B315F3B8B489918EF109E156193951EC7E937B1652C0BD3BB1BF073573DF883D2C34F1EF451FD46B503F00
G = (
    0x00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66,
    0x011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD16650,
)
n = 0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF


# Hàm tính nghịch đảo modulo sử dụng Thuật toán Euclid mở rộng
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
