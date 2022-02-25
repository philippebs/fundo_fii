from datetime import datetime, date
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date
# from sqlalchemy.orm import relationships, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import QueryableAttribute
import os

db_path = os.path.join(os.path.dirname(__file__), "investimento.db")
db_uri = "sqlite:///{}".format(db_path)
engine = create_engine(db_uri) #'sqlite:///investimento.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

def save_one_models(model:Base):
    if model.id is None:
        db_session.add(model)
    db_session.commit()

def save_all_models(models):
    for model in models:
        if model.id is None:
            db_session.add(model)
    db_session.commit()
    

class BaseModel(Base):
    __abstract__ = True

    def to_dict(self, show=None, _hide=None, _path=None):
        """Return a dictionary representation of this model."""

        show = show or []
        _hide = _hide or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'criado', 'atualizado', 'ativo'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        _path=('%s.%s' % (_path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data

class Investimento(BaseModel):
    __tablename__ = 'investimento'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(30))
    descricao = Column(String(120))
    tipo = Column(String(120))
    criado = Column(DateTime, default=datetime.now)
    atualizado = Column(DateTime)
    ativo = Column(Boolean, default=True)
    fiis = relationship("Fii", back_populates="investimento") #, cascade = 'all, delete-orphan', lazy = 'dynamic')
    acoes = relationship("Acao", back_populates="investimento") #, backref="investimento", cascade = 'all, delete-orphan', lazy = 'dynamic')

    _default_fields = [
        'codigo', 'descricao','tipo'
    ]

    def __init__(self, codigo:str, tipo:str, descricao:str="", ativo:bool=True) -> None:
        self.codigo = codigo
        self.tipo = tipo
        self.descricao = descricao
        self.atualizado = datetime.now()
        self.ativo = ativo
        

    def __repr__(self):
            return f'<User {self.codigo!r}>'


    def __eq__(self, other) -> bool:
        return self.codigo == other.codigo

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Fii(BaseModel):
    __tablename__ = "fii"
    id = Column(Integer, primary_key=True)
    investimento_id = Column(Integer, ForeignKey('investimento.id'))
    investimento = relationship("Investimento",back_populates="fiis", uselist=False) # backref=backref("fiis", uselist=False))
    data_importacao = Column(Date, default=date.today)
    setor =  Column(String(30))
    preco_atual =  Column(String(30))
    liquidez_diaria =  Column(String(30))
    dividendo =  Column(String(30))
    dividend_yield =  Column(String(30))
    dy_3m_acumulado =  Column(String(30))
    dy_6m_acumulado =  Column(String(30))
    dy_12m_acumulado =  Column(String(30))
    dy_3m_media =  Column(String(30))
    dy_6m_media =  Column(String(30))
    dy_12m_media =  Column(String(30))
    dy_ano =  Column(String(30)) 
    variacao_preco =  Column(String(30))
    rentabilidade_periodo =  Column(String(30))
    rentabilidade_acumulada =  Column(String(30))
    patrimonio_liq =  Column(String(30))
    vpa =  Column(String(30))
    pvpa = Column(String(30))
    dy_patrimonial =  Column(String(30))
    variacao_patrimonial =  Column(String(30))
    rentabilidade_patrno_periodo =  Column(String(30))
    rentabilidade_patr_acumulada =  Column(String(30))
    vacancia_fisica =  Column(String(30))
    vacancia_financeira =  Column(String(30))
    quantidade_ativos =  Column(String(30))
    criado = Column(DateTime, default=datetime.utcnow)
    atualizado = Column(DateTime)
    ativo = Column(Boolean, default=True)

    _default_fields = [
        'preco_atual', 'liquidez_diaria','dividendo', 'dividend_yield', 'dy_3m_acumulado', 'dy_6m_acumulado', 'dy_12m_acumulado',
        'dy_3m_media', 'dy_6m_media', 'dy_12m_media', 'dy_ano', 'variacao_preco', 'rentabilidade_periodo', 'rentabilidade_acumulada', 'patrimonio_liq',
        'vpa', 'pvpa', 'dy_patrimonial', 'variacao_patrimonial', 'rentabilidade_patrno_periodo', 'rentabilidade_patr_acumulada', 'vacancia_fisica',
        'vacancia_financeira', 'quantidade_ativos'
    ]

    def __init__(self, investimento_id, data_importacao, setor, preco_atual, liquidez_diaria
                ,dividendo, dividend_yield, dy_3m_acumulado, dy_6m_acumulado, dy_12m_acumulado,
                dy_3m_media, dy_6m_media, dy_12m_media, dy_ano, variacao_preco, rentabilidade_periodo, rentabilidade_acumulada, patrimonio_liq,
                vpa, pvpa, dy_patrimonial, variacao_patrimonial, rentabilidade_patrno_periodo, rentabilidade_patr_acumulada, vacancia_fisica,
                vacancia_financeira, quantidade_ativos, ativo:bool=True):
        self.investimento_id = investimento_id
        self.setor = setor
        self.data_importacao = data_importacao
        self.preco_atual = preco_atual
        self.liquidez_diaria = liquidez_diaria
        self.dividendo = dividendo
        self.dividend_yield = dividend_yield
        self.dy_3m_acumulado = dy_3m_acumulado
        self.dy_6m_acumulado = dy_6m_acumulado
        self.dy_12m_acumulado = dy_12m_acumulado
        self.dy_3m_media = dy_3m_media
        self.dy_6m_media = dy_6m_media
        self.dy_12m_media = dy_12m_media
        self.dy_ano = dy_ano 
        self.variacao_preco = variacao_preco
        self.rentabilidade_periodo = rentabilidade_periodo
        self.rentabilidade_acumulada = rentabilidade_acumulada
        self.patrimonio_liq = patrimonio_liq
        self.vpa = vpa
        self.pvpa = pvpa
        self.dy_patrimonial = dy_patrimonial
        self.variacao_patrimonial = variacao_patrimonial
        self.rentabilidade_patrno_periodo = rentabilidade_patrno_periodo
        self.rentabilidade_patr_acumulada = rentabilidade_patr_acumulada
        self.vacancia_fisica = vacancia_fisica
        self.vacancia_financeira = vacancia_financeira
        self.quantidade_ativos = quantidade_ativos
        self.atualizado = datetime.utcnow()
        self.ativo = ativo

    
    def __repr__(self):
        return f'<Investimento {self.name!r}>'


    def __eq__(self, other) -> bool:
        return self.investimento.codigo == other.investimento.codigo

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Acao(BaseModel):
    __tablename__ = "acao"
    id = Column(Integer, primary_key=True)
    investimento_id = Column(Integer, ForeignKey('investimento.id'))
    # investimento = relationships("Investimento", backref=backref("acao", uselist=False))
    investimento = relationship("Investimento", back_populates="acoes", uselist=False) #, backref=backref("acao", uselist=False))
    data_importacao = Column(Date)
    valor_atual = Column(String(30))
    min_52_semanas = Column(String(30))
    max_52_semanas = Column(String(30))
    dividend_yield = Column(String(30))
    valorizacao_12m = Column(String(30))
    dy = Column(String(30))
    pl = Column(String(30))
    peg_ratio = Column(String(30))
    pvp = Column(String(30))
    evebitda = Column(String(30))
    evebit = Column(String(30))
    pebitda = Column(String(30))
    pebit = Column(String(30))
    vpa = Column(String(30))
    pativo = Column(String(30))
    lpa = Column(String(30))
    psr = Column(String(30))
    pcap_giro = Column(String(30))
    pativo_circ_liq = Column(String(30))
    div_liquidapl = Column(String(30))
    div_liquidaebitda = Column(String(30))
    div_liquidaebit = Column(String(30))
    plativos = Column(String(30))
    passivoativos = Column(String(30))
    liq_corrente = Column(String(30))
    m_bruta = Column(String(30))
    m_ebitda = Column(String(30))
    m_ebit = Column(String(30))
    m_liquida = Column(String(30))
    roe = Column(String(30)) 
    roa = Column(String(30))
    roic = Column(String(30))
    giro_ativos = Column(String(30))
    cagr_receitas_5_anos = Column(String(30))
    cagr_lucros_5_anos = Column(String(30))
    criado = Column(DateTime, default=datetime.utcnow)
    atualizado = Column(DateTime)
    ativo = Column(Boolean, default=True)


class AcaoOld():

    def __init__(self, codigo, valor_atual, min_52_semanas, max_52_semanas, dividend_yield, valorizacao_12m, dy, pl, peg_ratio, pvp, evebitda, evebit, pebitda, pebit,vpa, pativo,
                lpa, psr,pcap_giro,pativo_circ_liq, div_liquidapl,div_liquidaebitda, div_liquidaebit, plativos, passivoativos, liq_corrente, m_bruta, m_ebitda, m_ebit,
                m_liquida, roe, roa, roic, giro_ativos, cagr_receitas_5_anos, cagr_lucros_5_anos): 
        self.codigo = codigo
        self.valor_atual = valor_atual
        self.min_52_semanas = min_52_semanas
        self.max_52_semanas = max_52_semanas
        self.dividend_yield = dividend_yield
        self.valorizacao_12m = valorizacao_12m 
        self.dy = dy
        self.pl = pl
        self.peg_ratio = peg_ratio
        self.pvp = pvp
        self.evebitda = evebitda
        self.evebit = evebit
        self.pebitda = pebitda
        self.pebit = pebit
        self.vpa = vpa
        self.pativo = pativo
        self.lpa = lpa
        self.psr = psr
        self.pcap_giro = pcap_giro
        self.pativo_circ_liq = pativo_circ_liq
        self.div_liquidapl = div_liquidapl
        self.div_liquidaebitda = div_liquidaebitda
        self.div_liquidaebit = div_liquidaebit
        self.plativos = plativos
        self.passivoativos = passivoativos
        self.liq_corrente = liq_corrente
        self.m_bruta = m_bruta
        self.m_ebitda = m_ebitda
        self.m_ebit = m_ebit
        self.m_liquida = m_liquida
        self.roe = roe
        self.roa = roa
        self.roic = roic
        self.giro_ativos = giro_ativos
        self.cagr_receitas_5_anos = cagr_receitas_5_anos
        self.cagr_lucros_5_anos = cagr_lucros_5_anos


    def __eq__(self, other) -> bool:
        return self.investimento.codigo == other.investimento.codigo


class FiiOld():

    def __init__(self, link, codigo_fundo, setor, preco_atual, liquidez_diaria,dividendo, dividend_yield, dy_3m_acumulado, dy_6m_acumulado, dy_12m_acumulado,
                dy_3m_media, dy_6m_media, dy_12m_media, dy_ano, variacao_preco, rentabilidade_periodo, rentabilidade_acumulada, patrimonio_liq,
                vpa, pvpa, dy_patrimonial, variacao_patrimonial, rentabilidade_patrno_periodo, rentabilidade_patr_acumulada, vacancia_fisica,
                vacancia_financeira, quantidade_ativos):
        self.link = link
        self.codigo_fundo = codigo_fundo
        self.setor = setor
        self.preco_atual = preco_atual
        self.liquidez_diaria = liquidez_diaria
        self.dividendo = dividendo
        self.dividend_yield = dividend_yield
        self.dy_3m_acumulado = dy_3m_acumulado
        self.dy_6m_acumulado = dy_6m_acumulado
        self.dy_12m_acumulado = dy_12m_acumulado
        self.dy_3m_media = dy_3m_media
        self.dy_6m_media = dy_6m_media
        self.dy_12m_media = dy_12m_media
        self.dy_ano = dy_ano 
        self.variacao_preco = variacao_preco
        self.rentabilidade_periodo = rentabilidade_periodo
        self.rentabilidade_acumulada = rentabilidade_acumulada
        self.patrimonio_liq = patrimonio_liq
        self.vpa = vpa
        self.pvpa = pvpa
        self.dy_patrimonial = dy_patrimonial
        self.variacao_patrimonial = variacao_patrimonial
        self.rentabilidade_patrno_periodo = rentabilidade_patrno_periodo
        self.rentabilidade_patr_acumulada = rentabilidade_patr_acumulada
        self.vacancia_fisica = vacancia_fisica
        self.vacancia_financeira = vacancia_financeira
        self.quantidade_ativos = quantidade_ativos

