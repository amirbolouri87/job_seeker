# config

## Setup

### Environment Configuration

For this project, you need to have a directory named `.setting_envs` in the root of the project. Inside this directory, create the following directories:


Your project directory structure should look like this:

```plaintext
project-root-directory/
│
├── .setting_envs/
│   ├── local/
│   │   └── .env
│   ├── production/
│   │   └── .env
│   ├── test/
│       └── .env
│   
│
├── other-project-files/
│   ├── ...
│   └── ...
│
├── manage.py
├── requirements
└── README.md

Each .env file should contain the following keys:

DJANGO_SETTINGS_MODULE=

DEBUG=
SECRET_KEY=
ALLOWED_HOSTS=


