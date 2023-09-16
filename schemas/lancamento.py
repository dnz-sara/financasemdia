
from typing import List, Optional
from pydantic import BaseModel
from model.lancamento import Lancamento
from model.tipolancamento import TipoLancamento

class TipoLancamentoSchema(BaseModel):
    """define um tipo de lançamento"""    
    id: int
    descricao: str

class LancamentoViewSchema(BaseModel):
    """ Schema a ser utilizado para retornar dados de um lançamento
    """
    id: int
    mes_referencia: int
    ano_referencia: int
    tipo_lancamento: TipoLancamentoSchema
    valor_lancamento: float
    descricao: str
    comentario: str
    

class NovoLancamentoSchema(BaseModel):
    """ Schema utilizado para criar um lançamento
    """
    mes_referencia: int
    ano_referencia: int
    tipo_lancamento: int
    valor_lancamento: float
    descricao: Optional[str]
    comentario: Optional[str]


class LancamentoSchema(BaseModel):
    """ Schema utilizado para criar um lançamento
    """
    mes_referencia: int
    ano_referencia: int
    tipo_lancamento: TipoLancamentoSchema
    valor_lancamento: float
    descricao: str

class ListagemLancamentoSchema(BaseModel):
    """ Schema utilizado para listagem de lançamentos 
    """
    lancamentos: List[LancamentoSchema]


class LancamentoBuscaSchema(BaseModel):
    """ Schema para busca de lancamento
    """
    id: int


class LancamentoDeleteSchema(BaseModel):
    """ Schema que define retorno após a exclusão de um lançamento.
    """
    mesage: str
    id: int


class ListagemTipoLancamentoSchema(BaseModel):
    """ Schema utilizado para listagem de tipos de lançamento 
    """
    tipo_lancamentos: List[TipoLancamentoSchema]


def apresenta_lancamento(lancamento: Lancamento):
    return {
        "id": lancamento.id,
        "mes_referencia": lancamento.mes_referencia,
        "ano_referencia": lancamento.ano_referencia,
        "tipo_lancamento": { "id": lancamento.tipo_lancamento.id, "descricao": lancamento.tipo_lancamento.descricao },
        "valor_lancamento": lancamento.valor_lancamento,
        "descricao": lancamento.descricao,
    }

def apresenta_lancamentos(lancamentos: List[Lancamento]):
     """ Retorna uma representação do lançamento seguindo o schema definido em
        LancamentoViewSchema.
    """
     result = []
     for lancamento in lancamentos:
        result.append({
        "id": lancamento.id,
        "mes_referencia": lancamento.mes_referencia,
        "ano_referencia": lancamento.ano_referencia,
        "tipo_lancamento": { "id": lancamento.tipo_lancamento.id, "descricao": lancamento.tipo_lancamento.descricao },
        "valor_lancamento": lancamento.valor_lancamento,
        "descricao": lancamento.descricao,
        })
     return {"lancamentos": result} 
 

class ListagemTipoDeLancamentoSchema(BaseModel):
    """ Schema utilizado para listagem de tipos de lançamento 
    """
    tipo_lancamentos: List[ListagemTipoLancamentoSchema]
 
def apresenta_tipos_de_lancamentos(tipos_de_lancamentos: List[TipoLancamento]):
    result = []
    for tipo in tipos_de_lancamentos :
        result.append({
            "id": tipo.id,
            "descricao": tipo.descricao
        })
    return {"tipos_de_lancamentos": result}