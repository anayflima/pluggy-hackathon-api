import json
import requests

class DataCollector():
    APIKey = ""
    pluggyUrl = "https://api.pluggy.ai/"
    hackathonPluggyUrl = "https://pluggy-demeter-api.herokuapp.com/"
    clientId = ""
    clientSecret = ""
    
    def __init__(self, clientSecret, clientId):
        self.setClientSecret(clientSecret)
        self.setClientId(clientId)
        self.setAPIKey(self.getAPIKey(self.clientId, self.clientSecret))
    
    def setClientId(self, clientId):
        """
            Função atribui valor recebido para atributo clientSecret
        """
        self.clientId = clientId
    
    def setClientSecret(self, clientSecret):
        """
            Função atribui valor recebido para atributo clientSecret
        """
        self.clientSecret = clientSecret

    def setAPIKey(self,APIKey):
        """
            Função atribui valor recebido para atributo APIKey
        """
        self.APIKey = APIKey
    
    def getAPIKey(self, clientId, clientSecret):
        """
            Função obtém API Key do cliente por chamada de API da Pluggy
        """
        requestUrl = self.pluggyUrl + "auth"

        payload = json.dumps({
            "clientId": clientId,
            "clientSecret": clientSecret
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", requestUrl, headers=headers, data=payload)
        responseJson = response.json()
        self.APIKey = str(responseJson["apiKey"])
        return self.APIKey