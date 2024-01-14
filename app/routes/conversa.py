from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..schemas import usuario as UsuarioSchema
from ..schemas import conversa as ConversaSchema
from ..schemas import anuncio as AnuncioSchema
from ..schemas import mensagem as MensagemSchema
from ..models import Usuario
from ..models import Anuncio
from ..models import Conversa
from ..models import Mensagem

from ..controllers.database import get_db

from app.routes.login import get_current_user
from fastapi_pagination import Page, paginate


router = APIRouter(
    tags=['Conversas'],
    prefix="/conversas"
    )

@router.get('/{id}', 
            summary="Retorna uma conversa pelo respectivo ID",
            response_model=ConversaSchema.MostraConversa)
def conversa_id(id: int, db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):

    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    query= text(f"conversas.usuario_visitante_id = {usuario.idusuario} or anuncios.usuario_id = {usuario.idusuario}")
    conversa_detalhada = db.query(Conversa).join(Anuncio).where(query).filter(Conversa.idconversa == id).first()
    if not conversa_detalhada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Conversa não encontrada')
    return conversa_detalhada

@router.get('/', 
            summary="Retorna a lista de conversas",
            response_model=Page[ConversaSchema.MostraConversa])
def conversa_lista(db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    query= text(f"conversas.usuario_visitante_id = {usuario.idusuario} or anuncios.usuario_id = {usuario.idusuario}")
    lista_conversas = db.query(Conversa).join(Anuncio).join(Usuario, isouter=True).where(query).order_by(Conversa.created_at.desc()).all()
    return paginate(lista_conversas)


@router.post('/cria', 
             summary="Cria uma conversa",
             response_model=ConversaSchema.MostraConversa)
# @router.post('/cria')
def cria_conversa(request: ConversaSchema.Conversa, db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    query= text(f"conversas.usuario_visitante_id = {usuario.idusuario} and conversas.anuncio_id = {request.anuncio_id} and anuncios.usuario_id != {usuario.idusuario}")
    result = db.query(Conversa).join(Anuncio).where(query).first()
    if not result:
        nova_conversa = Conversa(usuario_visitante_id=usuario.idusuario, anuncio_id=request.anuncio_id)
        db.add(nova_conversa)
        db.commit()
        db.refresh(nova_conversa)
        return nova_conversa
    return result
    # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Conversa Existente {result}')


@router.post('/{id}/mensagens', summary="Envia mensagem para uma determinada conversa(ID)")
# @router.get('/{id}')
def conversa_envia_mensagem(id: int, request: MensagemSchema.Mensagem, db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    query= text(f"conversas.usuario_visitante_id = {usuario.idusuario} or anuncios.usuario_id = {usuario.idusuario}")
    conversa_detalhada = db.query(Conversa).join(Anuncio).where(query).filter(Conversa.idconversa == id).first()
    if not conversa_detalhada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Conversa não encontrada')
    registra_mensagem = Mensagem(mensagem = request.mensagem, 
                                 conversa_id = id,
                                 usuario_id = usuario.idusuario)
    db.add(registra_mensagem)
    db.commit()
    db.refresh(registra_mensagem)
    return registra_mensagem

#response model List[response_model]
@router.get('/{id}/mensagens',
            summary="Retorna todas as mensagens de uma conversa",
            response_model=Page[MensagemSchema.MostraTodasAsMensagens])
def conversa_lista_mensagens(id: int, db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):

    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    query= text(f"conversas.usuario_visitante_id = {usuario.idusuario} or anuncios.usuario_id = {usuario.idusuario}")
    conversa_detalhada = db.query(Conversa).join(Anuncio).where(query).filter(Conversa.idconversa == id).first()
    if not conversa_detalhada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Conversa não encontrada')
    mensagens_lista = db.query(Mensagem).filter(Mensagem.conversa_id == id).order_by(Mensagem.created_at.desc()).all()
    
    return paginate(mensagens_lista)
