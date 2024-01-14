from ..controllers.database import engine
from .categoria import *
from .anuncio import *
from .fotos import *
from .telefone import *
from .usuario import *
from .conversa import *
from .mensagem import *
from .favorito import *

Base.metadata.create_all(engine)