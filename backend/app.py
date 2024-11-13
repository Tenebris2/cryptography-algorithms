import fastapi
import pydantic
import runner
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

frontend_url = "http://localhost:3000"
origins = [frontend_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(pydantic.BaseModel):
    message: str


@app.get("/messages")
async def read_root():
    # encrypted_message, rsa_obj = runner.rsa_runner(message)
    encrypted_message, rsa_obj = runner.rsa_cryptography("BUIDUCANH")
    return {"message": str(hex(encrypted_message))}


@app.post("/api/rsa/")
async def rsa_cryptography_api(data: Message):
    encrypted_message, rsa_obj = runner.rsa_cryptography(data.message)
    return {"message": str(hex(encrypted_message))}
