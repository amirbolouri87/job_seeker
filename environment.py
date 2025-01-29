import os
import environ

env = environ.Env()
env.read_env(".env")


match os.getenv("DJANGO_MODE"):
    case "production":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
    case "test":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.test')
    case _:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
