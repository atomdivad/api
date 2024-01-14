from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from ..controllers.database import Base
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Mensagem(Base):
    __tablename__ = 'mensagens'
    idmensagem: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    mensagem = Column(String, nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.idusuario"))
    conversa_id: Mapped[int] = mapped_column(ForeignKey("conversas.idconversa"))
    usuario: Mapped["Usuario"] = relationship(back_populates="mensagens")
    conversa: Mapped["Conversa"] = relationship(back_populates="mensagem")