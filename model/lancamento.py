from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from tipo import Tipo
from natureza import Natureza
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column 
from model import Base    

class Lancamento(Base):
    __tablename__ = 'lancamento'    
    
    id = Column("pk_lancamento", Integer, primary_key=True)
    id_usuario = Column(Integer)
    mes_referencia = Column(Integer)
    ano_referencia = Column(Integer)
    tipo_lancamento = Column(Tipo)
    valor_lancamento = Column(Float)
    comentario = Column(String(500))
    natureza_id = Mapped[int] = mapped_column(ForeignKey("natureza.id"))
    
    def __init__(self, id_usuario:int, mes_referencia:int, ano_referencia:int, tipo_lancamento:Tipo, 
                 valor_lancamento:float, comentario:str, natureza_id:int):
        self.id_usuario = id_usuario
        self.mes_referencia = mes_referencia
        self.ano_referencia = ano_referencia
        self.tipo_lancamento = tipo_lancamento
        self.valor_lancamento = valor_lancamento
        self.comentario = comentario
        self.natureza_id = natureza_id


        
        


