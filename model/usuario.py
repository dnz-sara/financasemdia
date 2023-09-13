from sqlalchemy import Column, String, Integer
from model import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column("pk_usuario", Integer, primary_key=True)
    email = Column(String(100))
    nome = Column(String(100))
def __init__(self, id:int, email:str, nome:str):
    self.id = id
    self.email = email
    self.nome = nome
