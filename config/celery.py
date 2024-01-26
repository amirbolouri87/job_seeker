import os
from celery import Celery
from collect_data.arbeitnow.arbeitnow import CollectArbeitnow

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('config')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(180.0, collect_data.s(), name='add every 10')


@app.task
def collect_data():
    print('start collecting data............')
    arbeitnow = CollectArbeitnow(site_root='https://www.arbeitnow.com', search_keyword='django')
    arbeitnow.crawl()
    # print(arbeitnow.)

# DJANGO_SETTINGS_MODULE="config.settings.local" celery -A config.celery worker -B --loglevel=info -E