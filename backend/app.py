import fastapi
from pydantic import *
from runner import *
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

frontend_url = "http://localhost:3000"
origins = [frontend_url]

class MessageInput(BaseModel):
    message: str
    
class DecryptInput(BaseModel):
    encrypted: str  # Dữ liệu được mã hóa dạng chuỗi
    private_key: str  # Khóa riêng dạng chuỗi
    n: str  # Số nguyên n dạng chuỗi
    
class VerifyInput(BaseModel):
    message: str
    encrypted: str  # Dữ liệu được mã hóa dạng chuỗi
    private_key: str  # Khóa riêng dạng chuỗi
    n: str  # Số nguyên n dạng chuỗi


# Hàm run_rsa() không cần phải là async nhưng bạn vẫn có thể đợi nó trong sự kiện startup

@app.get("/")
def read_root():
    return {"State": "Active"}

@app.post("/rsa-encrypt")
async def rsa_encrypt(input_data: MessageInput):
    result = await run_rsa_enc(input_data.message)
    return result

@app.post("/rsa-decrypt")
async def rsa_decrypt(input_data: DecryptInput):
    encrypted = int(input_data.encrypted)
    private_key = int(input_data.private_key)
    n = int(input_data.n)
    result = await run_rsa_dec(encrypted,private_key,n)
    return result

@app.post("/rsa-signature")
async def rsa_signature(input_data: MessageInput):
    result = await run_rsa_sig(input_data.message)
    return result

@app.post("/rsa-verify")
async def rsa_verify(input_data: VerifyInput):
    message = str(input_data.message)
    encrypted = int(input_data.encrypted)
    private_key = int(input_data.private_key)
    n = int(input_data.n)
    result = await run_rsa_ver(message, encrypted,private_key,n)
    return result
    
    
# @app.get("/elgamal-encrypt")
# async def elgamal_signature():

    
# @app.get("/elgamal-signature")
# async def elgamal_signature():
    

# @app.get("")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
