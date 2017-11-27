from selenium import webdriver
import sqlite3
import requests


from bs4 import BeautifulSoup

def pagina():
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get('https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi')
    saida = browser.page_source

    browser.close()







    return saida

def scraping():
    pag = pagina()
    bsObj = BeautifulSoup(pag,"html5lib")

    temperatura = bsObj.find(attrs={'id': 'momento-temperatura'})

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
temp = str(scraping())

inserindo_dado(temp)

print(exibindo_temperaturas())