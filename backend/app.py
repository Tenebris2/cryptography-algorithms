import fastapi
import pydantic
import runner

app = fastapi.FastAPI()


class Message(pydantic.BaseModel):
    message: str


@app.get("/messages")
async def read_root():
    # encrypted_message, rsa_obj = runner.rsa_runner(message)
    encrypted_message, rsa_obj = runner.rsa_cryptography("BUIDUCANH")
    return {"message": str(hex(encrypted_message))}
