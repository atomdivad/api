from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey, String
from ..controllers.database import Base
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Fotos(Base):
    __tablename__ = 'fotos'
    idfoto: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    foto_codigo = Column(String, nullable=False)
    anuncio_id: Mapped[int] = mapped_column(ForeignKey("anuncios.idanuncio"), nullable=False)
    anuncios: Mapped["Anuncio"] = relationship(back_populates="fotos")
