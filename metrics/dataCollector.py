import json
import requests

class DataCollector():
    APIKey = ""
    pluggyUrl = "https://api.pluggy.ai/"
    hackathonPluggyUrl = "https://pluggy-demeter-api.herokuapp.com/"
    clientId = "a8935a1f-a204-40de-bd86-eed00f433887"
    clientSecret = "2c61a2ee-eca2-4d69-8891-060ec0fd76cd"
    
    def __init__(self):
        self.setAPIKey(self.getAPIKey(self.clientId, self.clientSecret))

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