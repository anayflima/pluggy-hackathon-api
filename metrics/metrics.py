import numpy as np
import requests
from datetime import date, datetime
import json
import dateutil.relativedelta
from dataCollector import DataCollector
from transactions import Transactions
from debts import Debts

class Metrics():
    
    def calculateCashOnEBITDA(self, accountId, itemId):
        """
            Função calcula a razão entre caixa da empresa e EBITDA
            Com isso, queremos obter uma estimativa de se a empresa possui ou não receita recorrente.
        """

        clientTransactions = Transactions()
        cash = clientTransactions.getCash(itemId)
        # print("cash = " + str(cash))
        EBITDA = clientTransactions.getEBITDA(accountId)
        # print("EBITDA = " + str(EBITDA))
        cashOnEBITDA = cash/EBITDA
        return cashOnEBITDA
    
    def calculateIncomeVolatility(self, accountId):
        """
            Função calcula a volatilidade da receita do último ano da empresa.
            Com isso, queremos obter uma estimativa de se a empresa possui ou não receita recorrente.
            Para podermos comparar soluções, usaremos o coeficiente de variação (uma espécie de
            "desvio padrão relativo", que é obtido dividindo o desvio padrão absoluto pela média dos valores.
        """
        clientTransactions = Transactions()
        positiveTransactionsByMonth = clientTransactions.getPositiveTransactionsByMonth(accountId)

        montlyIncomesList = list(positiveTransactionsByMonth.values())

        # print(montlyIncomesList)

        absoluteAverageMontlyIncomes = abs(sum(montlyIncomesList) / len(montlyIncomesList))

        standartDeviationMontlyIncomes = np.std(montlyIncomesList)

        coefficientOfVariation = standartDeviationMontlyIncomes / absoluteAverageMontlyIncomes

        return coefficientOfVariation
    
    def calculateLeverave(self, clientId, accountId):
        """
            Função calcula a alavancagem da empresa, usando a seguinte fórmula:
            Alavancagem = (dívida líquida) / EBITDA = (dívida bruta - caixa) / EBITDA,
            sendo EBITDA a soma das transações positivas (o que entrou)
            e as transações negativas (o que saiu).
        """
        clientTransactions = Transactions()
        clientDebts = Debts()

        EBITDA = clientTransactions.getEBITDA(accountId)

        # print(EBITDA)

        grossDebt = clientDebts.calculateGrossDebt(clientId)

        # print(grossDebt)

        cash = clientTransactions.getCash(clientId)
        
        netDebt = grossDebt - cash

        # print(netDebt)

        leverage = netDebt / EBITDA

        return leverage