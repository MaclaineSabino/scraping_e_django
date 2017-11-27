import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

def page(url):
    page = None

    try:
        link = urlopen(url).read()

        page = link

    except requests.exceptions.RequestException as e:
        print('erro: ',e.reason)

    return page




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

valorTotal = calculando_total('http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento')
print("o valor total gasto foi de: R$ ",(valorTotal))

