from pydantic import BaseModel
from .token import Token
class Login(BaseModel):
    usuario: str
    senha: str

class DisplayLogin(BaseModel):
    usuario: str
    auth_info: Token
    class Config:
        orm_mode = True

