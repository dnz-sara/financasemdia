from sqlalchemy import Column, String, Integer
from model.tipo import Tipo
from model import Base

class Natureza(Base):
    __tablename__ = 'natureza'
    
    id = Column("id_natureza", Integer, primary_key=True)
    descricao = (String(50))
    tipo = (Tipo)

    def __init__(self, descricao:str): 
        self.descricao = descricao
