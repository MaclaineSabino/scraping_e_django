import requests
from bs4 import BeautifulSoup
import time
import re
import sqlite3


lista_paises = []

def banco():
    con = sqlite3.connect('dados.db')


    return con
def tabela():
    con =banco()

    cursor = con.cursor()

    try:

        cursor.execute('create table if not exists densidade('
                   'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                   'pais VARCHAR(50),'
                   'area DOUBLE,'
                   'populacao DOUBLE,'
                   'densidade VARCHAR(100));')


    except sqlite3.DataError as e:
        print(e)
    return con


def inserindo_dado(pais_vl,area_vl,populacao_vl,densidade_vl):
    con = tabela()
    cursor = con.cursor()






    cursor.execute("INSERT INTO densidade(pais,area,populacao,densidade) VALUES('"+pais_vl+"',+"+area_vl+",+"+populacao_vl+",+"+densidade_vl+")")
    con.commit()

    con.close()


def limpando_tabela():
    con = tabela()
    cursor = con.cursor()

    try:
        cursor.execute("DELETE FROM densidade")



    except sqlite3.DataError as e:
        print(e)
def page(url):
    page = None

    try:
        link = requests.get(url)

        page = link.text

    except requests.exceptions.RequestException as e:
        print('erro: ',e.reason)

    return page

def pegando_bs(link):
    pagina = page(link)
    bsObj = BeautifulSoup(pagina, 'html5lib')

    return bsObj


def pegando_links(bsObj):
    sites = []

    links = bsObj.find('tbody').findAll("a")
    for lista in links:
        if 'href' in lista.attrs:
            sites.append(lista.attrs['href'])


    return sites

def retorna_numero_area(valor):
    filtro = re.compile('([0-9]+)')
    num = valor.replace(",","")
    numero = filtro.findall((num))
    return numero[0]

def retorna_numero_populacao(valor):
    numero = valor.replace(",","")
    return numero

def retorna_densidade(populacao,area):
    populacao = int(populacao)
    area = float(area)
    if area==0:
        densidade=0
    else:
        densidade = populacao/area
    return densidade

def pegando_conteudo(subdominio):






    endereco = "http://example.webscraping.com/"+subdominio

    print(endereco)

    bsobj = pegando_bs(endereco)



    lis = pegando_links(bsobj)

    for link in lis:
        pagina = page("http://example.webscraping.com/" +link)
        bsObj = BeautifulSoup(pagina, 'html5lib')

        area = bsObj.find(attrs={"id":"places_area__row"}).find(attrs={"class":"w2p_fw"})
        populacao = bsObj.find(attrs={"id":"places_population__row"}).find(attrs={"class":"w2p_fw"})
        pais = bsObj.find(attrs={"id": "places_country__row"}).find(attrs={"class": "w2p_fw"})

        area_te = retorna_numero_area(area.text)
        populacao_te = retorna_numero_populacao(populacao.text)
        densidade =str(retorna_densidade(populacao_te,area_te))

        inserindo_dado(pais.text,area_te,populacao_te,densidade)

        dados={"pais":pais.text,
               "area":area_te,
               "populacao":populacao_te,
               "densidade_populacional":densidade,}
        lista_paises.append(dados)
        time.sleep(2)



    print(lista_paises)






    paginacao = bsobj.find(attrs={"id":"pagination"}).findAll('a')



    for pag in paginacao:


        if 'Next' in pag.text:
            ancora = pag.attrs['href']



            pegando_conteudo(ancora)


        
    return lista_paises
#limpando_tabela()
pegando_conteudo("places/default/index/0")