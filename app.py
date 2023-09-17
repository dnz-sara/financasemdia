from asyncio.log import logger
from flask import redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from sqlalchemy.exc import IntegrityError
from lookups import LookupLoader

from model import Lancamento, Session
from model.tipolancamento import TipoLancamento
from schemas.error import ErrorSchema
from schemas.lancamento import *

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc.")
lancamento_tag = Tag(name="Lançamento", description="Adiciona, visualiza e remove lançamentos.")
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
def add_lancamento(form: NovoLancamentoSchema):
    """Adicionar um novo lançamento
    """
    novo_lancamento = Lancamento(
        mes_ano_referencia = form.mes_ano_referencia,
        id_tipo_lancamento=form.tipo_lancamento,
        valor_lancamento=form.valor_lancamento, 
        descricao=form.descricao,
        comentario=form.comentario
        )
    try:
        session = Session() 
        session.add(novo_lancamento)   
        session.commit()

        print(novo_lancamento)

        return apresenta_lancamento(novo_lancamento), 200

    except IntegrityError as e:
        error_msg = "Não foi possível criar o lançamento com os dados inseridos"  
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = "Ocorreu um erro interno e seu lançamento não foi registrado"
        logger.warning(e)
        return {"mesage": error_msg}, 400    



@app.get('/api/lancamentos', tags=[lancamento_tag],
         responses={"200": ListagemLancamentoSchema, "404": ErrorSchema})
def get_lancamentos(query: LancamentoBuscaSchema):
    """Faz a busca por todos os Lançamentos cadastrados

    Retorna uma representação da listagem de lançamentos.
    """
    session = Session()
    lancamentos = session.query(Lancamento).filter(Lancamento.mes_ano_referencia == query.mes_ano_referencia)

    if not lancamentos:
        return {"lancamentos": []}, 200
    else:
        print(lancamentos)
        return apresenta_lancamentos(lancamentos), 200



@app.get('/api/lancamento', tags=[lancamento_tag],
         responses={"200": LancamentoViewSchema, "404": ErrorSchema})
def get_lancamento(query: LancamentoBuscaSchema):
    """Faz a busca por Lançamentos cadastrados

    a partir de um Id.
    """
    session = Session()

    lancamento = session.query(Lancamento).filter(Lancamento.id == query.id).first()

    if not lancamento:
        return {"mesage": f"Lançamento não encontrado na database. Lancamento Id: {query.id} "}, 404
    else:
        return apresenta_lancamento(lancamento), 200


@app.delete('/api/lancamento', tags=[lancamento_tag],
            responses={"200": LancamentoDeleteSchema, "404": ErrorSchema})
def delete_lancamento(query: LancamentoBuscaSchema):
    """ Remove um lançamento existente a partir do seu identificador
        Retorna uma mensagem de confirmação da remoção.
    """
    session = Session()
    count = session.query(Lancamento).filter(Lancamento.id == query.id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Lançamento removido", "id": query.id}
    else:
        # se o produto não foi encontrado
        return {"mesage": f"Erro ao excluir lançamento. Lançamento não encontrado. Id: {query.id} "}, 404


@app.get('/api/tipo_lancamento', tags=[lookup_tipos_lancamento],
         responses={"200": ListagemTipoDeLancamentoSchema, "404": ErrorSchema})
def get_tipos_de_lancamentos():
    """Retorna os tipos de lançamentos existentes na database"""

    #abre uma conexão com o banco de dados através do ORM sqlAlchemy
    session = Session()
    # busco todos os tipos de lançamentos existentes na tabela tipo_lancamento
    # utilizando a funçao do ORM .all()
    tipos_de_lancamentos = session.query(TipoLancamento).all()
    # verifico se existem itens em tipos_de_lancamento
    if not tipos_de_lancamentos:
        # caso não existam itens, retorna uma representaçao de lista vazia
        return {"tipos_de_lancamentos": []}, 200
    else:
        # caso existam itens, retorna uma representaçao dos itens da lista
        return apresenta_tipos_de_lancamentos(tipos_de_lancamentos), 200


