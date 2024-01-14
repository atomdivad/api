from __future__ import annotations
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from typing import List
from ..controllers.database import Base
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped


# https://learnings.desipenguin.com/post/rolechecker-with-fastapi/
# https://sqlalchemy-migrate.readthedocs.io/en/latest/
# https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_working_with_joins.htm
class Usuario(Base):
    __tablename__ = "usuarios"
    idusuario: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario = Column(String, nullable=False, unique=True)
    nome = Column(String, nullable=False)
    sobrenome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    cpf = Column(String, unique=True)
    senha = Column(String, nullable=False)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    anuncio: Mapped[List["Anuncio"]] = relationship(back_populates="usuario")
    telefones: Mapped[List["Telefone"]] = relationship(back_populates="usuario")
    conversa: Mapped[List["Conversa"]] = relationship(back_populates="usuario")
    mensagens: Mapped[List["Mensagem"]] = relationship(back_populates="usuario")
    favoritos: Mapped[List["Favorito"]] = relationship(back_populates="usuarios")


# favoritos = Table(
#     "favoritos",
#     Base.metadata,
#     Column("id_favorito", Integer, primary_key=True, index=True),
#     Column("usuario_id",  ForeignKey("usuarios.idusuario"), nullable=False),
#     Column("anuncio_id", ForeignKey("anuncios.idanuncio"), nullable=False),
# )
