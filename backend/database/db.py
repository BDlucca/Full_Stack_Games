from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config
import os

# Cria a pasta do banco se não existir (cuidado básico que todo mundo esquece)
os.makedirs(os.path.dirname(Config.DATABASE_URL.replace('sqlite:///', '')), exist_ok=True)

engine = create_engine(
    Config.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in Config.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency Injection pros routes (o tal do "get_db" que o povo ama)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()