from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


from model.base import Base
from model.lancamento import Lancamento
from model.tipolancamento import TipoLancamento

db_url = 'sqlite:///database/db.sqlite3'

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)