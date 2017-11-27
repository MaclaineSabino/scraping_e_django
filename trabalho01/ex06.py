import requests
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sqlite3
def banco():
    con = sqlite3.connect('dados.db')


    return con
def tabela():
    con =banco()

    cursor = con.cursor()

    try:

        cursor.execute('create table if not exists estados('
                   'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                   'nome VARCHAR(50),'
                    'despesas DOUBLE);')


    except sqlite3.DataError as e:
        print(e)
    return con

def limpando_tabela():
    con = tabela()
    cursor = con.cursor()

    try:
        cursor.execute("DELETE FROM estados")
        con.commit()
        con.close()



    except sqlite3.DataError as e:
        print(e)

def inserindo_dados(sede,despesas):
    con = tabela()
    cursor = con.cursor()

    try:

        cursor.execute("INSERT INTO estados(nome,despesas) VALUES('"+sede+"',+"+despesas+")")


    except sqlite3.DataError as e:
        print(e)
    con.commit()
    con.close()

def page(url):
    page = None

    try:
        link = urlopen(url).read()

        page = link

    except requests.exceptions.RequestException as e:
        print('erro: ',e.reason)

    return page




def pegando_unidades(link):
    limpando_tabela()
    pagina = page(link)


    bsObj = BeautifulSoup(pagina,'xml')






    dados = bsObj.findAll("empreendimento")

    for dado in dados:
        unidade_sede  = dado.find("cidadeSede")
        valor_previsto = dado.find("valorTotalPrevisto")
        percentual = dado.find("valorPercentualExecucaoFisica")
        nome = unidade_sede.find("nome")
        if (nome is not None and valor_previsto is not None and percentual is not None):
            valor_gasto = float(valor_previsto.text)*(float(percentual.text)/100)
            cid = nome.text
            vl = str(valor_gasto)
            inserindo_dados(cid, vl)






def exibindo_dados():
    con = banco()
    cursor = con.cursor()
    dados = cursor.execute("SELECT nome,SUM(despesas) FROM estados GROUP BY nome")
    return dados.fetchall()

def salvando_csv(dados):
    resp = input('Deseja salvar em arquivo csv? (s/n)')

    if resp == 's':
        csvFile = open("gastos_ufs.csv", 'wt')
        writer = csv.writer(csvFile, delimiter=';')
        writer.writerow(['UF', 'VALOR GASTO'])

        for dic in dados:
            print(dic)
            writer.writerow(
                dic)
    elif resp =='n':
        pass
    else:
        print('você digitou uma opção inválida')





tabela()
valorTotal = pegando_unidades('http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento')

resultados = exibindo_dados()
salvando_csv(resultados)
