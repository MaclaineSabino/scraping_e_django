import csv
import requests
from bs4 import BeautifulSoup

csvFile = open("arquivo.csv",'wt')
writer = csv.writer(csvFile,delimiter=';')
writer.writerow(['filme', 'valor arrecadado', 'valor acumulado','número de semanas no ranking'])


def page(url):
    page = None

    try:
        link = requests.get(url)

        page = link.text

    except requests.exceptions.RequestException as e:
        print('erro: ',e.reason)

    return page

def exibir_dados():
    pagina = page('http://www.imdb.com/chart/boxoffice')
    soup = BeautifulSoup(pagina,'html5lib')
    filmes = soup.find_all('tr')

    return filmes


def lista_dic():
    dicionarios = []

    lista = exibir_dados()
    tamanho = len(lista)

    del lista[tamanho-1]
    del lista[tamanho-2]
    del lista[0]



    for filme in lista:
        titulo_html = filme.find(attrs={'class':'titleColumn'})
        titulo_text = titulo_html.find('a')

        valor_arrecadado = str(filme.find(attrs={'class':'ratingColumn'}))
        valor_filtrado = valor_arrecadado.split("\n")



        valor_acumulado = filme.find(attrs={'class':'secondaryInfo'})

        numero_semanas_ranking = filme.find(attrs={'class':'weeksColumn'})



        dicionario={'filme':titulo_text.text,
                    'valor_arrecadado':valor_filtrado[1].strip(),
                    'valor_acumulado':valor_acumulado.text,
                    'numero_semanas_no_ranking':numero_semanas_ranking.text,
                    }
        dicionarios.append(dicionario)

    return dicionarios

listao =lista_dic()
try:
    for dic in listao:
        print(dic)
        writer.writerow([dic['filme'],dic['valor_arrecadado'],dic['valor_acumulado'], dic['numero_semanas_no_ranking']])

finally:
    csvFile.close()




