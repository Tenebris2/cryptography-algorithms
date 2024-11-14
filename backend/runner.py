"""
File to run algorithms
"""
from algorithms.rsa import *

async def run_rsa_enc(message: str):
    # Chạy tệp module1.py và truyền input_value cho nó
    encrypted, private_key, n, public_key, decrypted = rsa_encrypt(message)
    return {
        "encrypted": str(encrypted),
        "private_key": str(private_key),
        "public_key": str(public_key),
        "n":str(n),
        "decrypted": str(decrypted)
    }
    pass

async def run_rsa_dec(encrypted:int, private_key:int, n:int):
    # Chạy tệp module1.py và truyền input_value cho nó
    decrypted = rsa_decrypt(encrypted, private_key, n)
    return {
        "decrypted": str(decrypted)
    }
    pass

async def run_rsa_sig(message: str):
    # Chạy tệp module1.py và truyền input_value cho nó
    encrypted, private_key, n = rsa_signature(message)
    return {
        "encrypted": str(encrypted),
        "private_key": str(private_key),
        "n":str(n),
    }
    pass

async def run_rsa_ver(message:str, encrypted:int, private_key:int, n:int):
    # Chạy tệp module1.py và truyền input_value cho nó
    verify = rsa_verify(message,encrypted, private_key, n)
    return {
        "Verified": verify
    }
    pass


def run_elgamal_enc():
    """
    Elgamal Cryptography runner
    """
    pass


def run_elgamal_sig():
    """
    Elgamal Signature runner
    """

    pass
