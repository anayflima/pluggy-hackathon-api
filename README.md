# Pluggy Deméter API

### Resumo

O objetivo desse produto é utilizar os dados do Open Finance para propor sugestões de tomada de decisões para uma determinada empresa, a fim de melhorar tanto o seu caráter operacional, como expandir e pensar em novas soluções.

### Servidor

As APIs desse repositório estão hospedadas no servidor:
- [Pluggy Demeter API](https://pluggy-demeter-api.herokuapp.com/)

### Como consumir esse serviço

A API principal recebe como parâmetros a clientSecret, clientId, accountId e itemId, fornecidos pelo sandbox da Pluggy e devolve as 4 soluções mapeadas que mais se adequam ao perfil da companhia. Cada uma das soluções contém a porcentagem de impacto positivo que aquela solução provavelmente terá no negócio. Também é devolvido a distância euclideana, para fins de visualização.

##### Exemplo de execução:

[https://pluggy-demeter-api.herokuapp.com/classifier/clientSecret=<clientSecret>/clientId=<clientId>/accountId=<accountId>/itemId=<itemId>](https://pluggy-demeter-api.herokuapp.com/classifier/clientSecret=2c61a2ee-eca2-4d69-8891-060ec0fd76cd/clientId=a8935a1f-a204-40de-bd86-eed00f433887/accountId=4d4f622a-38d6-4991-b340-387492fd22c8/itemId=a4ac3258-e88f-4123-8dc4-a4f72c3da7a7)

$ https://pluggy-demeter-api.herokuapp.com/classifier/clientSecret=2c61a2ee-eca2-4d69-8891-060ec0fd76cd/clientId=a8935a1f-a204-40de-bd86-eed00f433887/accountId=4d4f622a-38d6-4991-b340-387492fd22c8/itemId=a4ac3258-e88f-4123-8dc4-a4f72c3da7a7

##### Exemplo de saída:
```json
$ {"page":1,"results":[{"amount":235,"currencyCode":"BRL","id":"d3434-2343-7878-a4534-032h72343423k","paymentDate":"2022-06-13T03:00:00.000Z"},{"amount":572,"currencyCode":"BRL","id":"d45gf-dfg43-7845678-d675-so83n9ds9","paymentDate":"2022-07-13T03:00:00.000Z"},{"amount":1235,"currencyCode":"BRL","id":"aa3f2f-fhhy345-dfh34234-4563g-sdf872jn","paymentDate":"2022-08-13T03:00:00.000Z"},{"amount":835,"currencyCode":"BRL","id":"aa3f2f-fhhy345-dfh34234-4563g-sdf872jn","paymentDate":"2022-09-13T03:00:00.000Z"}],"total":2,"totalPages":1}
```

### Algoritmo utilizado

Esse repositório recebe dados das APIs fornecida pelo sandbox da Pluggy:
- [Dashboard Pluggy](https://dashboard.pluggy.ai/)

No entanto, alguns dados de Open Finance não são fornecidos por esse sandbox. Assim, como forma de complementação, foram feitas APIs para simular o retorno dos dados faltantes. Essas APIs fornecem dados de financiamentos e empréstimos do cliente.

##### Exemplos de uso das APIs criadas:

- [https://pluggy-demeter-api.herokuapp.com/financings/<clientId>](https://pluggy-demeter-api.herokuapp.com/financings/a8935a1f-a204-40de-bd86-eed00f433887)
- [https://pluggy-demeter-api.herokuapp.com/loans/<clientId>](https://pluggy-demeter-api.herokuapp.com/loans/a8935a1f-a204-40de-bd86-eed00f433887)

#### Descrição

Escolhemos utilizar os dados do Open Finance para obter informações sobre as seguintes métricas financeiras da empresa: alavancagem, volatilidade de receita e caixa sobre EBITDA.

Em primeiro lugar, mapeamos soluções para empresas com diferentes níveis dessas três métricas. A exemplo disso, se uma determinada empresa se encontra com alto nível de volatilidade da receita, mas baixa alavancagem, sugerimos tomada de crédito para investir na fidelização de clientes. Essas soluções podem ser encontradas no arquivo [solutionsList.csv](https://github.com/anayflima/pluggy-hackathon-api/blob/main/data/solutionsList.csv). Cada uma das soluções foi classificada como sendo a ideal em um determinado cenário de alavancagem, volatilidade de receita e caixa sobre EBITDA, sendo que 1 representa um alto nível dessa métrica e 0 um baixo nível.

Em segundo lugar, com os dados de uma determinada empresa fornecidos por APIs do Open Finance, o algoritmo desenvolvido classifica a companhia em termos dessas métricas. Dessa forma, com esses valores, é possível cruzar esses indicadores com as soluções já mapeadas e, assim, identificar o momento da empresa e possíveis sugestões e insights  para o negócio. 

O tratamento dos dados e a devolução dos insights é feita pelo método [generateClientSolutionsClassifier](https://github.com/anayflima/pluggy-hackathon-api/blob/main/app.py#L104) desse servidor. Ele recebe o clientId, accountId e itemId da companhia e devolve uma lista das soluções mais adequadas para ela. Essas soluções são encontradas considerando que as 3 métricas formam um espaço 3D, cada uma representando um dos eixos. Assim, tendo a posição do cliente e das soluções nesse espaço, calculamos a distância euclideana entre o cliente e cada uma das soluções e escolhemos as k soluções mais próximas como insights. Tal algoritmo foi baseado no modelo de machine learning [K-Nearest Neighbors](https://www.baeldung.com/cs/k-nearest-neighbors#k-nearest-neighbors). Além disso, o método devolve o quão forte aquela solução é indicada para um usuário, sendo isso inversamente proporcional à distância do cliente àquela solução.

##### Exemplo de uso do método generateClientSolutionsClassifier:

[https://pluggy-demeter-api.herokuapp.com/classifier/clientId=<clientId>/accountId=<accountId>/itemId=<itemId>](https://pluggy-demeter-api.herokuapp.com/classifier/clientId=a8935a1f-a204-40de-bd86-eed00f433887/accountId=4d4f622a-38d6-4991-b340-387492fd22c8/itemId=a4ac3258-e88f-4123-8dc4-a4f72c3da7a7)