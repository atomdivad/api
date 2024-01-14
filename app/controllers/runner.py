from fastapi import FastAPI
from ..routes import anuncio, login, usuario, categoria, conversa
from fastapi_pagination import add_pagination
app = FastAPI(
    title="MeTroca API",
    description="Troca de itens",
    terms_of_service="https://www.metroca.com.br",
    contact={
        "Developer name": "David Mota",
        "website":"http://peer.dev.br",
        "email":"davidmota@gmail.com",
        
    },
    license_info={
        "name": "xyz",
        "url": "http://metroca.com.br"
    },
    # docs_url="/documentation",
    # redoc_url=None
    )

add_pagination(app)
app.include_router(login.router)
app.include_router(usuario.router)
app.include_router(anuncio.router)
app.include_router(categoria.router)
app.include_router(conversa.router)

admin_api = FastAPI(
    title="MeTroca API Adminstração",
    description="AdminPage",
    terms_of_service="https://www.metroca.com.br/admin",
    contact={
        "Developer name": "David Mota",
        "website":"http://peer.dev.br",
        "email":"davidmota@gmail.com",
        
    },
    license_info={
        "name": "xyz",
        "url": "http://metroca.com.br"
    },
    # docs_url="/documentation",
    # redoc_url=None
    )
app.mount("/admin", admin_api)
# admin_api.include_router(categoria.router)