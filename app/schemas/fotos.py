from pydantic import BaseModel
from typing import Optional, List

class Fotos(BaseModel):
    foto_codigo: str
    anuncio_id: int

class MostraFoto(BaseModel):
    idfoto: int
    foto_codigo: str
    # anuncio_id: int
    class Config:
        orm_mode = True
