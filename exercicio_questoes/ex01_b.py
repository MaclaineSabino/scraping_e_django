from selenium import webdriver
import sqlite3



from bs4 import BeautifulSoup

def pagina():
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get('https://www.rottentomatoes.com/browse/tv-list-1')
    saida = browser.page_source

    browser.close()







    return saida


def exibir_dados():
    pagin = pagina()
    soup = BeautifulSoup(pagin,'html5lib')
    filmes = soup.find_all(attrs={'class':'tvTopListTitle'})
    return filmes

def lista_dic():
    dicionarios = []

    lista = exibir_dados()



    for filme in lista:
        titulo = filme.find(attrs={'class':'middle_col'})
        titulo2 = titulo.find('a')
        avaliac = filme.find(attrs={'class':'left_col'})
        avaliac2 = avaliac.find('a')
        avaliac3 = avaliac2.find(attrs={'class':'tMeterScore'})

        texto = str(avaliac3)[26:30]

        tamanho = len(texto)

        if(tamanho>0) and (texto[tamanho-1]=="<"):
            texto = texto.replace(texto[tamanho-1],"")




        dicionario={'filme':titulo2.text,
                    'avaliacao':texto,
                    }
        dicionarios.append(dicionario)

    return dicionarios

listao =lista_dic()

for fil in listao:
    print(fil)