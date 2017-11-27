import sqlite3
import requests
from bs4 import BeautifulSoup


def page(url):
    page = None

    try:
        link = requests.get(url)

        page = link.text

    except requests.exceptions.RequestException as e:
        print('erro: ',e.reason)

    return page


def pegar_temperatura():
    pagina = page('https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi')
    soup = BeautifulSoup(pagina,'html5lib')
    temperatura = soup.find(attrs={'id':'momento-temperatura'})
    return temperatura.text



def banco():
    con = sqlite3.connect('dados.db')


    return con
def tabela():
    con =banco()

    cursor = con.cursor()

    try:

        cursor.execute('create table if not exists dados_temperatura('
                   'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                   'temperatura VARCHAR(50));')


    except sqlite3.DataError as e:
        print(e)
    return con

def quantidade_registros():
    con = banco()
    valor = con.cursor().execute("SELECT COUNT(*) FROM dados_temperatura")
    return valor.fetchone()[0]
def menor_registro():
    con = banco()
    linha1 = con.cursor().execute("SELECT MIN(id) FROM dados_temperatura")
    menor_id = linha1.fetchone()[0]
    return menor_id

def exibindo_temperaturas():
    con = banco()
    dados = con.cursor().execute("SELECT temperatura FROM dados_temperatura")

    return dados.fetchall()

def inserindo_dado(temp):
    con = tabela()
    cursor = con.cursor()
    qde = quantidade_registros()
    valor_id = str(menor_registro())



    if qde>=5:
        cursor.execute("DELETE FROM dados_temperatura WHERE id='"+valor_id+"'")

    cursor.execute("INSERT INTO dados_temperatura (temperatura) values ('"+temp+"')")
    con.commit()

    con.close()





tabela()
temp = str(pegar_temperatura())

inserindo_dado(temp)

print(exibindo_temperaturas())




