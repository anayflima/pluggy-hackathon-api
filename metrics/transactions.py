import numpy as np
import requests
from datetime import date, datetime
import json
import dateutil.relativedelta
from metrics.dataCollector import DataCollector

class Transactions(DataCollector):

    def getCash(self, itemId):
        """
            Função retorna o valor, em dinheiro, que a companhia tem em sua conta.
            Valor obtido por meio de chamada de API da Pluggy
        """
        requestUrl = self.pluggyUrl + "accounts?itemId={itemId}".format(itemId = itemId)

        payload = ""
        headers = {
            'X-API-KEY': self.APIKey
        }
        response = requests.request("GET", requestUrl, headers=headers, data=payload)
        
        responseJson = response.json()

        balance = 0
        
        for item in responseJson['results']:
            balance += item['balance']
        
        return balance
    
    def getTransactions(self, accountId):
        """
            Função retorna todas as transações de determinada conta de um cliente,
            por meio de chamada de API da Pluggy
        """
        requestUrl = self.pluggyUrl + "transactions?accountId={accountId}".format(accountId = accountId)

        payload = ""
        headers = {
            'X-API-KEY': self.APIKey
        }
        response = requests.request("GET", requestUrl, headers=headers, data=payload)
        
        responseJson = response.json()
        return responseJson
    
    def getEBITDA(self, accountId):
        """
            Estima o EBITDA anual da empresa, somando todas as suas transações negativas e positivas,
            a fim de obter uma métrica dos lucros que a empresa obteve.
        """

        responseJson = self.getTransactions(accountId)

        now = datetime.now()

        dateAYearAgo = (now + dateutil.relativedelta.relativedelta(months=-12))

        sumTransactions = 0

        for item in responseJson['results']:
            transactionDate = item['date']
            transactionDateObject = datetime.strptime(transactionDate, '%Y-%m-%dT%H:%M:%S.000Z')

            if (transactionDateObject > dateAYearAgo): # se a transação foi de um ano atrás para frente
                sumTransactions += item['amount']

        return sumTransactions
    
    def getMensalIncome(self, accountId):
        """
            Estima o rendimento mensal, baseando-se em todas as transações positivas feitas no mês.
        """

        responseJson = self.getTransactions(accountId)

        sumPositiveTransactions = 100

        for item in responseJson['results']:
            if (item['amount'] > 0):
                sumPositiveTransactions += item['amount']

        return sumPositiveTransactions

    def getTotalLastMonthTransactions(self, accountId):
        """
            Função retorna todas as transações de determinada conta de um cliente
            feitas no último mês (transações de um més atrás para frente)
        """

        responseJson = self.getTransactions(accountId)

        now = datetime.now()
        
        dateAMonthAgo = (now + dateutil.relativedelta.relativedelta(months=-1))

        sumTransactions = 0

        for item in responseJson['results']:
            transactionDate= item['date']
            transactionDateObject = datetime.strptime(transactionDate, '%Y-%m-%dT%H:%M:%S.000Z')

            # se a transação foi de um mês atrás para frente
            if (transactionDateObject > dateAMonthAgo):
                sumTransactions += item['amount']
        
        return sumTransactions
    
    def getPositiveTransactionsByMonth(self, accountId):
        """
            Função retorna todas as transações positivas do último ano
            de determinada conta de um cliente separadas por mês.
            O formato de devolução é um dicionário cujas chaves
            são os meses e os valores o total de transações naquele mês
        """
        responseJson = self.getTransactions(accountId)
        now = datetime.now()

        dateAYearAgo = (now + dateutil.relativedelta.relativedelta(months=-12))

        transactionsByMonth = {}

        for item in responseJson['results']:
            transactionDate = item['date']
            transactionAmount = item['amount']
            transactionDateObject = datetime.strptime(transactionDate, '%Y-%m-%dT%H:%M:%S.000Z')

            # se a transação é positiva e se foi de um ano atrás para frente, separar por mês
            if (abs(transactionAmount) > 0 and transactionDateObject > dateAYearAgo):
                month = str(transactionDateObject.month)
                if month in transactionsByMonth:
                    transactionsByMonth[month] += transactionAmount
                else:
                    transactionsByMonth[month] = transactionAmount
        
        return transactionsByMonth
    
