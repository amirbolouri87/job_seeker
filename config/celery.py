import os
import json
import requests
from django.conf import settings
from django.urls import reverse
from celery import Celery
from collect_data.arbeitnow.arbeitnow import CollectArbeitnow

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('config')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(90.0, collect_data.s(), name='add every 30')
    sender.add_periodic_task(5.0, analysis_data.s(), name='add every 120')


@app.task
def analysis_data():
    print('start analysis data............')
    data = {
              "query": {
                "match": {
                  "is_translate": {
                    "query": False
                  }
                }
              }
            }
    payload = json.dumps(data)
    headers = {'content-type': 'application/json', 'charset': 'UTF-8'}
    not_translated_query = requests.get(F'{settings.ELASTICSEARCH_HOST}/arbeitnow/_search/', data=payload, headers=headers)
    if not_translated_query.status_code == 200:
        response = (not_translated_query.text)
        json_response = json.loads(response)
        not_translate_advertisements = json_response['hits']['hits']
        for not_translate_advertisement in not_translate_advertisements:
            not_translate_advertisement = not_translate_advertisement['_source']

            # not_translate_advertisement['content'] = 'testtiiiiiiiii'
            not_translate_advertisement['is_translate'] = True

            payload = {
                'content': not_translate_advertisement['content'],
                'is_translated': True
            }
            payload = json.dumps(payload)
            translated_content = requests.post(F'{settings.BASE_HOST}/api/v1/translate-english-text', data=payload, headers=headers)
            print(translated_content.status_code)
            print(translated_content.text)
            updated_advertisement = not_translate_advertisement
            payload = {
                          "doc": updated_advertisement
                     }

            payload = json.dumps(payload)
            response = requests.post(F'{settings.ELASTICSEARCH_HOST}/arbeitnow/_update/{not_translate_advertisement["pk"]}/', data=payload, headers=headers)

    # print(arbeitnow.)

@app.task
def collect_data():
    print('start collecting data............')
    arbeitnow = CollectArbeitnow(site_root='https://www.arbeitnow.com', search_keyword='django')
    arbeitnow.crawl()
    # print(arbeitnow.)

# DJANGO_SETTINGS_MODULE="config.settings.local" celery -A config.celery worker -B --loglevel=info -E
