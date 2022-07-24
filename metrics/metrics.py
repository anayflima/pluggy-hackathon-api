import numpy as np
import requests
import os
from datetime import date, datetime
import json
import dateutil.relativedelta
from metrics.dataCollector import DataCollector
from metrics.transactions import Transactions
from metrics.debts import Debts

class Metrics():
    
    def calculateCashOnEBITDA(self, accountId, itemId, clientSecret, clientId):
        """
            Função calcula a razão entre caixa da empresa e EBITDA
            Com isso, queremos obter uma estimativa de se a empresa possui ou não receita recorrente.

            Se o caixa for menor do que zero, consideraremos como zero, para que o valor negativo
            não distorça o algoritmo (por exemplo, se caixa e EBITDA forem menores do que zero,
            a razão dará positiva, o que criará a falsa sensação de que a empresa tem um bom caixa
            em relação ao seu retorno e pode investi-lo em novas atividades. Faremos algo semelhante
            com o EBITDA, mas, como este não pode ser zero pois é denominador de função, atribuiremos
            o valor 1, de forma que a razão será igual ao caixa nesse caso.
            Tais atribuições não serão prejudiciais ao algoritmo, já que elas continuarão
            mais próximas de soluções que possuem baixo caixa e lucro.
        """

        clientTransactions = Transactions(clientSecret, clientId)
        
        cash = clientTransactions.getCash(itemId)

        EBITDA = clientTransactions.getEBITDA(accountId)

        # Remoção de valores negativos das variáveis
        if (EBITDA <= 0):
            EBITDA = 1
        
        if (cash < 0):
            cash = 0

        cashOnEBITDA = cash/EBITDA
        return cashOnEBITDA
    
    def calculateIncomeVolatility(self, accountId, clientSecret, clientId):
        """
            Função calcula a volatilidade da receita do último ano da empresa.
            Com isso, queremos obter uma estimativa de se a empresa possui ou não receita recorrente.
            Para podermos comparar soluções, usaremos o coeficiente de variação (uma espécie de
            "desvio padrão relativo", que é obtido dividindo o desvio padrão absoluto pela média dos valores.
        """
        clientTransactions = Transactions(clientSecret, clientId)
        positiveTransactionsByMonth = clientTransactions.getPositiveTransactionsByMonth(accountId)

        montlyIncomesList = list(positiveTransactionsByMonth.values())

        absoluteAverageMontlyIncomes = abs(sum(montlyIncomesList) / len(montlyIncomesList))

        standartDeviationMontlyIncomes = np.std(montlyIncomesList)

        coefficientOfVariation = standartDeviationMontlyIncomes / absoluteAverageMontlyIncomes

        return coefficientOfVariation
    
    def calculateLeverave(self, clientId, accountId, clientSecret):
        """
            Função calcula a alavancagem da empresa, usando a seguinte fórmula:
            Alavancagem = (dívida líquida) / EBITDA = (dívida bruta - caixa) / EBITDA,
            sendo EBITDA a soma das transações positivas (o que entrou)
            e as transações negativas (o que saiu).
        """
        clientTransactions = Transactions(clientSecret, clientId)
        clientDebts = Debts(clientSecret, clientId)

        EBITDA = clientTransactions.getEBITDA(accountId)

        grossDebt = clientDebts.calculateGrossDebt(clientId)

        cash = clientTransactions.getCash(clientId)
        
        netDebt = grossDebt - cash

        leverage = netDebt / EBITDA

        return leverage