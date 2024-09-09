import os

d_setting_module = os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.test")
print(d_setting_module)

match d_setting_module:
    case "config.settings.test":
        os.system("python3 manage.py makemigrations")
        os.system("python3 manage.py migrate --no-input")
        os.system("python3 manage.py test")
    case "config.settings.local":
        os.system("python3 manage.py makemigrations")
        os.system("python3 manage.py migrate --no-input")
        os.system(f"python3 manage.py runserver 0.0.0.0:{os.getenv('DJANGO_PORT')}")
    case "config.settings.production":
        os.system("python3 manage.py migrate --no-input")
        os.system("python3 manage.py collectstatic --no-input")
        os.system(f"gunicorn -k gevent --workers 4 --worker-tmp-dir /dev/shm --chdir config config.wsgi:application -b 0.0.0.0:{os.getenv('DJANGO_PORT')}")
