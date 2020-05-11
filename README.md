# Projeto
Projeto desenvolvido com intuito de criar um servidor 
com flask que consumisse a api do site [Advisor](https://advisor.climatempo.com.br/) 
e salvasse as informações em um banco de dados relacional.

## Como Funciona?

O servidor possui duas rotas:

1. A rota */cidade?id=<ID_DA_CIDADE>* que recebe o id de uma 
cidade como parâmetro.

2. A rota */analise?data_inicial=<DATA_INICIAL>&data_final=<DATA_FINAL>* 
que recebe como parâmetros duas datas.


## Rodando o projeto

Assim que realizar o download ou clonar o projeto, 
basta instalar os requirements através do comando:

```bash
$ python -m pip install -r requirements.txt
```

Após a instalação, o servidor pode ser inicializado com o comando:

```bash
$ python entry_point.py
```
Você também pode rodar este servidor utilizando o docker realizando os
sequintes comandos:

```bash
$ docker build -t servidor_flask .
```

```bash
$ docker run -d -p 5000:5000 servidor_flask
```

Desta maneira, o servidor estará rodando em uma imagem do Docker ese comunicando com 
sua máquina através da porta 5000.
