
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

def exibir_dados():
    pagina = page('https://www.rottentomatoes.com/browse/tv-list-1')
    soup = BeautifulSoup(pagina,'html5lib')
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






