import hashlib
import random

# Tham số của đường cong secp256r1
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
G = (
    55066263022277343669578718895168534326250603453777594175500187360389116729240,
    32670510020758816978083085130507043184471273380659243275938904335757337482424,
)
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337


def mod_inverse(k, p):
    return pow(k, p - 2, p)


# def mod_inverse(k, p):
#     """Tính toán nghịch đảo modulo bằng cách sử dụng thuật toán Euclid mở rộng"""
#     if k <= 0 or k >= p:
#         raise ValueError("k must be in the range (0, p)")
#
#     r0, r1 = p, k
#     s0, s1 = 1, 0
#     while r1 > 0:
#         q = r0 // r1
#         r0, r1 = r1, r0 - q * r1
#         s0, s1 = s1, s0 - q * s1
#
#     return s0 % p


def point_add(p1, p2):
    """Cộng hai điểm trên đường cong"""
    if p1 == (0, 0):
        return p2
    if p2 == (0, 0):
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 == y2:
        # Tính m = (3 * x1^2 + a) / (2 * y1) với 2 * y1 đã được modulo p
        m = (3 * x1**2 + a) * mod_inverse(2 * y1 % p, p) % p
    else:
        # Tính m = (y2 - y1) / (x2 - x1)
        m = (y2 - y1) * mod_inverse((x2 - x1) % p, p) % p

    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)


def point_multiply(k, P):
    """Nhân một điểm với một số nguyên"""
    R = (0, 0)
    while k:
        if k & 1:
            R = point_add(R, P)
        P = point_add(P, P)
        k >>= 1
    return R


def ecdsa_sign(private_key, message):
    """Ký một thông điệp bằng ECDSA"""
    # Bước 1: Hash thông điệp
    message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    while True:
        # Bước 2: Chọn số ngẫu nhiên k trong khoảng (1, n-1)
        k = random.randint(1, n - 1)

        # Bước 3: Tính R = k * G
        R = point_multiply(k, G)
        r = R[0] % n
        if r == 0:
            continue

        # Bước 4: Tính s
        k_inv = mod_inverse(k, n)
        s = (k_inv * (message_hash + private_key * r)) % n
        if s == 0:
            continue

        return (r, s)


def ecdsa_verify(public_key, message, signature):
    """Xác minh chữ ký bằng ECDSA"""
    r, s = signature

    # Bước 1: Hash thông điệp
    message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16)

    # Bước 2: Tính w = s^(-1) mod n
    w = mod_inverse(s, n)

    # Bước 3: Tính u1 và u2
    u1 = (message_hash * w) % n
    u2 = (r * w) % n

    # Bước 4: Tính điểm P = u1 * G + u2 * public_key
    P1 = point_multiply(u1, G)
    P2 = point_multiply(u2, public_key)
    P = point_add(P1, P2)

    # Bước 5: Kiểm tra r == x(P) mod n
    if P == (0, 0):
        return False  # Kiểm tra điểm vô cùng
    R = P[0] % n
    print("R: ", R, "   r: ", r)
    return R == r


#
# a = 0
# b = 7
# p = 43


private_key = random.randint(1, n - 1)
public_key = point_multiply(private_key, G)

message = "Hello, Luong!"
signature = ecdsa_sign(private_key, message)

print("Private Key:", private_key)
print("Public Key:", public_key)
print("Message:", message)
print("Signature:", signature)

# Xác minh chữ ký
is_valid = ecdsa_verify(public_key, message, signature)
print("Signature valid:", is_valid)
