from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import json
import datetime
import dateutil.relativedelta
import sys
sys.path.insert(0, './models/')
from models.solutionsClassifier import SolutionsClassifier
sys.path.insert(0, './metrics/')
from metrics.dataCollector import DataCollector
from metrics.transactions import Transactions

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

"""
    Como há dados fornecidos pelo Open Finance, como dados de receita e financiamento,
    que não são fornecidos no sandbox da Pluggy, criamos algumas APIs, para uso nesse hackathon.
    Para fazê-las, utilizamos tanto materiais na internet sobre dados fornecidos pelo Open Finance,
    quanto os exemplos de retornos fornecidos pelas APIs da Pluggy (PRODUCTS em https://docs.pluggy.ai/docs/)
"""

@app.route("/financings/<clientId>")
def getFinancings(clientId):
    """
        API retorna dados de pagamentos de financiamentos feitos pelo cliente.
        Para o retorno dessa API, utilizamos um formato parecido com a API de transactions,
        disponível com o sandbox da Pluggy.
    """
    financingsPayments = {
        "total": 2,
        "totalPages": 1,
        "page": 1,
        "results": [
            {
                "id": "d3434-2343-7878-a4534-032h72343423k",
                "paymentDate": "2022-06-13T03:00:00.000Z",
                "amount": 235,
                "currencyCode": "BRL",
            },
            {
                "id": "d45gf-dfg43-7845678-d675-so83n9ds9",
                "paymentDate": "2022-07-13T03:00:00.000Z",
                "amount": 572,
                "currencyCode": "BRL",
            },
            {
                "id": "aa3f2f-fhhy345-dfh34234-4563g-sdf872jn",
                "paymentDate": "2022-08-13T03:00:00.000Z",
                "amount": 1235,
                "currencyCode": "BRL",
            },
            {
                "id": "aa3f2f-fhhy345-dfh34234-4563g-sdf872jn",
                "paymentDate": "2022-09-13T03:00:00.000Z",
                "amount": 835,
                "currencyCode": "BRL",
            },
        ]
    }
    
    return financingsPayments

@app.route("/loans/<clientId>")
def getLoans(clientId):
    """
        API retorna dados de pagamentos de empréstimos feitos pelo cliente.
        Para o retorno dessa API, utilizamos um formato parecido com a API de transactions,
        disponível com o sandbox da Pluggy.
    """
    loansPayments = {
        "total": 2,
        "totalPages": 1,
        "page": 1,
        "results": [
            {
                "id": "d3434-2343-7878-a4534-032h72343423k",
                "paymentDate": "2022-07-25T03:00:00.000Z",
                "amount": 334,
                "currencyCode": "BRL",
            },
            {
                "id": "d45gf-dfg43-7845678-d675-so83n9ds9",
                "paymentDate": "2022-06-25T03:00:00.000Z",
                "amount": 122,
                "currencyCode": "BRL",
            },
            {
                "id": "aa3f2f-fhhy345-dfh34234-4563g-sdf872jn",
                "paymentDate": "2022-08-25T03:00:00.000Z",
                "amount": 784,
                "currencyCode": "BRL",
            },
            {
                "id": "aa3f2f-fhhy345-dfh34234-4563g-sdf872jn",
                "paymentDate": "2022-09-25T03:00:00.000Z",
                "amount": 963,
                "currencyCode": "BRL",
            },
        ]
    }
    
    return loansPayments


@app.route("/classifier/clientSecret=<clientSecret>/clientId=<clientId>/accountId=<accountId>/itemId=<itemId>")
def generateClientSolutionsClassifier(clientSecret, clientId, accountId, itemId):
    '''
        Função principal da API. Recebe dados de Ids do cliente e retorna as possíveis soluções.
        Para mais detalhes sobre a implementação, veja o método defineCustomerSolutionsPortfolio
        da classe SolutionsClassifier, que é chamado por essa função.
    '''

    clientSolutionsClassifier = SolutionsClassifier()

    dataCollector = DataCollector(clientSecret, clientId)

    clientTransactions = Transactions(clientSecret, clientId)

    print(clientTransactions.clientSecret)

    solutionsList = clientSolutionsClassifier.defineCustomerSolutionsPortfolio(clientSecret, clientId, accountId, itemId)
    print("solutionsList")
    print(solutionsList)

    return solutionsList