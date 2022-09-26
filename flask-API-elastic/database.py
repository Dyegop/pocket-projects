""" Connection to Elastic Search database and methods to load a csv file into that database """

import json
import csv
from elasticsearch import Elasticsearch, helpers



CREDENTIALS = "resources/credentials.json"
FIELD_NAMES = ["id", "inventory name", "contact name", "stock", "last revenue",
               "current revenue", "refund", "company name", "categories", "rating"]


def ElasticSearchConnection():
    """Connect to ElasticSearch"""
    try:
        _USER, _PASSWORD, _CLOUD_ID = json.load(open(CREDENTIALS)).values()
        return Elasticsearch(cloud_id=_CLOUD_ID, http_auth=(_USER, _PASSWORD), timeout=60)
    except ConnectionError:
        print("Error connecting to ElasticSearch\n")
        raise
    except FileNotFoundError:
        print(f"File {CREDENTIALS} not found\n")
        raise


def loadCsv(filepath: str, es_client: Elasticsearch, fieldnames=None):
    """Load csv file into ElasticSearch"""
    try:
        csv_file = csv.DictReader(open(filepath, "r"), fieldnames=fieldnames)
        response = helpers.bulk(es_client, csv_file, index="second_load",)
        print("RESPONSE: ", response)
    except Exception as e:
        print("ERROR: ", e)


def getData(n: int, es_client: Elasticsearch):
    """ Query data from ElasticSearch """
    query_body = {
        "query": {"match_all": {}},
        "from": n*20,
        "size": 20
    }
    response = es_client.search(index="second_load", body=query_body)
    return response





if __name__ == '__main__':
    es = ElasticSearchConnection()
    print(es.ping())
    # loadCsv("resources/SampleCSVFile_556kb.csv", es, FIELD_NAMES)
    print(getData(0, es))
