from typing import List, Optional
from pydantic import BaseModel
from model.lancamento import Lancamento

class TipoLancamentoSchema(BaseModel):
    """define um tipo de lançamento"""    
    id: int
    descricao: str

class LancamentoViewSchema(BaseModel):
    """ Schema a ser utilizado para retornar dados de um lançamento
    """
    id: int
    mes_ano_referencia: str
    tipo_lancamento: TipoLancamentoSchema
    valor_lancamento: float
    descricao: str
    comentario: str
    

class NovoLancamentoSchema(BaseModel):
    """ Schema utilizado para criar um lançamento
    """
    mes_ano_referencia: str
    tipo_lancamento: int
    valor_lancamento: float
    descricao: Optional[str]
    comentario: Optional[str]

class AtualizarLancamentoSchema(BaseModel):
    """ Schema utilizado para criar um lançamento
    """    
    mes_ano_referencia: str
    tipo_lancamento: int
    valor_lancamento: float
    descricao: Optional[str]
    comentario: Optional[str]



class LancamentoSchema(BaseModel):
    """ Schema utilizado para criar um lançamento
    """
    mes_ano_referencia: str
    tipo_lancamento: TipoLancamentoSchema
    valor_lancamento: float
    descricao: str
    comentario: str

class ListagemLancamentoSchema(BaseModel):
    """ Schema utilizado para listagem de lançamentos 
    """
    lancamentos: List[LancamentoSchema]

class BuscaLancamentosSchema(BaseModel):
    """ Schema para busca de lancamento
    """
    mes_ano_referencia: str

class BuscaLancamentoSchema(BaseModel):
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


class ListagemConsolidadaSchema(BaseModel):
    """ Schema utilizado para listagem das informações de lançamentos consolidadas
    """
    total_despesas: float
    total_receitas: float
    total_rendimentos: float
    saldo: float


def apresenta_lancamento(lancamento: Lancamento):
    return {
        "id": lancamento.id,
        "mes_ano_referencia": lancamento.mes_ano_referencia,
        "tipo_lancamento": { "id": lancamento.tipo_lancamento.id, "descricao": lancamento.tipo_lancamento.descricao },
        "valor_lancamento": lancamento.valor_lancamento,
        "descricao": lancamento.descricao,
        "comentario": lancamento.comentario
    }

def apresenta_lancamentos(lancamentos: List[Lancamento]):
     """ Retorna uma representação do lançamento seguindo o schema definido em
        LancamentoViewSchema.
    """
     result = []
     for lancamento in lancamentos:
        result.append({
        "id": lancamento.id,
        "mes_ano_referencia": lancamento.mes_ano_referencia,
        "tipo_lancamento": { "id": lancamento.tipo_lancamento.id, "descricao": lancamento.tipo_lancamento.descricao },
        "valor_lancamento": lancamento.valor_lancamento,
        "descricao": lancamento.descricao,
        "comentario": lancamento.comentario
        })
     return {"lancamentos": result} 