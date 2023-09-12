from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from tipo import Tipo
from natureza import Natureza
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column 
from model import Base

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer)
    email = Column(String(100))
    nome = Column(String(100))
def __init__(self, id:int, email:str, nome:str):
    self.id = id
    self.email = email
    self.nome = nome
