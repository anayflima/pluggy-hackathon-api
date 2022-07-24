import numpy as np
import requests
from datetime import date, datetime
import json
import dateutil.relativedelta
from dataCollector import DataCollector

class Transactions(DataCollector):

    def getCash(self, itemId):
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

        # print(responseJson)

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

    def getTotalMonthlyTransactions(self, accountId):

        responseJson = self.getTransactions(accountId)

        now = datetime.now()
        
        dateAMonthAgo = (now + dateutil.relativedelta.relativedelta(months=-1))

        sumTransactions = 0

        for item in responseJson['results']:
            transactionDate= item['date']
            transactionDateObject = datetime.strptime(transactionDate, '%Y-%m-%dT%H:%M:%S.000Z')

            if (transactionDateObject > dateAMonthAgo): # se a transação foi de um mês atrás para frente
                sumTransactions += item['amount']
        
        return sumTransactions
    
    def getPositiveTransactionsByMonth(self, accountId):
        responseJson = self.getTransactions(accountId)
        now = datetime.now()

        dateAYearAgo = (now + dateutil.relativedelta.relativedelta(months=-12))

        transactionsByMonth = {}

        # print(responseJson)

        for item in responseJson['results']:
            transactionDate = item['date']
            transactionAmount = item['amount']
            transactionDateObject = datetime.strptime(transactionDate, '%Y-%m-%dT%H:%M:%S.000Z')
            # se a transação é positiva e se foi de um ano atrás para frente
            if (abs(transactionAmount) > 0 and transactionDateObject > dateAYearAgo):
                # separar por mês
                month = str(transactionDateObject.month)
                if month in transactionsByMonth:
                    transactionsByMonth[month] += transactionAmount
                else:
                    transactionsByMonth[month] = transactionAmount
        
        return transactionsByMonth
    
