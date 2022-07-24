import sys
from metricsClassifier import MetricsClassifier
from metrics.metrics import Metrics
sys.path.insert(0, '../data')
import pandas as pd
import requests
from operator import itemgetter
import math
import os

class SolutionsClassifier:
    def __init__(self):
        pass
    
    def getSolutionsList(self, file):
        return pd.read_csv(file, sep = ';')
    
    def calculateSolutionsMetrics(self, solutionsList):
        solutionsMetrics = []
        for i in range(len(solutionsList)):
            solutionMetrics = {}
            # pegar métricas da solução
            cashOnEBITDA = int(solutionsList.iloc[i]['CaixaSobreEBITDA'])
            leverage = int(solutionsList.iloc[i]['Alavancagem'])
            incomeVolatility = int(solutionsList.iloc[i]['VolatilidadeDaReceita'])
            # normalizar e colocar em um dicionário da solução
            solutionMetrics['solution'] = solutionsList.iloc[i]['Solução']
            solutionMetrics['cashOnEBITDA'] = cashOnEBITDA
            solutionMetrics['leverage'] = leverage
            solutionMetrics['incomeVolatility'] = incomeVolatility

            solutionsMetrics.append(solutionMetrics)
        return solutionsMetrics

    def defineClientProfile(self, clientId, accountId, itemId):
        clientMetricsClassifier = MetricsClassifier()
        profile = {
            'cashOnEBITDA': clientMetricsClassifier.calculateCashOnEBITDAPosition(accountId, itemId),
            'incomeVolatility': clientMetricsClassifier.calculateIncomeVolatilityPosition(accountId),
            'leverage': clientMetricsClassifier.calculateLeveragePosition(clientId, accountId),
        }
        return profile

    def calculateEuclideanDistance3D(self, xa, ya, za, xb, yb, zb):
        """
            Calcula a distância entre dois pontos
        """
        return math.sqrt((xa-xb)**2 + (ya-yb)**2 + (za-zb)**2)

    def findBestSolutions(self, client, solutionsMetrics):
        """
            Função calcula a distância euclideana de cada uma das soluções até o cliente,
            devolvendo as k soluções que mais se aproximam do seu perfil.
        """
        distancesSolutionsClients = {}
        solutions = []

        # achar a distância do cliente para cada uma das soluções
        for solution in solutionsMetrics:
            clientLeverage = float(client['leverage'])
            clientCash = float(client['cashOnEBITDA'])
            clientIncomeVolatility = float(client['incomeVolatility'])

            euclideanDistance = self.calculateEuclideanDistance3D(float(solution['leverage']),float(solution['cashOnEBITDA']), float(solution['incomeVolatility']), clientLeverage, clientCash, clientIncomeVolatility)
            print("distance between (", clientLeverage, ", ", clientCash, ", ", clientIncomeVolatility, ") and ", "(", float(solution['leverage']), ", ", float(solution['cashOnEBITDA']), ", ", float(solution['incomeVolatility']), ") is ", euclideanDistance)
            
            distancesSolutionsClients[solution['solution']] = euclideanDistance

            solutionsInformation = {
                'solution': solution['solution'],
                'euclideanDistance': euclideanDistance,
                # 'leverage':solution['leverage'],
                # 'cashProfile': solution['cashOnEBITDA'],
                # 'incomeVolatility': solution['incomeVolatility'],
            }
            solutions.append(solutionsInformation)
        
        k = 4
        bestSolutionsDistance = dict(sorted(distancesSolutionsClients.items(), key = itemgetter(1))[:k])
        bestSolutions = []
        for solution in solutions:
            if (solution['solution'] in bestSolutionsDistance.keys()):
                bestSolutions.append(solution)

        return bestSolutions

    
    def createSolutionsPortfolio(self, bestSolutions):
        distancesSum = 0
        # normaliza os dados (coloca no intervalo 0 e 1)

        positions = []
        for solution in bestSolutions:
            position = 1/(3*solution['euclideanDistance'])
            positions.append(position)
            
        for i in range(len(bestSolutions)):
            position = positions[i]
            normalizedPosition = (position - min(positions)) / (max(positions)-min(positions))
            bestSolutions[i]['positiveImpact'] = normalizedPosition
        
        # solution['positiveImpact'] = position
        
        return bestSolutions


    def defineCustomerSolutionsPortfolio(self, clientId, accountId, itemId):
        # define perfil do cliente
        clientProfile = self.defineClientProfile(clientId, accountId, itemId)


        # Fazer diretório atual igual a diretório dos dados
        directory = os.getcwd()
        print(directory)
        if "data" not in directory:
            os.chdir(directory + "/data")
            directory = os.getcwd()
            print(directory)
        
        # importa e calcula métricas das soluções
        solutionsList = self.getSolutionsList("./solutionsList.csv")
        solutionsMetrics = self.calculateSolutionsMetrics(solutionsList)

        # encontra as x soluções mais próximas da pessoa
        bestSolutions = self.findBestSolutions(clientProfile, solutionsMetrics)

        # prepara o retorno para cliente, com a porcentagem de
        # proximidade dele para cada solução
        solutionsPortfolio = self.createSolutionsPortfolio(bestSolutions)

        customerSolutionsPortfolio = {
            "solutions": solutionsPortfolio
        }

        return customerSolutionsPortfolio


