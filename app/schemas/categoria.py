from datetime import datetime
from pydantic import BaseModel
from typing import Optional
class Categoria(BaseModel):
    nome: str
    descricao: str

class MostraCategoria(BaseModel):
    idcategoria: int
    nome: str
    descricao: str
    class Config:
        orm_mode = True
class MostraCategoriaDetalhada(BaseModel):
    idcategoria: int
    nome: str
    descricao: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        orm_mode = True
