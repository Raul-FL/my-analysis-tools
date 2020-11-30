#!/usr/bin/env python3

import curses
import re
import urllib.request
import urllib.parse
import http.cookiejar
import pickle
import sys
# from termcolor import colored, cprint
# from colorama import init
# init()
# print('\033[31m' + 'some red text')

from lxml.html import fragment_fromstring
from collections import OrderedDict
from decimal import Decimal
from datetime import date


def get_data(*args, **kwargs):
    url = 'http://www.fundamentus.com.br/resultado.php'
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min': '',
            'pl_max': '',
            'pvp_min': '',
            'pvp_max': '',
            'psr_min': '',
            'psr_max': '',
            'divy_min': '',
            'divy_max': '',
            'pativos_min': '',
            'pativos_max': '',
            'pcapgiro_min': '',
            'pcapgiro_max': '',
            'pebit_min': '',
            'pebit_max': '',
            'fgrah_min': '',
            'fgrah_max': '',
            'firma_ebit_min': '',
            'firma_ebit_max': '',
            'margemebit_min': '',
            'margemebit_max': '',
            'margemliq_min': '',
            'margemliq_max': '',
            'liqcorr_min': '',
            'liqcorr_max': '',
            'roic_min': '',
            'roic_max': '',
            'roe_min': '',
            'roe_max': '',
            'liq_min': '',
            'liq_max': '',
            'patrim_min': '',
            'patrim_max': '',
            'divbruta_min': '',
            'divbruta_max': '',
            'tx_cresc_rec_min': '',
            'tx_cresc_rec_max': '',
            'setor': '',
            'negociada': 'ON',
            'ordem': '1',
            'x': '28',
            'y': '16'}

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    content = re.findall(pattern, content)[0]
    page = fragment_fromstring(content)
    result = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        result.update(
            {rows.getchildren()[0][0].getchildren()[0].text: {'Cotacao': todecimal(rows.getchildren()[1].text),
                                                              'P/L': todecimal(rows.getchildren()[2].text),
                                                              'P/VP': todecimal(rows.getchildren()[3].text),
                                                              'PSR': todecimal(rows.getchildren()[4].text),
                                                              'DY': todecimal(rows.getchildren()[5].text),
                                                              'P/Ativo': todecimal(rows.getchildren()[6].text),
                                                              'P/Cap.Giro': todecimal(rows.getchildren()[7].text),
                                                              'P/EBIT': todecimal(rows.getchildren()[8].text),
                                                              'P/ACL': todecimal(rows.getchildren()[9].text),
                                                              'EV/EBIT': todecimal(rows.getchildren()[10].text),
                                                              'EV/EBITDA': todecimal(rows.getchildren()[11].text),
                                                              'Mrg.Ebit': todecimal(rows.getchildren()[12].text),
                                                              'Mrg.Liq.': todecimal(rows.getchildren()[13].text),
                                                              'Liq.Corr.': todecimal(rows.getchildren()[14].text),
                                                              'ROIC': todecimal(rows.getchildren()[15].text),
                                                              'ROE': todecimal(rows.getchildren()[16].text),
                                                              'Liq.2meses': todecimal(rows.getchildren()[17].text),
                                                              'Pat.Liq': todecimal(rows.getchildren()[18].text),
                                                              'Div.Brut/Pat.': todecimal(rows.getchildren()[19].text),
                                                              'Cresc.5anos': todecimal(rows.getchildren()[20].text)}})

    return result


def todecimal(string):
    string = string.replace('.', '')
    string = string.replace(',', '.')

    if (string.endswith('%')):
        string = string[:-1]
        return Decimal(string) / 100
    else:
        return Decimal(string)


def get_indicators_keys():
    print('ct: cotação',
          '\npl: P/L',
          '\npvp: P/VP',
          '\npsr: PSR',
          '\ndy: Dividend Yeld',
          '\npativo: P/Ativo',
          '\npcapgiro: P/Cap - Preço por Capital de Giro',
          '\npebit: P/EBIT',
          '\npacl: P/ACL',
          '\nevebit: EV/EBIT',
          '\nevebitda: EV/EBITDA',
          '\nmrgebit: Mrg.Ebit',
          '\nmrgliq: Mrg.Liq',
          '\nliqcor: Liquidez Corrida',
          '\nroic: ROIC',
          '\nroe: ROE',
          '\nliqd: liquidez 2 meses',
          '\npatliq: Patrimonio Liquido',
          '\ndivpatr: Dívida Bruta Patrimonio',
          '\ncresc: Crescimento 5 anos'
          )


def get_cotacao(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['Cotacao'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_pl(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['P/L'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_pvp(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['P/VP'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_psr(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['PSR'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_dy(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['DY'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_pativo(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['P/Ativo'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_pcapgiro(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['P/Cap.Giro'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_pebit(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['P/EBIT'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_pacl(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['P/ACL'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_evebit(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['EV/EBIT'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_evebitda(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['EV/EBITDA'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_mrgebita(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['Mrg.Ebit'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_mrgliq(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['Mrg.Liq.'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_liqcor(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['Liq.Corr.'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_roic(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['ROIC'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_roe(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['ROE'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_liqd(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['Liq.2meses'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_patliq(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['Pat.Liq'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_divpatr(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['Div.Brut/Pat.'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_cresc(market, crescente):
    aux = {}
    for key, value in market.items():
        aux[key] = (value['Cresc.5anos'])

    if crescente == 1:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1], reverse=True)}

    if crescente == 0:
        aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}

    return aux


def get_indicator(key, market, crescente):
    if key == 'cotacao':
        get_cotacao(market, crescente)

    if key == 'pl':
        get_pl(market, crescente)

    if key == 'pvp':
        get_pvp(market, crescente)

    if key == 'psr':
        get_psr(market, crescente)

    if key == 'dy':
        get_dy(market, crescente)

    if key == 'pativo':
        get_pativo(market, crescente)

    if key == 'pcapgiro':
        get_pcapgiro(market, crescente)

    if key == 'pebit':
        get_pebit(market, crescente)

    if key == 'pacl':
        get_pacl(market, crescente)

    if key == 'evebit':
        get_evebit(market, crescente)

    if key == 'evebitda':
        get_evebitda(market, crescente)

    if key == 'mrgebita':
        get_mrgebita(market, crescente)

    if key == 'mrgliq':
        get_mrgliq(market, crescente)

    if key == 'liqcor':
        get_liqcor(market, crescente)

    if key == 'roic':
        get_roic(market, crescente)

    if key == 'roe':
        get_roe(market, crescente)

    if key == 'liqd':
        get_liqd(market, crescente)

    if key == 'patliq':
        get_patliq(market, crescente)

    if key == 'divpatr':
        get_divpatr(market, crescente)

    if key == 'cresc':
        get_cresc(market, crescente)


""" 

Selecionar melhores ações:

Analisa um indicador
Marca os pontos daquele indicador perante aos melhores indicadores. Quanto mais alto, melhor. Ou seja, mais pontos.
Quanto mais baixo, pior, ou seja, perde pontos.
No final, aquele que ficar com um saldo positivo entre os melhores indicadores, é selecionado como uma boa ação.
Alguns critérios devem ser levados em consideração com mais peso que outros. Ex: Dívidas.
Existirá também uma escala de melhores indicadores.

Mesclar indicadores: (MAIS FÁCIL)

Analisa apenas dois indicadores. Se os indicadores selecionados forem maiores, mais pontos.
Se os indicadores forem menores, menos pontos(ou subtraem).
Levar em conta também critérios universais como muito endividamento.


"""

if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    from waitingbar import WaitingBar

    # filename = 'fundamentus_' + str(date.today())
    # infile = open(filename, 'rb')
    # reade = pickle.load(infile)
    # infile.close()

    progress_bar = WaitingBar('[*] Downloading...')
    result = get_data()
    progress_bar.stop()

    print('get_cotacao(result)')
    for j, i in get_cotacao(result, 1).items():
        print(j, i)

    # print('get_pl(result)')
    # for j, i in get_pl(result, 1).items():
    # print(j, i)
    # print('get_pvp(result)')
    # for j, i in get_pvp(result, 1).items():
    # print(j, i)
    # print('get_psr(result)')
    # for j, i in get_psr(result, 1).items():
    # print(j, i)
    # print('get_dy(result)')
    # for j, i in get_dy(result, 1).items():
    # print(j, i)
    # print('get_pativo(result)')
    # for j, i in get_pativo(result, 1).items():
    # print(j, i)
    # print('get_pcapgiro(result)')
    # for j, i in get_pcapgiro(result, 1).items():
    # print(j, i)
    # print('get_pebit(result)')
    # for j, i in get_pebit(result, 1).items():
    # print(j, i)
    # print('get_pacl(result)')
    # for j, i in get_pacl(result, 1).items():
    # print(j, i)
    # print('get_evebit(result)')
    # for j, i in get_evebit(result, 1).items():
    # print(j, i)
    # print('get_evebitda(result)')
    # for j, i in get_evebitda(result, 1).items():
    # print(j, i)
    # print('get_mrgebita(result)')
    # for j, i in get_mrgebita(result, 1).items():
    # print(j, i)
    # print('get_mrgliq(result)')
    # for j, i in get_mrgliq(result, 1).items():
    # print(j, i)
    # print('get_liqcor(result)')
    # for j, i in get_liqcor(result, 1).items():
    # print(j, i)
    # print('get_roic(result)')
    # for j, i in get_roic(result, 1).items():
    # print(j, i)
    # print('get_roe(result)')
    # for j, i in get_roe(result, 1).items():
    # print(j, i)
    # print('get_liqd(result)')
    # for j, i in get_liqd(result, 1).items():
    # print(j, i)
    # print('get_patliq(result)')
    # for j, i in get_patliq(result, 1).items():
    # print(j, i)
    # print('get_divpatr(result)')
    # for j, i in get_divpatr(result, 1).items():
    # print(j, i)
    # print('get_cresc(result)')
    # for j, i in get_cresc(result, 1).items():
    # print(j, i)

    # get_indicators()

    # print(get_indicator('pvp'))                    

    # print('sucesso')
    # outfile = open(filename, 'wb')
    # pickle.dump(result, outfile)
    # outfile.close()

    # print(reade==result)
    # texta =  colored('Hello', 'red')
