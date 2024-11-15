import hashlib
import random
from algorithms.curves import SECP521r1

# Khởi tạo các tham số đường cong SECP521r1
p, a, b, G, n = SECP521r1()

# Hàm tính nghịch đảo modulo sử dụng thuật toán Euclid mở rộng
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
            return None  # Điểm tại vô cực
        l = (3 * P[0] * P[0] + a) * mod_inv(2 * P[1], p) % p
    else:
        l = (Q[1] - P[1]) * mod_inv(Q[0] - P[0], p) % p
    x = (l * l - P[0] - Q[0]) % p
    y = (l * (P[0] - x) - P[1]) % p
    return (x, y)

# Phép nhân điểm (nhân đôi và cộng - Double and Add)
def scalar_mult(k, P):
    R = None
    while k:
        if k & 1:
            R = point_add(R, P)
        P = point_add(P, P)
        k >>= 1
    return R

# Mã hóa ElGamal trên đường cong elliptic
def encrypt(plain_point, public_key):
    k = random.randint(1, n - 1)
    C1 = scalar_mult(k, G)  # Điểm công khai
    shared_secret = scalar_mult(k, public_key)
    C2 = point_add(plain_point, shared_secret)  # Tạo điểm mã hóa
    return (C1, C2)

# Giải mã ElGamal trên đường cong elliptic
def decrypt(ciphertext, private_key):
    C1, C2 = ciphertext
    shared_secret = scalar_mult(private_key, C1)
    neg_shared_secret = (shared_secret[0], -shared_secret[1] % p)  # Điểm đối
    plain_point = point_add(C2, neg_shared_secret)
    return plain_point

# Tạo chữ ký số ECDSA
def ecdsa_sign(message, private_key):
    z = int(hashlib.sha256(message.encode()).hexdigest(), 16)  # Băm thành số nguyên
    while True:
        k = random.randint(1, n - 1)
        R = scalar_mult(k, G)
        r = R[0] % n
        if r == 0:
            continue
        k_inv = mod_inv(k, n)
        s = (k_inv * (z + r * private_key)) % n
        if s != 0:
            break
    return (r, s)

# Xác minh chữ ký số ECDSA
def ecdsa_verify(message, signature, public_key):
    r, s = signature
    if not (1 <= r < n and 1 <= s < n):
        return False
    z = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    w = mod_inv(s, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    P = point_add(scalar_mult(u1, G), scalar_mult(u2, public_key))
    return P is not None and (P[0] % n) == r

# Chạy thử mã hóa/giải mã và ký/xác minh
def main():
    # Tạo khóa riêng và khóa công khai
    private_key = random.randint(1, n - 1)
    public_key = scalar_mult(private_key, G)

    # Điểm để mã hóa (ví dụ dữ liệu hoặc thông điệp dưới dạng tọa độ trên đường cong)
    plain_point = (123456, 789012)  # Đây là ví dụ, điểm cần nằm trên đường cong elliptic

    print("Public key:", public_key)

    # Mã hóa và giải mã
    ciphertext = encrypt(plain_point, public_key)
    decrypted_point = decrypt(ciphertext, private_key)

    print("Original point:", plain_point)
    print("Ciphertext:", ciphertext)
    print("Decrypted point:", decrypted_point)

    # Kiểm tra mã hóa/giải mã thành công
    if plain_point == decrypted_point:
        print("Decryption successful!")
    else:
        print("Decryption failed!")

    # Ký và xác minh thông điệp
    message = "Hello, Elliptic Curve!"
    signature = ecdsa_sign(message, private_key)
    is_valid = ecdsa_verify(message, signature, public_key)

    print("Message:", message)
    print("Signature:", signature)
    print("Signature valid:", is_valid)


if __name__ == "__main__":
    main()
