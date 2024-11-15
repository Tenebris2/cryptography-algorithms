import fastapi
from pydantic import *
from runner import *
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

frontend_url = "http://localhost:3000"
origins = [frontend_url]


# RSA
class MessageInput(BaseModel):
    message: str


class RSADecryptInput(BaseModel):
    encrypted: str  # Dữ liệu được mã hóa dạng chuỗi
    private_key: str  # Khóa riêng dạng chuỗi
    n: str  # Số nguyên n dạng chuỗi


class RSAVerifyInput(BaseModel):
    message: str
    encrypted: str  # Dữ liệu được mã hóa dạng chuỗi
    private_key: str  # Khóa riêng dạng chuỗi
    n: str  # Số nguyên n dạng chuỗi


class ElGamalDecryptInput(BaseModel):
    c_1: str  # Dữ liệu được mã hóa dạng chuỗi
    c_2: str  # Khóa riêng dạng chuỗi
    alpha: str  # Số nguyên n dạng chuỗi
    a: str
    p: str


class ElGamalVerifyInput(BaseModel):
    message: str
    c_1: str  # Dữ liệu được mã hóa dạng chuỗi
    c_2: str  # Khóa riêng dạng chuỗi
    alpha: str  # Số nguyên n dạng chuỗi
    a: str
    p: str


@app.get("/")
def read_root():
    return {"State": "Active"}


@app.post("/rsa-encrypt")
async def rsa_encrypt(input_data: MessageInput):
    result = await run_rsa_enc(input_data.message)
    return result


@app.post("/rsa-decrypt")
async def rsa_decrypt(input_data: RSADecryptInput):
    encrypted = int(input_data.encrypted)
    private_key = int(input_data.private_key)
    n = int(input_data.n)
    result = await run_rsa_dec(encrypted, private_key, n)
    return result


@app.post("/rsa-signature")
async def rsa_signature(input_data: MessageInput):
    result = await run_rsa_sig(input_data.message)
    return result


@app.post("/rsa-verify")
async def rsa_verify(input_data: RSAVerifyInput):
    message = str(input_data.message)
    encrypted = int(input_data.encrypted)
    private_key = int(input_data.private_key)
    n = int(input_data.n)
    result = await run_rsa_ver(message, encrypted, private_key, n)
    return result


# ElGamal


@app.post("/elgamal-encrypt")
async def elgamal_encrypt(input_data: MessageInput):
    result = await run_elgamal_enc(input_data.message)
    return result


@app.post("/elgamal-signature")
async def elgamal_signature(input_data: MessageInput):
    result = await run_elgamal_sig(input_data.message)
    return result


@app.post("/elgamal-decrypt")
async def elgamal_decrypt(input_data: ElGamalDecryptInput):
    c_1 = int(input_data.c_1)
    c_2 = int(input_data.c_2)
    alpha = int(input_data.alpha)
    a = int(input_data.a)
    p = int(input_data.p)
    result = await run_elgamal_dec(c_1, c_2, alpha, a, p)
    return result


@app.post("/elgamal-verify")
async def elgamal_verify(input_data: ElGamalDecryptInput):
    message = str(input_data.message)
    c_1 = int(input_data.c_1)
    c_2 = int(input_data.c_2)
    alpha = int(input_data.alpha)
    a = int(input_data.a)
    p = int(input_data.p)
    result = await run_elgamal_ver(message, c_1, c_2, alpha, a, p)
    return result


# EcElgamal - encrypt
@app.post("/ecelgamal-encrypt")
async def ecelgamal_encrypt(input_data: MessageInput):
    result = await run_ecelgamal_enc(input_data.message)
    return result


# ECElGamal (ECDSA) - Signature
@app.post("/ecelgamal-signature")
async def ecelgamal_signature(input_data: MessageInput):
    result = await run_ecelgamal_sig(input_data.message)
    return result


# ECElGamal (ECDSA) - Decrypt
@app.post("/ecelgamal-decrypt")
async def ecelgamal_decrypt(input_data: ElGamalDecryptInput):
    c_1 = int(input_data.c_1)
    c_2 = int(input_data.c_2)
    alpha = int(input_data.alpha)
    a = int(input_data.a)
    p = int(input_data.p)
    result = await run_ecelgamal_dec(c_1, c_2, alpha, a, p)
    return result


# ECElGamal (ECDSA) - Verify
@app.post("/ecelgamal-verify")
async def ecelgamal_verify(input_data: ElGamalVerifyInput):
    message = str(input_data.message)
    c_1 = int(input_data.c_1)
    c_2 = int(input_data.c_2)
    alpha = int(input_data.alpha)
    a = int(input_data.a)
    p = int(input_data.p)
    result = await run_ecelgamal_ver(message, c_1, c_2, alpha, a, p)
    return result


@app.post("/aks-check-prime")
async def check_prime(data: MessageInput):
    n = int(data.message)
    return {"is_prime": f"{aks_prime_test(n)}"}


# @app.get("")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, modify this as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/messages")
async def read_root():
    # encrypted_message, rsa_obj = runner.rsa_runner(message)
    encrypted_message, rsa_obj = runner.rsa_cryptography("BUIDUCANH")
    return {"message": str(hex(encrypted_message))}


@app.post("/api/rsa/")
async def rsa_cryptography_api(data: MessageInput):
    encrypted_message, rsa_obj = runner.rsa_cryptography(data.message)
    return {"message": str(hex(encrypted_message))}
