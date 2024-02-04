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

python_skills = ["Python", "Django", "Flask", "RESTful API development", "SQL", "ORM (Object-Relational Mapping)", "HTML", "CSS", "JavaScript", "Git", "Unit testing", "Debugging", "Data structures", "Algorithm design", "Problem-solving", "Web development", "Software architecture", "Agile methodology"]
python_skills_advance = ["Front-end development", "Back-end development", "DevOps", "Docker", "AWS", "Azure", "Google Cloud Platform", "Microservices", "Machine learning", "Data analysis", "Data visualization", "AI", "Natural language processing", "Parallel processing", "Security best practices", "Continuous integration/Continuous deployment (CI/CD)", "Design patterns", "Code optimization", "Performance tuning", "Agile project management", "Collaboration and communication skills"]
django_skills = ["Django", "Python", "Django Rest Framework", "ORM (Object-Relational Mapping)", "SQL", "HTML", "CSS", "JavaScript", "RESTful API development", "Authentication and authorization", "Database design and management", "Unit Testing", "Front-end frameworks (e.g., React, Angular)", "Version control (e.g., Git)", "Debugging", "Performance optimization", "Software architecture", "Security best practices", "Agile methodology"]
docker_skills = ["Docker", "Containerization", "Docker Compose", "Docker Swarm", "Kubernetes", "Container orchestration", "Microservices architecture", "CI/CD pipelines", "Docker networking", "Docker security best practices", "Dockerfile", "Docker volumes", "Docker registries", "Monitoring and logging in Docker", "Docker cloud platforms (e.g., AWS ECS, Google Kubernetes Engine)"]
software_design_skills = ["Software architecture", "Design patterns", "UML (Unified Modeling Language)", "System design", "Object-oriented design", "Component-based design", "Design principles (SOLID, DRY, etc.)", "Architectural patterns (MVC, MVP, etc.)", "API design", "Database design", "Scalability considerations", "Reliability and fault tolerance", "Cross-functional collaboration", "Trade-off analysis", "Documentation"]


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(120.0, collect_data.s(), name='collect_data')
    # sender.add_periodic_task(50.0, analysis_data.s(), name='add every 20')
    # sender.add_periodic_task(120.0, find_best_ads.s(), name='add every 120')


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
        response = not_translated_query.text
        json_response = json.loads(response)
        not_translate_advertisements = json_response['hits']['hits']
        for not_translate_advertisement in not_translate_advertisements:
            not_translate_advertisement = not_translate_advertisement['_source']

            payload = {
                'content': not_translate_advertisement['content'],
                'is_translated': True
            }
            # print("germany ====================================")
            # print(not_translate_advertisement)
            payload = json.dumps(payload)

            translated_content = requests.post(F'{settings.BASE_HOST}/api/v1/translate-english-text', data=payload, headers=headers)
            print(translated_content.status_code)
            if translated_content.status_code == 200:
                print("traslate is ok .....")
            updated_advertisement = translated_content.text
            payload = {
                          "doc": json.loads(updated_advertisement)
                     }
            # print("eng ====================================")
            payload = json.dumps(payload)
            # print(updated_advertisement)
            response = requests.post(F'{settings.ELASTICSEARCH_HOST}/arbeitnow/_doc/{not_translate_advertisement["pk"]}/', data=payload, headers=headers)
            if response.status_code == 200:
                print('ads = ', not_translate_advertisement["pk"] , ' updated.')
                not_translate_advertisement['is_translate'] = True
            else:
                print('update error')
                print(payload)
                print('error >>>>>>>>>>>>>>')
                print(response.text)

@app.task
def collect_data():
    print('start collecting data............')
    arbeitnow = CollectArbeitnow(site_root='https://www.arbeitnow.com', search_keyword='django')
    arbeitnow.crawl()


@app.task
def find_best_ads():
    print('find_best_ads ............')
    # arbeitnow = CollectArbeitnow(site_root='https://www.arbeitnow.com', search_keyword='django')
    # arbeitnow.crawl()


# DJANGO_SETTINGS_MODULE="config.settings.local" celery -A config.celery worker -B --loglevel=info -E
