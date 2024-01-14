from fastapi import APIRouter, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session
from fastapi.params import Depends
from app.routes.login import get_current_user
from ..schemas import categoria as CategoriaSchema
from ..models import Categoria
from ..controllers.database import get_db
from fastapi_pagination import Page, paginate
router = APIRouter(
    tags=['Categorias'],
    prefix="/categorias"
    )

# @router.delete('/{id}')
# def delete(id, db: Session = Depends(get_db)):
#     db.query(Categoria).filter(Categoria.idcategoria == id).delete(synchronize_session=False)
#     db.commit()
#     return {'Categoria deletada'}



@router.get('/', response_model=List[CategoriaSchema.MostraCategoria])
def categoria(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return categorias

# @router.get('/{id}')
@router.get('/{id}', response_model=CategoriaSchema.MostraCategoriaDetalhada)
def categoria(id: int, db: Session = Depends(get_db)):
# def categoria(id: int, db: Session = Depends(get_db), current_user: CategoriaSchema.Categoria = Depends(get_current_user)):
    categoria = db.query(Categoria).filter(Categoria.idcategoria == id).first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada')
    return categoria

# @router.put('/{id}')
# def update(id, request: CategoriaSchema.Categoria, db: Session = Depends(get_db)):
#     categoria = db.query(Categoria).filter(Categoria.idcategoria == id)
#     if not categoria.first():
#         return {'Categoria não encontrada'}
#     else:
#         categoria.update(request.dict())
#         db.commit()
#         return {'Categoria atualizada'}

# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=CategoriaSchema.MostraCategoria)
# def add(request: CategoriaSchema.Categoria, db: Session = Depends(get_db)):
# # def add(request: CategoriaSchema.Categoria, db: Session = Depends(get_db), current_user: CategoriaSchema.Categoria = Depends(get_current_user)):
#     nova_categoria = Categoria(nome=request.nome, descricao=request.descricao, ativa=True)
#     db.add(nova_categoria)
#     db.commit()
#     db.refresh(nova_categoria)
#     return nova_categoria
