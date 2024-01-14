from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..schemas import usuario as UsuarioSchema
from ..schemas import favorito as FavoritoSchema
from ..schemas import anuncio as AnuncioSchema
from ..models import Usuario
from ..models import Anuncio
from ..models import Favorito
from ..controllers.database import get_db
from passlib.context import CryptContext
from email_validator import validate_email, EmailNotValidError
from app.routes.login import get_current_user
from fastapi_pagination import Page, paginate


router = APIRouter(
    tags=['Usuarios'],
    prefix="/usuario"
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/', 
             summary="Cria um usuário",
             response_model=UsuarioSchema.MostraUsuario)
def cria_usuario(request: UsuarioSchema.Usuario, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.senha)
    try:
        emailinfo = validate_email(request.email, check_deliverability=False)
        email = emailinfo.normalized

    except EmailNotValidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    novo_usuario = Usuario(usuario=request.usuario,
                                        nome=request.nome,
                                        sobrenome=request.sobrenome,
                                        cpf=request.cpf,
                                        latitude=request.latitude,
                                        longitude=request.longitude,
                                        email=email, 
                                        senha=hashed_password)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.put('/', summary="Atualização localização do usuário")
def atualiza_localizacao(request: UsuarioSchema.Localizacao, db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario)
    if not usuario.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado')
    else:
        usuario.update(request.dict())
        db.commit()
        return {'status':'Localização atualizada'}

@router.get('/favoritos',
            summary="Retorna a lista de anúncios favoritos do usuário",
            response_model=Page[AnuncioSchema.MostraAnuncio])
def anuncio(db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    lista_favoritos = db.query(Favorito).filter(Favorito.usuario_id == usuario.idusuario).order_by(Favorito.idfavorito.desc()).all() # idfavorito decrescente 
    if not lista_favoritos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Favoritos não encontrados')
    favoritos = []
    for elemento in lista_favoritos:
        anuncio = db.query(Anuncio).filter(Anuncio.idanuncio == elemento.anuncio_id).first()
        favoritos.append(anuncio)
    return paginate(favoritos)

@router.get('/favoritos/{id}',
            summary="Retorna se um anúncio é favorito")
def anuncio(id: int, db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    favorito = db.query(Favorito).filter(Favorito.usuario_id == usuario.idusuario).filter(Favorito.anuncio_id == id).first() # idfavorito decrescente 
    if not favorito:
        return {"favorito": False}
    return {"favorito": True}

@router.post('/favoritos/adiciona', 
             summary="Adiciona um anúncio favorito",
             response_model=FavoritoSchema.MostraFavorito)
def insere_favorito(request: FavoritoSchema.Favorito, db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    verifica_existecia = db.query(Favorito).filter(Favorito.usuario_id == usuario.idusuario).filter(Favorito.anuncio_id==request.anuncio_id).first()
    if verifica_existecia:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Anúncio já favoritado')
    adiciona_favorito = Favorito(usuario_id=usuario.idusuario, anuncio_id=request.anuncio_id)
    db.add(adiciona_favorito)
    db.commit()
    db.refresh(adiciona_favorito)
    return adiciona_favorito


@router.delete('/favoritos/remove/{id}', summary="Remove um anúncio favorito do usuário")
def deleta_favorito(id, db: Session = Depends(get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.usuario == current_user.usuario).first()
    favorito = db.query(Favorito).filter(Favorito.usuario_id == usuario.idusuario).filter(Favorito.anuncio_id == id).first()
    if not favorito:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Anúncio não favoritado')
    db.query(Favorito).filter(Favorito.idfavorito == favorito.idfavorito).delete(synchronize_session=False)
    db.commit()
    return {'Anúncio retirado dos favoritos'}
