from __future__ import annotations
from sqlalchemy import Column, Integer, String, Boolean
from ..controllers.database import Base
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
class Categoria(Base):
    __tablename__ = 'categorias'
    idcategoria: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    ativa = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    anuncios: Mapped["Anuncio"] = relationship(back_populates="categoria")