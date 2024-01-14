from __future__ import annotations
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from typing import List
from ..controllers.database import Base
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Anuncio(Base):
    __tablename__ = 'anuncios'
    idanuncio: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descricao = Column(String)
    interesses = Column(String)
    ativo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.idusuario"))
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.idcategoria"))
    usuario: Mapped["Usuario"] = relationship(back_populates="anuncio")
    categoria: Mapped["Categoria"] = relationship(back_populates="anuncios")
    conversa: Mapped[List["Conversa"]] = relationship(back_populates="anuncio")
    fotos: Mapped[List["Fotos"]] = relationship(back_populates="anuncios")
    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="anuncios")
