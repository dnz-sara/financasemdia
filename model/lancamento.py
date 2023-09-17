from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from model import Base    

class Lancamento(Base):
    __tablename__ = 'lancamento'    
    
    id = Column("id", Integer, primary_key=True)
    mes_ano_referencia = Column(String)
    id_tipo_lancamento = Column(ForeignKey("tipo_lancamento.id"), nullable=False)
    valor_lancamento = Column(Float)
    descricao = Column(String(500))
    comentario = Column(String(500))
   
    tipo_lancamento = relationship("TipoLancamento", uselist = False, backref="lancamento")
    
    def __init__(self, mes_ano_referencia:str, id_tipo_lancamento:int, 
                 valor_lancamento:float, descricao:str, comentario:str):
        self.mes_ano_referencia = mes_ano_referencia
        self.id_tipo_lancamento = id_tipo_lancamento
        self.valor_lancamento = valor_lancamento
        self.descricao = descricao
        self.comentario = comentario

        
        


