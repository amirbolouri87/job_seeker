FROM repo.sos.com/docker-remote/python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /eclaim_data && mkdir -p /root/.pip
ARG requirement_file

# Create pip.conf with custom repository URL
RUN echo "[global]" > /root/.pip/pip.conf && \
    echo "index-url = http://f-ansari:Zaq12321@@repo.sos.com/artifactory/api/pypi/python-remote/simple" >> /root/.pip/pip.conf


WORKDIR /eclaim_data
COPY . /eclaim_data/


# Copy project files to the working directory
COPY . /ecalim_data/

COPY oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm  /eclaim_data/

## Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.8-dev \
    alien \
    libaio1 \
    libaio-dev

# Install Oracle Instant Client
RUN alien -i oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm
RUN alien -i oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm
RUN sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"
RUN ldconfig

# Install Python dependencies
RUN pip install -r /eclaim_data/requirements/$requirement_file --trusted-host repo.sos.com


COPY ./entrypoint.py /eclaim_data/

RUN chmod +x /eclaim_data/entrypoint.py
CMD ["python", "/eclaim_data/entrypoint.py"]


# for build image use these structure
# sudo docker build --build-arg requirement_file=production.txt --no-cache -t eclaim_production:latest -f Dockerfile .
