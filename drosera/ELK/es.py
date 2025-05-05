from datetime import datetime
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
import requests

load_dotenv()

class Logger:
    def __init__(self , es_server , api_key):
        self.client = Elasticsearch(es_server , api_key=api_key )


# log = Logger("http://localhost:9200" , api_key=os.getenv("ELASTIC_SEARCH_LOGGER_API_KEY"))


# import requests
# ip_api=os.getenv('IPINFO_API_KEY')
# response = requests.get(f"https://ipinfo.io/8.8.8.8/json?token={ip_api}")
# data = response.json()
# print(data)
