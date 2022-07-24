import sys
import os
from metrics.metrics import Metrics
from metrics.transactions import Transactions
import pandas as pd
import numpy as np
import requests
from operator import itemgetter
import math

class MetricsClassifier:
    def __init__(self):
        pass
    def calculateSigmoid(self, x):
        """
            Aplica e retorna a função sigmóide para valores positivos.
            Para valores negativos, devolve zero, já que estamos normalizando
            a variável de 0 a 1.
        """
        if (x > 0):
            return 1/(1+np.exp(-(1/x)))
        else:
            return 0
    
    def calculateCashOnEBITDAPosition(self, accountId, itemId, clientSecret, clientId):
        """
            Quanto maior a proporção de caixa em relação ao EBITDA, mais dinheiro a
            empresa tem disponível em relação ao seus lucros. Com base nisso,
            mapearemos qual a reserva de emergência da empresa e se é um provável
            bom momento ou não para investir em novas soluções dentro do negócio.

            Para normalizar os valores da proporção para valores entre 0 e 1, usaremos a função sigmóide.
            Como essa função tem uma curva acentuada, trata-se de uma boa função para representarmos
            o impacto da proporção de caixa em relação ao EBITDA, dado que, depois de um certo valor alto,
            o seu impacto passa a não crescer mais tanto quanto no início.
        """

        clientMetrics = Metrics()

        cashOnEBITDA = clientMetrics.calculateCashOnEBITDA(accountId, itemId, clientSecret, clientId)

        print("cashOnEBITDA")
        print(cashOnEBITDA)
  
        # cashOnEBITDAPosition = (self.calculateSigmoid(cashOnEBITDA)-0.5)*2    
        cashOnEBITDAPosition = self.calculateSigmoid(cashOnEBITDA)

        print("cashOnEBITDAPosition")
        print(cashOnEBITDAPosition)
        
        return cashOnEBITDAPosition

    def calculateIncomeVolatilityPosition(self, accountId, clientSecret, clientId):
        """
            Quanto maior a volatilidade de receita da empresa, menor é a previsibilidade
            de receita da empresa. Como a função calculateIncomeVolatility já nos retorna
            a volatilidade com base no coeficiente de relação, que é uma métrica que varia
            de 0 a 1, podemos considerar esse valor como a posição da empresa na métrica
            volatibilidade da receita.
        """

        clientMetrics = Metrics()

        incomeVolatility = clientMetrics.calculateIncomeVolatility(accountId, clientSecret, clientId)

        print("incomeVolatility")
        print(incomeVolatility)
        
        return incomeVolatility
    
    def calculateLeveragePosition(self, clientId, accountId, clientSecret):
        """
            Quanto maior o nível de alavancagem de uma empresa, mais endividada ela está.
            Usaremos essa métrica para recomendação ou não de crédito para a empresa.
            Consideraremos empresas com alavancagem maior do que 10 igual a 10, já que
            apresentam uma alavancagem alta e o aumento dela acima desse número não
            impactaria nas soluções proposta para a empresa, que é não pegar crédito
            e focar em formas de expansão barata. Para normalizar de 0 a 1 e encontrar
            a posição no eixo dessa métrica, aplicaremos a função 1/10, para mudar o
            intervalo de 0 a 10 para 0 a 1.
            Se a empresa possuir alavancavem menor do que 0, significa que seu EBITDA é negativo
            ou então que a empresa possui mais caixa do que dívida.
            
        """

        clientMetrics = Metrics()

        leverage = clientMetrics.calculateLeverave(clientId, accountId, clientSecret)

        print("leverage")
        print(leverage)

        if (leverage > 10):
            leverage = 10
        elif (leverage < 0):
            clientTransactions = Transactions(clientSecret, clientId)

            EBITDA = clientTransactions.getEBITDA(accountId)
            if (EBITDA < 0):
                """
                    Alavancagem deu negativa por causa do EBITDA negativo.
                    Lucro é negativo e empresa está individida. Assim,
                    classificaremos essa empresa como tendo alta alavancagem.
                """
                leverage = 10
            else:
                """
                    O motivo de a alavancagem estar negativa é devido
                    à empresa possuir mais caixa do que dívida. Assim, podemos
                    classificar a empresa como tendo baixa alavancagem.
                """
                leverage = 0
        
        # normalizar de 0 a 10 para 0 a 1 (dividir por 10)

        leveragePosition = leverage/10

        print("leveragePosition")
        print(leveragePosition)
        
        return leveragePosition