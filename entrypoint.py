import os

os.system("python manage.py migrate --no-input")
os.system("python manage.py collectstatic --no-input")
os.system("gunicorn config.wsgi:application -b 0.0.0.0:8000")
