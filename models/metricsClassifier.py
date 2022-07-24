import sys
sys.path.insert(0, './')
from metrics import Metrics
import pandas as pd
import numpy as np
import requests
from operator import itemgetter
import math

class MetricsClassifier:
    def __init__(self):
        pass
    def calculateSigmoid(self, x):
        return 1/(1+np.exp(-(1/x)))
    
    def calculateCashOnEBITDAPosition(self, accountId, itemId):
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

        cashOnEBITDA = clientMetrics.calculateCashOnEBITDA(accountId, itemId)
  
        # cashOnEBITDAPosition = (self.calculateSigmoid(cashOnEBITDA)-0.5)*2    
        cashOnEBITDAPosition = self.calculateSigmoid(cashOnEBITDA)
        
        return cashOnEBITDAPosition

    def calculateIncomeVolatilityPosition(self, accountId):
        """
            Quanto maior a volatilidade de receita da empresa, menor é a previsibilidade
            de receita da empresa. Como a função calculateIncomeVolatility já nos retorna
            a volatilidade com base no coeficiente de relação, que é uma métrica que varia
            de 0 a 1, podemos considerar esse valor como a posição da empresa na métrica
            volatibilidade da receita.
        """

        clientMetrics = Metrics()

        incomeVolatility = clientMetrics.calculateIncomeVolatility(accountId)
        
        return incomeVolatility
    
    def calculateLeveragePosition(self, clientId, accountId):
        """
            Quanto maior o nível de alavancagem de uma empresa, mais endividada ela está.
            Usaremos essa métrica para recomendação ou não de crédito para a empresa.
            Consideraremos:
            1 - empresas com alavancagem entre 0 e 3
            2 - empresas com alavancagem entre 3 e 6
            3 - empresas com alavancagem maior do que 6
            Para normalizar de 0 a 1 e encontrar a posição no eixo dessa métrica, aplicaremos
            a função 1/2 - 1, para mudar o range de 1 a 3 para 0 a 1. Ou seja:
            0 - empresas com alavancagem entre 0 e 3
            0.5 - empresas com alavancagem entre 3 e 6
            1 - empresas com alavancagem maior do que 6

            Se a empresa possuir alavancavem menor do que 0, significa que seu EBITDA é negativo
            ou então que a empresa possui mais caixa do que dívida.
            
        """

        clientMetrics = Metrics()

        leverage = clientMetrics.calculateLeverave(clientId, accountId)

        print(leverage)

        if (leverage < 0):
            leveragePosition = 1
        elif (leverage < 3):
            leveragePosition = 0
        elif (leverage < 6):
            leveragePosition = 0.5
        else:
            leveragePosition = 1

        
        return leveragePosition