

from model import Session, TipoLancamento
import model

class LookupLoader():
    def carregarLookups():
        """ Carrega lookups padrão da applicação
        """    
        print("Carregando lookups")

        session = Session()

        if not session.query(TipoLancamento).filter(TipoLancamento.descricao == "Receita").first():
            tipo_lancamento_receita = model.TipoLancamento(descricao="Receita")
            session.add(tipo_lancamento_receita)

        if not session.query(TipoLancamento).filter(TipoLancamento.descricao == "Despesa").first():
            tipo_lancamento_despesa = model.TipoLancamento(descricao="Despesa")
            session.add(tipo_lancamento_despesa)

        if not session.query(TipoLancamento).filter(TipoLancamento.descricao == "Rendimento").first():
            tipo_lancamento_rendimento = model.TipoLancamento(descricao="Rendimento")
            session.add(tipo_lancamento_rendimento)

        session.commit()

        # print(tipo_lancamento_receita_exists)

        # if not tipo_lancamento_receita_exists:
        #     tipo_lancamento_receita = model.TipoLancamento(descricao="Receita")
        #     session.add(tipo_lancamento_receita)
        #     session.commit()