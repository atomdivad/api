from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey
from ..controllers.database import Base
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
class Favorito(Base):
    __tablename__ = 'favoritos'
    idfavorito: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.idusuario"), nullable=False)
    anuncio_id: Mapped[int] = mapped_column(ForeignKey("anuncios.idanuncio"), nullable=False)
    usuarios: Mapped["Usuario"] = relationship(back_populates="favoritos")
    anuncios: Mapped["Anuncio"] = relationship(back_populates="favoritos")
