from pydantic import BaseModel
from typing import Optional

# https://pydantic-docs.helpmanual.io/usage/validators/


class Favorito(BaseModel):
    anuncio_id: int


class MostraFavorito(BaseModel):
    anuncio_id: int

    class Config:
        orm_mode = True
