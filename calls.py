import sys
sys.path.insert(0, './metrics/')
from metrics import Metrics
from transactions import Transactions
from debts import Debts
from dataCollector import DataCollector
sys.path.insert(0, './models/')
from metricsClassifier import MetricsClassifier

def calls():
    clientMetrics = Metrics()
    clientTransactions = Transactions()
    # X_API_KEY = clientTransactions.getAPIKey("a8935a1f-a204-40de-bd86-eed00f433887", "2c61a2ee-eca2-4d69-8891-060ec0fd76cd")
    # clientTransactions.setAPIKey(X_API_KEY)
    totalTransations = clientTransactions.getTransactions("4d4f622a-38d6-4991-b340-387492fd22c8")
    # print("totalTransations = " + str(totalTransations))
    # mensalIncome = clientMetrics.getMensalIncome("4d4f622a-38d6-4991-b340-387492fd22c8")
    # print("mensalIncome = " + str(mensalIncome))
    # cash = clientMetrics.getCash("4d4f622a-38d6-4991-b340-387492fd22c8")
    # print("cash = " + str(cash))
    # cashForMensalIncome = clientMetrics.calculateCashForMensalIncome("4d4f622a-38d6-4991-b340-387492fd22c8")
    # print("cashForMensalIncome = " + str(cashForMensalIncome))
    # incomeVolatility = clientMetrics.getIncomeVolatility()
    # print("incomeVolatility = " + str(incomeVolatility))
    positiveTransactionsByMonth = clientTransactions.getPositiveTransactionsByMonth("4d4f622a-38d6-4991-b340-387492fd22c8")
    print("positiveTransactionsByMonth = " + str(positiveTransactionsByMonth))

def callsDebts():
    clientDebts = Debts()
    # annualFinancings = clientDebts.getCurrentFinancings("a8935a1f-a204-40de-bd86-eed00f433887")
    # print("annualFinancings = " + str(annualFinancings))
    # annualLoans = clientDebts.getCurrentLoans("a8935a1f-a204-40de-bd86-eed00f433887")
    # print("annualLoans = " + str(annualLoans))
    grossDebt = clientDebts.calculateGrossDebt("a8935a1f-a204-40de-bd86-eed00f433887")
    print("grossDebt = " + str(grossDebt))


def callsMetrics():
    clientMetrics = Metrics()
    cashForEBITDA = clientMetrics.calculateCashOnEBITDA("4d4f622a-38d6-4991-b340-387492fd22c8", "a4ac3258-e88f-4123-8dc4-a4f72c3da7a7")
    print("cashForEBITDA = " + str(cashForEBITDA))
    incomeVolatility = clientMetrics.calculateIncomeVolatility("4d4f622a-38d6-4991-b340-387492fd22c8")
    print("incomeVolatility = " + str(incomeVolatility))
    leverage = clientMetrics.calculateLeverave("a8935a1f-a204-40de-bd86-eed00f433887", "4d4f622a-38d6-4991-b340-387492fd22c8")
    print("leverage = " + str(leverage))

def callsImpact():
    clientMetricsClassifier = MetricsClassifier()
    cashOnEBITDAPosition = clientMetricsClassifier.calculateCashOnEBITDAPosition("4d4f622a-38d6-4991-b340-387492fd22c8", "a4ac3258-e88f-4123-8dc4-a4f72c3da7a7")
    print("cashOnEBITDAPosition = " + str(cashOnEBITDAPosition))
    incomeVolatilityPosition = clientMetricsClassifier.calculateIncomeVolatilityPosition("4d4f622a-38d6-4991-b340-387492fd22c8")
    print("incomeVolatilityPosition = " + str(incomeVolatilityPosition))
    leveragePosition = clientMetricsClassifier.calculateLeveragePosition("a8935a1f-a204-40de-bd86-eed00f433887", "4d4f622a-38d6-4991-b340-387492fd22c8")
    print("leveragePosition = " + str(leveragePosition))
    
    

if __name__ == '__main__':
    callsImpact()