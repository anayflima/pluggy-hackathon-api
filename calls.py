import sys
sys.path.insert(0, './metrics/')
from metrics import Metrics
from transactions import Transactions
from debts import Debts
from dataCollector import DataCollector
sys.path.insert(0, './models/')
from metricsClassifier import MetricsClassifier

accountId = "4d4f622a-38d6-4991-b340-387492fd22c8"
itemId = "a4ac3258-e88f-4123-8dc4-a4f72c3da7a7"
clientId = "a8935a1f-a204-40de-bd86-eed00f433887"

def callsDebts():
    clientDebts = Debts()
    annualFinancings = clientDebts.getCurrentFinancings(clientId)
    print("annualFinancings = " + str(annualFinancings))
    annualLoans = clientDebts.getCurrentLoans(clientId)
    print("annualLoans = " + str(annualLoans))
    grossDebt = clientDebts.calculateGrossDebt(clientId)
    print("grossDebt = " + str(grossDebt))

def callsMetrics():
    clientMetrics = Metrics()
    cashForEBITDA = clientMetrics.calculateCashOnEBITDA(accountId, itemId)
    print("cashForEBITDA = " + str(cashForEBITDA))
    incomeVolatility = clientMetrics.calculateIncomeVolatility(accountId)
    print("incomeVolatility = " + str(incomeVolatility))
    leverage = clientMetrics.calculateLeverave(clientId, accountId)
    print("leverage = " + str(leverage))

def callsImpact():
    clientMetricsClassifier = MetricsClassifier()
    cashOnEBITDAPosition = clientMetricsClassifier.calculateCashOnEBITDAPosition(accountId, itemId)
    print("cashOnEBITDAPosition = " + str(cashOnEBITDAPosition))
    incomeVolatilityPosition = clientMetricsClassifier.calculateIncomeVolatilityPosition(accountId)
    print("incomeVolatilityPosition = " + str(incomeVolatilityPosition))
    leveragePosition = clientMetricsClassifier.calculateLeveragePosition(clientId, accountId)
    print("leveragePosition = " + str(leveragePosition))
    

if __name__ == '__main__':
    callsImpact()