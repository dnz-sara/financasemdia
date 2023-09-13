from sqlite3 import IntegrityError
from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag
from model import Session
from model.lancamento import Lancamento
from model.tipo import Tipo
from schemas.lancamento import LancamentoSchema, apresenta_lancamento_criado
from schemas.error import ErrorSchema
from schemas.lancamento import LancamentoViewSchema 
from flask_cors import CORS
import logging

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger")
lancamento_tag = Tag(name="Lancamento", description="Adição, visualização e remoção de lançamentos à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post("/api/lancamento", tags=[lancamento_tag],
          responses={"200": LancamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema }) 
def add_lancamento(form: LancamentoSchema):
    """Adiciona um novo lancamento

    Retorna uma representação de lancamento criado
    """
    lancamento = Lancamento(id_usuario=form.id_usuario,
                             mes_referencia=form.mes_referencia,
                             ano_referencia=form.ano_referencia,
                             comentario=form.comentario,
                             tipo_lancamento= form.tipo_lancamento,
                             natureza_id=form.natureza_id,
                             valor_lancamento= form.valor_lancamento
                            )
    
    try:
        session = Session()
        session.add(lancamento)
        session.commit()
        return apresenta_lancamento_criado(lancamento), 200
        
    except IntegrityError as e:
        error_message = "Ocorreu um erro de integridade. Lancamento já incluído a base de dados."
        logging.warning(f"Erro ao incluir lançamento: '{e.sqlite_errorcode}', {e.sqlite_errorname}")
        return { "message": error_message}, 409
    
    except Exception as e:
        error_message = "Erro ao incluir lancamento."
        logging.error(e)
        return { "message": error_message}, 400