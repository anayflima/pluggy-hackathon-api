import numpy as np
import requests
from datetime import date, datetime
import json
import dateutil.relativedelta
from dataCollector import DataCollector

class Debts(DataCollector):

    def getCurrentFinancings(self, clientId):
        """
            Função pega os financiamentos do cliente e seleciona aqueles
            que não foram pagos (cuja data de pagamento é maior que a data atual),
            para devolver os financiamentos atuais do cliente
        """
        requestUrl = self.hackathonPluggyUrl + "financings/{clientId}".format(clientId = clientId)

        response = requests.request("GET", requestUrl)
        
        responseJson = response.json()

        now = datetime.now()

        sumFinancings = 0

        for item in responseJson['results']:
            paymentDate = item['paymentDate']
            paymentDateObject = datetime.strptime(paymentDate, '%Y-%m-%dT%H:%M:%S.000Z')

            if (paymentDateObject > now): # se o financiamento ainda não foi pago
                sumFinancings += item['amount']

        return sumFinancings
    
    def getCurrentLoans(self, clientId):
        """
            Função pega os empréstimos do cliente e seleciona aqueles
            que não foram pagos (cuja data de pagamento é maior que a data atual),
            para devolver os empréstimos atuais do cliente
        """

        requestUrl = self.hackathonPluggyUrl + "loans/{clientId}".format(clientId = clientId)

        response = requests.request("GET", requestUrl)
        
        responseJson = response.json()

        now = datetime.now()

        sumLoans = 0
        
        for item in responseJson['results']:
            paymentDate = item['paymentDate']
            paymentDateObject = datetime.strptime(paymentDate, '%Y-%m-%dT%H:%M:%S.000Z')

            if (paymentDateObject > now): # se o financiamento ainda não foi pago
                sumLoans += item['amount']

        return sumLoans
    
    def calculateGrossDebt(self, clientId):
        """
            Função devolve a dívida bruta do cliente.
            Dívida bruta é a soma dos financiamentos e empréstimos de uma empresa,
            tanto de curto como de longo prazo
        """
        financings = self.getCurrentFinancings(clientId)
        loans = self.getCurrentLoans(clientId)

        grossDebt = financings + loans

        return grossDebt
