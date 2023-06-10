# TCC ADS

Para iniciar a aplicação é necessário ter os seguintes programas instalados na máquina:
1. PostgreSQL;
2. Python;

Tendo esses programas instalados, execute o seguinte comando no terminal/prompt:
`python -m pip install -r requirements.txt`.

Após isso inicie a aplicação com o comando: `python main.py`.

Caso for a primeira vez que esteja executando escolha a opção "6 - Iniciar banco de dados".

Isso irá fazer com que o banco de dados seja criado e o backup com nome "banco_de_dados.backup" presente na pasta restaurado.

E por fim para iniciar a API basta iniciar a aplicação e escolher a opção "5 - Iniciar servidor da API".

## Endpoints da API

---
- **/station** -> Retorna a lista de estações que possuem algum dado histórico, podendo informar a sigla de um estado com o argumento 'state' para serem listadas somente as estações de um estado específico. Ex:
  - `localhost:5000/station?state=SC`

---
- **/city** -> Retorna a lista de cidades que possuem algum dado de previsão do tempo, podendo informar a sigla de um estado com o argumento 'state' para serem listadas somente as cidades de um estado específico. Ex:
  - `localhost:5000/city?state=SC`

--- 
- **/weather-type** -> Retorna a lista de possíveis tipos de condição climática que podem ser retornados em uma previsão do tempo. Ex:
  - `localhost:5000/weather-type`

---
- **/history/station** -> Retorna os dados históricos do clima de uma estação específica, sendo obrigatório informar a partir de que data deseja o histórico com o argumento 'init_date' e o código da estação com o argumento 'station'. Como opcional pode-se informar o argumento 'times_of_day' para retornar somente os dados históricos de determinadas horas do dia, respeitando as regras descritas [aqui](#regras-para-o-argumento-timesofday). Ex:
  - `localhost:5000/history/station?init_date=20/03/2023&station=3&times_of_day=14`

---
- **/history/state** -> Retorna os dados históricos do clima de todas as estações de um estado específico, sendo obrigatório informar a partir de que data deseja o histórico com o argumento 'init_date' e a sigla do estado com o argumento 'state'. Como opcional pode-se informar o argumento 'times_of_day' para retornar somente os dados históricos de determinadas horas do dia, respeitando as regras descritas [aqui](#regras-para-o-argumento-timesofday). Ex:
  - `localhost:5000/history/state?init_date=20/03/2023&state=SC&times_of_day=14`

---
- **/history/average/station** -> Retorna as médias dos dados históricos do clima de uma estação específica, sendo obrigatório informar a partir de que data deseja as médias com o argumento 'init_date', o código da estação com o argumento 'station' e a frequência das médias que deseja, diária(daily), semanal(weekly) ou mensal(monthly) com o argumento 'frequency'. Ex:
  - `localhost:5000/history/average/station?init_date=20/03/2023&station=3&frequency=monthly`

---
- **/history/average/state** -> Retorna as médias dos dados históricos do clima de todas as estações de um estado específico, sendo obrigatório informar a partir de que data deseja as médias com o argumento 'init_date', a sigla do estado com o argumento 'state' e a frequência das médias que deseja, diária(daily), semanal(weekly) ou mensal(monthly) com o argumento 'frequency'. Ex:
  - `localhost:5000/history/average/state?init_date=20/03/2023&state=SC&frequency=monthly`

---
- **/forecast/city** -> Retorna os dados de previsão do tempo de uma cidade específica, sendo obrigatório informar o código da cidade com o argumento 'city' e a quantidade de dias da previsão com o argumento 'days'. Ex:
  - `localhost:5000/forecast/city?city=3&days=10`

---
- **/forecast/state** -> Retorna os dados de previsão do tempo de todas as cidades de um estado específico, sendo obrigatório informar a sigla do estado com o argumento 'state' e a quantidade de dias da previsão com o argumento 'days'. Ex:
  - `localhost:5000/forecast/state?state=SC&days=10`

---
- **/forecast/average/city** -> Retorna as médias dos dados de previsão do tempo de uma cidade específica, sendo obrigatório informar o código da cidade com o argumento 'city' e o período de médias de 7 ou 14 dias com o argumento 'period_day'. Ex:
  - `localhost:5000/forecast/average/city?city=3&period_day=7`

---
- **/forecast/average/state** -> Retorna as médias dos dados de previsão do tempo de todas as cidades de um estado específico, sendo obrigatório informar a sigla do estado com o argumento 'state' e o período de médias de 7 ou 14 dias com o argumento 'period_day'. Ex:
  - `localhost:5000/forecast/average/state?state=SC&period_day=14`

---
### Regras para o argumento 'times_of_day'

1. Informar horários específicos, separando por vírgula. Ex:
   2. 8, 13, 15.
   3. Nesse caso irá trazer os dados das horas 08:00, 13:00 e 15:00
2. Informar um range de horários, separando por traço. Ex:
   3. 13-17. 
   4. Nesse caso irá retornar os dados das horas 13:00, 14:00, 15:00, 16:00 e 17:00.
5. Realizar a junção de ambos. Ex:
   6. 12, 16-19.
   7. Nesse caso irá retornar os dados das horas 12:00, 16:00, 17:00, 18:00 e 19:00.