from pydantic import BaseModel

# https://pydantic-docs.helpmanual.io/usage/validators/


class Usuario(BaseModel):
    usuario: str
    email: str
    nome: str
    sobrenome: str
    cpf: str
    latitude: str
    longitude: str
    senha: str


class Localizacao(BaseModel):
    latitude: str
    longitude: str
    # class Config:
    #     orm_mode = True


# class MostraLocalizacao(BaseModel):
#     latitude: str
#     longitude: str
#     class Config:
#         orm_mode = True


class MostraUsuario(BaseModel):
    idusuario: int
    usuario: str
    email: str

    class Config:
        orm_mode = True


class MostraUsuarioSimplificado(BaseModel):
    usuario: str
    nome: str

    class Config:
        orm_mode = True
