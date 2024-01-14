from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from ..controllers.database import Base
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

# https://learnings.desipenguin.com/post/rolechecker-with-fastapi/

# https://sqlalchemy-migrate.readthedocs.io/en/latest/


class Telefone(Base):
    __tablename__ = 'telefones'
    idtelefone: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    telefone = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.idusuario"))
    usuario: Mapped["Usuario"] = relationship(back_populates="telefones")