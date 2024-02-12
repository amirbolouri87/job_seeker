#FROM python:3.8
#ARG requirement_file
#
#WORKDIR /job_seeker_data
#
## Copy project files to the working directory
#COPY . /job_seeker_data/
#
#RUN apt-get update && apt-get install -y \
#    python3.8-dev \
#    alien \
#    libaio1 \
#    libaio-dev
#
## Install Python dependencies
#RUN pip install -r /job_seeker_data/requirements/$requirement_file
#
#COPY ./entrypoint.py /job_seeker_data/
#
#RUN chmod +x /job_seeker_data/entrypoint.py
#CMD ["python", "/job_seeker_data/entrypoint.py"]
#
## for build image use these structure
## sudo docker build --build-arg requirement_file=production.txt --no-cache -t eclaim_production:latest -f Dockerfile .
FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
ARG requirement_file

WORKDIR /job_seeker_data
COPY . /job_seeker_data/

# Install system dependencies
RUN apk update && apk add --no-cache \
    python3-dev\
    libc-dev \
    linux-headers \
    libffi-dev \
    gcc


# Install Python dependencies
RUN pip install -r /job_seeker_data/requirements/$requirement_file

COPY ./entrypoint.py /job_seeker_data/
RUN apk del --purge \
    linux-headers \
    libffi-dev \
    gcc

RUN chmod +x /job_seeker_data/entrypoint.py
CMD ["python", "/job_seeker_data/entrypoint.py"]


# for build image use these structure
# sudo docker build --build-arg requirement_file=production.txt --no-cache -t eclaim_production:latest -f Dockerfile .
