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

```

```markdown
## Running the Project in Docker Development Environment

To run the project in a Docker environment in development mode, use the following command:

```bash
docker-compose --env-file .dockerenv --file development-docker-compose.yml up -d
```

### Docker Compose Environment Variables

The Docker Compose environment variables are located in the `.dockerenv` file. You can modify settings such as the web application port, password, and more.
```
