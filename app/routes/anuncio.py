from fastapi import APIRouter, status, Response, HTTPException
from sqlalchemy import text
from sqlalchemy import and_
from sqlalchemy.orm import Session
from fastapi.params import Depends
from app.models.categoria import Categoria
from app.models.conversa import Conversa
from ..models import Mensagem
from app.models.favorito import Favorito
from app.routes.login import get_current_user
from ..schemas import anuncio as AnuncioSchema
from ..schemas import usuario as UsuarioSchema
from ..models import Anuncio, Usuario, Fotos
from ..controllers.database import get_db
from fastapi_pagination import Page, paginate

router = APIRouter(tags=["Anuncios"], prefix="/anuncios")

# @router.delete('/{id}')
# def delete(id, db: Session = Depends(get_db)):
#     db.query(Anuncio).filter(Anuncio.idanuncio == id).delete(synchronize_session=False)
#     db.commit()
#     return {'anuncio deletado'}


# https://pt.wikipedia.org/wiki/F%C3%B3rmula_de_haversine


@router.get(
    "/",
    summary="Lista anúncios dos demais usuários",
    response_model=Page[AnuncioSchema.MostraAnuncio],
)
def anuncios(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema.Usuario = Depends(get_current_user),
    raio: float = 10,
    categoria: int = 0,
):  # query parameter
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    # query = text(f"usuarios.latitude::double precision BETWEEN min_lat({usuario.latitude}, {raio}) and max_lat({usuario.latitude}, {raio}) \
    #              and usuarios.longitude::double precision between min_lng({usuario.latitude}, {usuario.longitude}, {raio}) and max_lng({usuario.latitude}, {usuario.longitude}, {raio}) \
    #              and distancia_entre_localidades(usuarios.latitude::double precision, usuarios.longitude::double precision, {usuario.latitude}, {usuario.longitude}) <= {raio} \
    #              and anuncios.ativo is not false order by anuncios.idanuncio desc")
    if categoria == 0:
        query = text(
            f"distancia_entre_localidades(usuarios.latitude::double precision, usuarios.longitude::double precision, {usuario.latitude}, {usuario.longitude}) <= {raio} \
                    and anuncios.ativo is not false order by anuncios.idanuncio desc"
        )
    else:
        query = text(
            f"distancia_entre_localidades(usuarios.latitude::double precision, usuarios.longitude::double precision, {usuario.latitude}, {usuario.longitude}) <= {raio} \
        and anuncios.ativo is not false and anuncios.categoria_id = {categoria} order by anuncios.idanuncio desc"
        )

    anuncios = (
        db.query(Anuncio).join(Usuario).join(Fotos, isouter=True).where(query).all()
    )
    return paginate(anuncios)


@router.get(
    "/usuario/eu",
    summary="Mostra anúncios do usuário",
    response_model=Page[AnuncioSchema.MostraAnuncio],
)
def anuncios(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema.Usuario = Depends(get_current_user),
):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    anuncios = db.query(Anuncio).filter(Anuncio.usuario_id == usuario.idusuario).all()
    return paginate(anuncios)


@router.get(
    "/usuario/{id}",
    summary="Mostra anúncios de um usuário específico",
    response_model=Page[AnuncioSchema.MostraAnuncio],
)
def anuncios(
    id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema.Usuario = Depends(get_current_user),
):
    usuario = db.query(Usuario).filter(Usuario.idusuario == id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    anuncios = db.query(Anuncio).filter(Anuncio.usuario_id == id).all()
    return paginate(anuncios)


@router.get(
    "/{id}",
    summary="Mostra detalhes de um anúncio",
    response_model=AnuncioSchema.MostraAnuncio,
)
def anuncio(
    id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema.Usuario = Depends(get_current_user),
):
    anuncio = (
        db.query(Anuncio)
        .join(Fotos, isouter=True)
        .filter(Anuncio.idanuncio == id)
        .first()
    )
    if not anuncio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Anúncio não encontrado"
        )
    return anuncio


@router.delete("/{id}", summary="Deleta um anúncio")
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema.Usuario = Depends(get_current_user),
):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    anuncio = (
        db.query(Anuncio)
        .filter(Anuncio.idanuncio == id and Anuncio.usuario_id == usuario.idusuario)
        .first()
    )
    if not anuncio:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Anúncio não encontrado"
        )
    db.query(Favorito).filter(Favorito.anuncio_id == id).delete(
        synchronize_session=False
    )
    db.query(Fotos).filter(Fotos.anuncio_id == id).delete(synchronize_session=False)
    conversas = db.query(Conversa).filter(Conversa.anuncio_id == id).all()
    for i in conversas:
        db.query(Mensagem).filter(Mensagem.conversa_id == i.idconversa).delete(
            synchronize_session=False
        )
    for i in conversas:
        db.query(Conversa).filter(Conversa.idconversa == i.idconversa).delete(
            synchronize_session=False
        )
    anuncio_delete = (
        db.query(Anuncio)
        .filter(Anuncio.idanuncio == id and Anuncio.usuario_id == usuario.idusuario)
        .delete(synchronize_session=False)
    )
    if not anuncio_delete:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Problema ao remover",
        )
    db.commit()
    return {"status": "Anúncio deletado"}


@router.put("/{id}", summary="Edita os dados de um anúncio")
def update(id, request: AnuncioSchema.Anuncio, db: Session = Depends(get_db)):
    anuncio = db.query(Anuncio).filter(Anuncio.idanuncio == id)
    if not anuncio.first():
        return {"status": "Anuncio não encontrado"}
    else:
        anuncio.update(request.dict())
        db.commit()
        return {"status": "Anuncio atualizado"}


@router.post(
    "/",
    summary="Insere um anúncio",
    status_code=status.HTTP_201_CREATED,
    response_model=AnuncioSchema.MostraAnuncio,
)
def add(
    request: AnuncioSchema.Anuncio,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema.Usuario = Depends(get_current_user),
):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    novo_anuncio = Anuncio(
        titulo=request.titulo,
        descricao=request.descricao,
        interesses=request.interesses,
        usuario_id=usuario.idusuario,
        categoria_id=request.categoria_id,
    )
    db.add(novo_anuncio)
    db.commit()
    db.refresh(novo_anuncio)
    for foto in request.fotos:
        nova_foto = Fotos(foto_codigo=foto, anuncio_id=novo_anuncio.idanuncio)
        db.add(nova_foto)
        db.commit()
        db.refresh(nova_foto)
    return novo_anuncio
