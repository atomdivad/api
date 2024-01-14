from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from .anuncio import MostraAnuncioResumo
from .usuario import MostraUsuarioSimplificado

# https://docs.pydantic.dev/latest/usage/models/
# https://pydantic-docs.helpmanual.io/usage/validators/


class Mensagem(BaseModel):
    mensagem: str
    # usuario_id: Optional[int]
    conversa_id: Optional[int]
    # anuncio_id: Optional[int]


class MostraMensagem(BaseModel):
    idmensagem: int
    # mensagem: str
    conversa_id: int

    class Config:
        orm_mode = True


class MostraTodasAsMensagens(BaseModel):
    mensagem: str
    usuario: MostraUsuarioSimplificado
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
