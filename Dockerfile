FROM python:3.11-slim as builder

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \

# create and activate virtual environment
RUN python -m venv /home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --upgrade --no-cache-dir pip
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /home/myuser/venv /home/myuser/venv

USER myuser
RUN mkdir /home/myuser/code
WORKDIR /home/myuser/code
COPY . /home/myuser/code

EXPOSE ${DJANGO_PORT}

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# /dev/shm is mapped to shared memory and should be used for gunicorn heartbeat
# this will improve performance and avoid random freezes
# CMD ["gunicorn","-b", "0.0.0.0:8000", "-w", "4", "-k", "gevent", "--worker-tmp-dir", "/dev/shm", "--chdir", "config config.wsgi:application"]

#CMD ["python", "/job_seeker_data/entrypoint.py"]
