#GET /api/v1/products
# importing the requests library 
import os
import json
import pymongo
import requests
import datetime
import time
from   bson     import json_util
from   pymongo  import MongoClient
from   datetime import datetime

time.sleep(30)

#Definicao de URL para Captura dos Produtos no SPREE
#URLproducts = 'http://172.20.0.2:3000/api/v1/products.json?token=e0c91507ca69781a03c62aabd83246ed75e8ed0f498a4652'
URLproducts = 'http://172.20.0.2:3000/api/v1/products.json?token=894fa3111b5a8c4ff8778f2e20f067a367b665918a6eac28'

#Executando o POST dos Produtos SPREE atraves da chamada da API
#product_capture = requests.post(URLproducts)

#Executando o GET dos Produtos SPREE atraves da chamada da API
product_capture = requests.get(URLproducts)

#Valida Codigo de Retorno da chamada da API
if product_capture.status_code != 200:
    print('Falha na Obtencao dos Dados - Erro:', product_capture.status_code)
    exit
else:
    print('Coleta de Informacao ds API efetuada com Sucesso!')
    #Carregando JSON a partir do retorno da API
    product = json.loads(product_capture.text)
    print('Carga de JSON efetuada com Sucesso!')

    client = MongoClient('172.20.0.3', 27017)
    db = client['EP1_VILELA']
    collection_product = db['products']

    print('Parametros Atrubuidos para acesso ao MongoDB')

    #Loop que Obtem os FIELDs definidos para carregar no Mongodb
    for field in product['products']:
        json_file = {
            "id_spree": field["id"],
            "name": field["name"],
            #"description": field["description"],
            "price": field["price"],
            "available_on": field["available_on"],
            "slug": field["slug"],
            "collectdatetime": str(datetime.now())
        } 
        #Inserindo no MongoDB a coleta efetuada no SPREE
        posts = collection_product
        post_id = posts.insert_one(json_file).inserted_id

    print('Carga JSON Parcial efetuada com sucesso: ' + str(datetime.now()))

    client = MongoClient('172.20.0.3', 27017)
    db = client['EP1_VILELA']
    collection_product_raw = db['products_raw']

    for field in product['products']:
        posts = collection_product_raw
        post_id = posts.insert_one(field).inserted_id

    print('Carga JSON Completo efetuada com sucesso: ' + str(datetime.now()))
    exit
