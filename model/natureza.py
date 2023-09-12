from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from tipo import Tipo
from natureza import Natureza
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column 
from model import Base

class Natureza(Base):
    __tablename__ = 'natureza'
    
    id = Column("pk_natureza", Integer, primary_key=True)
    descricao = (String(50))
    tipo = (Tipo)

    def __init__(self, descricao:str): 
        self.descricao = descricao
