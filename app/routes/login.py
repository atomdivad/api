from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated, Union
from ..controllers import database
from ..schemas.login import Login
from ..schemas.token import TokenData
from ..models.usuario import Usuario
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError # python-jose
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..schemas import usuario as UsuarioSchema
from ..util import env

router = APIRouter(
    tags=['Login'],
    prefix="/login"
    )

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, env.ALGORITHM)
    return encoded_jwt


# @router.post('/', response_model=schemas.DisplayLogin)
@router.post('/',status_code=status.HTTP_202_ACCEPTED,)
# def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
def login(request: Login, db: Session = Depends(database.get_db)):
    usuario = db.query(Usuario).filter(Usuario.usuario == request.usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found/invalid user")
    if not pwd_context.verify(request.senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid paswword")
    access_token = generate_token(
        data={"sub": usuario.usuario}
        )
    # return {"username": user.username, "auth_info": {"access_token": access_token, "token_type": "bearer"}}
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
        usuario: str = payload.get('sub')
        if usuario is None:
            raise credentials_exception
        token_data = TokenData(usuario=usuario)
        return token_data
    except JWTError:
        raise credentials_exception


@router.get('/token/status',
            summary="Mostra status do token")
def anuncios(db: Session = Depends(database.get_db), current_user: UsuarioSchema.Usuario = Depends(get_current_user)):

    return {"detail":"active"}