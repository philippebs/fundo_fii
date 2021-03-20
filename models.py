# from flask_sqlalchemy import SQLAlchemy

class Acao():

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


class Fii():

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

