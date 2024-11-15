"""
File to run algorithms
"""

from algorithms.rsa import *
from algorithms.elgamal import *
from algorithms.ECElGamal import *
from algorithms.helper import *


# RSA
async def run_rsa_enc(message: str):
    # Chạy tệp module1.py và truyền input_value cho nó
    encrypted, private_key, n, public_key, decrypted = rsa_encrypt(message)
    return {
        "encrypted": str(encrypted),
        "private_key": str(private_key),
        "public_key": str(public_key),
        "n": str(n),
        "decrypted": str(decrypted),
    }


async def run_rsa_dec(encrypted: int, private_key: int, n: int):
    # Chạy tệp module1.py và truyền input_value cho nó
    decrypted = rsa_decrypt(encrypted, private_key, n)
    return {"decrypted": str(decrypted)}


async def run_rsa_sig(message: str):
    # Chạy tệp module1.py và truyền input_value cho nó
    encrypted, private_key, n = rsa_signature(message)
    return {
        "encrypted": str(encrypted),
        "private_key": str(private_key),
        "n": str(n),
    }


async def run_rsa_ver(message: str, encrypted: int, private_key: int, n: int):
    # Chạy tệp module1.py và truyền input_value cho nó
    verify = rsa_verify(message, encrypted, private_key, n)
    return {"Verified": verify}


# ElGamal
async def run_elgamal_enc(message: str):
    c_1, c_2, p, a, decrypted = elgamal_cryptography(message)
    return {
        "encrypted": f"({c_1}, {c_2})",
        "private_key": f"({p}, {a})",
        "decrypted": str(decrypted),
    }


async def run_elgamal_sig(message: str):
    sig_1, sig_2, verify = elgamal_signature(message)
    return {"signature": f"({sig_1}, {sig_2})", "verify": str(verify)}


async def run_elgamal_dec(c_1: int, c_2: int, alpha: int, a: int, p: int):
    decrypted = elgamal_decrypt(c_1, c_2, alpha, a, p)
    return {"decrypted": decrypted}


async def run_elgamal_ver(
    message: str, sig_1: int, sig_2: int, alpha: int, beta: int, p: int
):
    verify = elgamal_verify(message, sig_1, sig_2, alpha, beta, p)
    return {"verify": str(verify)}


# Elliptic vs ECDSA
async def run_ecelgamal_enc(message: str):
    # Chuyển đổi message thành điểm trên đường cong (giả định về cách ánh xạ message thành tọa độ)
    plain_point = (
        int(hash(message)[:4], 16),
        int(hash(message)[4:8], 16),
    )  # Giả sử điểm hợp lệ

    # Tạo khóa riêng và khóa công khai
    private_key = random.randint(1, n - 1)
    public_key = scalar_mult(private_key, G)

    # Mã hóa điểm thông điệp với khóa công khai
    c_1, c_2 = encrypt(plain_point, public_key)

    # Giải mã để kiểm tra tính đúng đắn
    decrypted_point = decrypt((c_1, c_2), private_key)

    return {
        "encrypted": f"({c_1}, {c_2})",
        "private_key": f"{private_key}",
        "public_key": f"{public_key}",
        "decrypted": str(decrypted_point),
    }


# Hàm ký số ECDSA với đầu vào là thông điệp cần ký
async def run_ecelgamal_sig(message: str):
    # Tạo khóa riêng và khóa công khai
    private_key = random.randint(1, n - 1)
    public_key = scalar_mult(private_key, G)

    # Ký số
    sig_1, sig_2 = ecdsa_sign(message, private_key)

    # Xác minh chữ ký để kiểm tra tính đúng đắn
    verify = ecdsa_verify(message, (sig_1, sig_2), public_key)

    return {
        "signature": f"({sig_1}, {sig_2})",
        "public_key": f"{public_key}",
        "verify": str(verify),
    }


# Hàm giải mã ElGamal với đầu vào là cặp mã và khóa riêng
async def run_ecelgamal_dec(c_1, c_2, private_key):
    # Giải mã cặp mã hóa ElGamal
    decrypted_point = decrypt((c_1, c_2), private_key)
    return {"decrypted": str(decrypted_point)}


# Hàm xác minh chữ ký ECDSA với đầu vào là thông điệp, chữ ký và khóa công khai
async def run_ecelgamal_ver(message: str, sig_1: int, sig_2: int, public_key):
    # Xác minh chữ ký với thông điệp và khóa công khai
    verify = ecdsa_verify(message, (sig_1, sig_2), public_key)
    return {"verify": str(verify)}


async def check_prime_aks(n: int):
    return aks_prime_test(n)
