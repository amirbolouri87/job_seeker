import os

os.system("python3 manage.py migrate --no-input")
os.system("python3 manage.py collectstatic --no-input")
os.system("python3 manage.py runserver 0.0.0.0:8000")
# os.system("gunicorn config.wsgi:application -b 0.0.0.0:8000")
