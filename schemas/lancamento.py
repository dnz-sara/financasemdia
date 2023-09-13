from pydantic import BaseModel
from typing import Optional, List

from model.lancamento import Lancamento


class LancamentoSchema(BaseModel):
    id_usuario : int
    mes_referencia : int
    ano_referencia : int
    tipo_lancamento : int 
    valor_lancamento : float
    comentario : str
    natureza_id : int

class LancamentoViewSchema(BaseModel):
    id : int
    id_usuario : int
    mes_referencia : int
    ano_referencia : int
    tipo_lancamento : int 
    valor_lancamento : float
    comentario : str
    natureza_id : int

def apresenta_lancamento_criado(lancamento: Lancamento):
    return {
        "id": lancamento.id,
        "id_usuario" : lancamento.id_usuario,
        "mes_referencia": lancamento.mes_referencia,
        "ano_referencia": lancamento.ano_referencia,
        "tipo_lancamento" : lancamento.tipo_lancamento,
        "valor_lancamento" : lancamento.valor_lancamento,
        "comentario" : lancamento.comentario,
        "natureza_id" : lancamento.natureza_id
    }