from pydantic import BaseModel
from .usuario import MostraUsuario, MostraUsuarioSimplificado
from .categoria import MostraCategoria
from .fotos import MostraFoto
from typing import Optional, List

class Anuncio(BaseModel):
    titulo: str
    descricao: str
    interesses: str
    fotos: List[str]
    categoria_id: int
class MostraAnuncio(BaseModel):
    idanuncio: int
    titulo: str
    descricao: str
    interesses: str
    usuario: MostraUsuario
    ativo: bool
    fotos: Optional[List[MostraFoto]]
    categoria: MostraCategoria
    class Config:
        orm_mode = True
class MostraAnuncioFavorito(BaseModel):
    idanuncio: int
    titulo: str
    descricao: str
    class Config:
        orm_mode = True

class MostraAnuncioResumo(BaseModel):
    idanuncio: int
    usuario_id: int
    usuario: MostraUsuarioSimplificado
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    fotos: Optional[List[MostraFoto]]
    class Config:
        orm_mode = True
