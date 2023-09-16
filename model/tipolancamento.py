from enum import unique
from sqlalchemy import Column, String, Integer
from model import Base 

class TipoLancamento (Base):
    __tablename__ = 'tipo_lancamento'
    
    id = Column("id", Integer, primary_key=True)
    descricao = Column(String(50), unique=True)

    def __init__(self, descricao:str): 
        self.descricao = descricao