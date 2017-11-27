from django.shortcuts import render,get_object_or_404,redirect
import re, time

import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
#---------------------------------------------------------------------------------------------
#questão 1
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

#-------------------------------------------------------------------------------------------------------
#questao 02


csvFile = open("arquivo.csv",'wt')
writer = csv.writer(csvFile,delimiter=';')
writer.writerow(['filme', 'valor arrecadado', 'valor acumulado','número de semanas no ranking'])

def exibir_dados2():
    pagina = page('http://www.imdb.com/chart/boxoffice')
    soup = BeautifulSoup(pagina,'html5lib')
    filmes = soup.find_all('tr')

    return filmes


def lista_dic_2():
    dicionarios = []

    lista = exibir_dados2()
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

listao =lista_dic_2()
try:
    for dic in listao:
        print(dic)
        writer.writerow([dic['filme'],dic['valor_arrecadado'],dic['valor_acumulado'], dic['numero_semanas_no_ranking']])

finally:
    csvFile.close()


#-------------------------------------------------------------------------------------------------------------------
# questão 3



def pegar_temperatura():
    pagina = page('https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi')
    soup = BeautifulSoup(pagina,'html5lib')
    temperatura = soup.find(attrs={'id':'momento-temperatura'})
    print(temperatura.text)
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

    lista_temp = []
    con = banco()
    dados = con.cursor().execute("SELECT temperatura FROM dados_temperatura")
    for temp in dados:

        tmp = str(temp)
        valor = tmp[2:5]



        lista_temp.append(valor)


    return lista_temp

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








#-----------------------------------------------------------------------------------------------------------------------
#questão 04

def exibindo_densidades():

    lista = []

    conex  = banco()

    cursor = conex.cursor()

    dados = cursor.execute("SELECT * FROM densidade")

    for data in dados:
        lista.append(data)

    return lista

#----------------------------------------------------------------------------------------------------------------------

#questão 05

def calculando_total(link):
    pagina = page(link)

    total = 0
    bsObj = BeautifulSoup(pagina,'xml')





    dados = bsObj.findAll("empreendimento")



    for dado in dados:
        valor = dado.find("valorTotalPrevisto")
        percentual = dado.find("valorPercentualExecucaoFisica")
        if(valor is not None and percentual is not None):
            calculo = float(valor.text)*(float(percentual.text)/100)
            total = float(total)+calculo



    return total




#------------------------------------------------------------------------------------------------------------------
#questão 6
def exibindo_despesas_estados():

    lista = []

    conex  = banco()

    cursor = conex.cursor()

    dados = cursor.execute("SELECT nome,sum(despesas) FROM estados GROUP BY nome")

    for data in dados:
        lista.append(data)

    return lista


#-------------------------------------------------------------------------------------------------



def index(request):

    return render(request,'index.html',{})

def questao_um(request):
    listao = lista_dic()

    return render(request, 'questao1.html',{'dados_filme':listao})

def questao_dois(request):
    lista = lista_dic_2()

    return render(request, 'questao2.html',{'dados_filme':lista})

def questao_tres(request):
    tabela()
    temp = str(pegar_temperatura())

    inserindo_dado(temp)
    temperaturas = exibindo_temperaturas()

    return render(request,'questao3.html',{'temperaturas':temperaturas })

def questao_quatro(request):

    densidades = exibindo_densidades()



    return render(request,'questao4.html',{'densidades':densidades})

def questao_cinco(request):

    total = calculando_total('http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento')

    return render(request,'questao5.html',{'total':total})


def questao_seis(request):

    despesas = exibindo_despesas_estados()

    return render(request,'questao6.html',{'despesas':despesas})