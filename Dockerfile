FROM python:3.12-slim
ARG requirement_file
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends

WORKDIR /job_seeker_data

# Copy project files to the working directory
COPY . /job_seeker_data/

# Install Python dependencies
RUN pip install -r requirements/$requirement_file

RUN chmod +x entrypoint.py
CMD ["python", "/job_seeker_data/entrypoint.py"]

# for build image use these structure
# sudo docker build --build-arg requirement_file=production.txt --no-cache -t eclaim_production:latest -f Dockerfile .
