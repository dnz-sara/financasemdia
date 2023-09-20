from sqlalchemy import update, func
from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from sqlalchemy.exc import IntegrityError
from lookups import LookupLoader
import logging
from model import Lancamento, Session
from model.tipolancamento import TipoLancamento
from schemas.error import ErrorSchema
from schemas.lancamento import *
from schemas.path import *

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc.")
lancamento_tag = Tag(name="Lançamento", description="Adiciona, busca, edita e remove lançamentos.")
lookup_tipos_lancamento = Tag(name="TipoLancamento", description="Lista a lookup de tipos de lançamentos")

info = Info(title="Finanças em dia - API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
""" carregando as database lookups """
with app.app_context():
    from lookups import LookupLoader
    LookupLoader.carregarLookups()


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/api/lancamento', tags=[lancamento_tag],
          responses={"200": LancamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_lancamento(body: NovoLancamentoSchema):
    """Adicionar um novo lançamento
    """
    novo_lancamento = Lancamento(
        mes_ano_referencia = body.mes_ano_referencia,
        id_tipo_lancamento=body.tipo_lancamento,
        valor_lancamento=body.valor_lancamento, 
        descricao=body.descricao,
        comentario=body.comentario
        )
    try:
        session = Session() 
        session.add(novo_lancamento)   
        session.commit()

        return apresenta_lancamento(novo_lancamento), 200

    except IntegrityError as e:
        error_msg = "Não foi possível criar o lançamento com os dados inseridos"  
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = "Ocorreu um erro interno e seu lançamento não foi registrado"
        logging.warning(e)
        return {"mesage": error_msg}, 400    


@app.put('/api/lancamento/<int:id>', tags=[lancamento_tag],
          responses={"200": LancamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def edit_lancamento(path: Path, body: AtualizarLancamentoSchema):
    """Atualizar um lançamento existente

    Retorna uma representação do lançamento atualizado
    """
    try:

        session = Session() 
        lancamento = session.query(Lancamento).filter(Lancamento.id == path.id).first()
        lancamento.comentario = body.comentario
        lancamento.mes_ano_referencia = body.mes_ano_referencia
        lancamento.id_tipo_lancamento = body.tipo_lancamento
        lancamento.valor_lancamento = body.valor_lancamento 
        lancamento.descricao = body.descricao

        if not lancamento :
            logging.warning(e)
            error_msg = "Lançamento não encontrado na base de dados."  
            return {"mesage": error_msg}, 409

        else :
            print(body.descricao)

            session.commit()
            return apresenta_lancamento(lancamento), 200


    except IntegrityError as e:
        logging.warning(e)
        error_msg = "Não foi possível atualizar o lançamento com os dados inseridos"  
        return {"mesage": error_msg}, 409

    except Exception as e:
        logging.warning(e)
        error_msg = "Ocorreu um erro interno e seu lançamento não foi atualizado"
        return {"mesage": error_msg}, 400    



@app.get('/api/lancamentos', tags=[lancamento_tag],
         responses={"200": ListagemLancamentoSchema, "404": ErrorSchema})
def get_lancamentos(query: BuscaLancamentosSchema):
    """Faz a busca por todos os Lançamentos cadastrados para um mês de referência

    Retorna uma representação da listagem de lançamentos.
    """
    session = Session()
    lancamentos = session.query(Lancamento).filter(Lancamento.mes_ano_referencia == query.mes_ano_referencia)

    if not lancamentos:
        return {"lancamentos": []}, 200
    else:
        print(lancamentos)
        return apresenta_lancamentos(lancamentos), 200



@app.get('/api/lancamento/<int:id>', tags=[lancamento_tag],
         responses={"200": LancamentoViewSchema, "404": ErrorSchema})
def get_lancamento(path: Path):
    """Faz a busca de um lançamento específico a partir de um Id.

    Retorna a representação de um lançamento existente.
    """
    session = Session()

    lancamento = session.query(Lancamento).filter(Lancamento.id == path.id).first()

    if not lancamento:
        return {"mesage": f"Lançamento não encontrado na database. Lancamento Id: {path.id} "}, 404
    else:
        return apresenta_lancamento(lancamento), 200


@app.delete('/api/lancamento/<int:id>', tags=[lancamento_tag],
            responses={"200": LancamentoDeleteSchema, "404": ErrorSchema})
def delete_lancamento(path: Path):
    """ Remove um lançamento existente a partir do seu identificador
        Retorna uma mensagem de confirmação da remoção.
    """
    session = Session()
    count = session.query(Lancamento).filter(Lancamento.id == path.id).delete()
    session.commit()
    logging.warning(count)

    if count > 0:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Lançamento removido", "id": path.id}
    else:
        # se o produto não foi encontrado
        return {"mesage": f"Erro ao excluir lançamento. Lançamento não encontrado. Id: {path.id} "}, 404

@app.get('/api/lancamento/consolidado', tags=[lancamento_tag],
         responses={"200": ListagemConsolidadaSchema, "404": ErrorSchema})
def get_consolidacao(query: BuscaLancamentosSchema):
    """
        Retorna o resumo de lançamentos de cada mês
    """
    session = Session()   
    total_receitas : float = 0
    total_despesas : float = 0
    total_rendimentos : float = 0

    #soma receitas
    consulta_receitas = session.query(func.sum(Lancamento.valor_lancamento).label('total'))\
    .filter(Lancamento.mes_ano_referencia == query.mes_ano_referencia, Lancamento.id_tipo_lancamento == 1)\
    .group_by(Lancamento.id_tipo_lancamento)

    resultado_receitas = consulta_receitas.first()

    if resultado_receitas :
        total_receitas = consulta_receitas.first().total

    #soma despesas
    consulta_despesas = session.query(func.sum(Lancamento.valor_lancamento)\
        .label('total'))\
        .filter(Lancamento.mes_ano_referencia == query.mes_ano_referencia, Lancamento.id_tipo_lancamento == 2)\
        .group_by(Lancamento.id_tipo_lancamento)

    resultado_despesas = consulta_despesas.first()

    if resultado_despesas: 
        total_despesas = consulta_despesas.first().total

    #soma de rendimentos
    consulta_rendimentos = session.query(func.sum(Lancamento.valor_lancamento)\
    .label('total'))\
    .filter(Lancamento.mes_ano_referencia == query.mes_ano_referencia, Lancamento.id_tipo_lancamento == 3)\
    .group_by(Lancamento.id_tipo_lancamento)

    resultado_rendimentos = consulta_rendimentos.first()

    if resultado_rendimentos: 
        total_rendimentos = consulta_rendimentos.first().total
  
    saldo = (total_receitas + total_rendimentos) - total_despesas

    return { "total_despesas": total_despesas,  "total_receitas": total_receitas, "total_rendimentos": total_rendimentos, "saldo":  saldo}