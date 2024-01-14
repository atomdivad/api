from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from .anuncio import MostraAnuncioResumo
from .mensagem import MostraTodasAsMensagens

# pydantic é usado para validação de dados
# https://pydantic-docs.helpmanual.io/usage/validators/


class Conversa(BaseModel):
    # usuario_visitante_id: Optional[int] = None
    anuncio_id: int


class MostraConversa(BaseModel):
    idconversa: int
    # anuncio_id: int
    anuncio: MostraAnuncioResumo
    created_at: Optional[datetime] = None

    # mensagens: MostraTodasAsMensagens
    class Config:
        orm_mode = True
