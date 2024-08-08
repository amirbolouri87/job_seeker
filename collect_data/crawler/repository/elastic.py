import json
import requests

from django.conf import settings

from collect_data.crawler.crawler import Repository


class ElasticStorage(Repository):

    def save_data(self, data):
        json_data = json.dumps(data)
        headers = {'content-type': 'application/json', 'charset': 'UTF-8'}
        requests.post(F'{settings.ELASTICSEARCH_HOST}/arbeitnow/_doc/{data["pk"]}', data=json_data,
                      headers=headers)
        print("data saved: pk: %s in elastic" % data.get("pk", ""))
