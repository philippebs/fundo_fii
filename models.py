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

    def __init__(self, codigo):
        'Codigodo_fundo', 
        'Setor', 
        'Preco_Atual', 
        'Liquidez_Diaria', 
        'Dividendo', 
        'DividendYield', 
        'DY_3MAcumulado', 
        'DY_6MAcumulado', 
        'DY_12MAcumulado', 
        'DY_3MMedia', 
        'DY_6MMedia', 
        'DY_12MMedia', 
        'DY_Ano', 
        'Variacao_Preco', 
        'RentabPeriodo', 
        'RentabAcumulada', 
        'PatrimonioLiq', 
        'VPA', 
        'PVPA', 
        'DYPatrimonial', 
        'VariacaoPatrimonial', 
        'Rentab_Patrno_Periodo', 
        'Rentab_PatrAcumulada', 
        'VacanciaFisica', 
        'VacanciaFinanceira', 
        'QuantidadeAtivos'


# acao = Acao('Teste')

# print(acao.nome)
