from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..util import env

# SQLALCHEMY_DATABASE_URL = "sqlite:///./product.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{env.DB_USER}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        # yield é um generator
        # Ele retorna um valor mantendo o estado de onde parou.
        #  Quando executa de novo ele continua de onde parou. 
        # Ele controla o estado de um enumerador entre execuções da função.
        yield db
    finally:
        db.close()
