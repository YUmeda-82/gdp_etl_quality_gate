FROM python:3.12.3
RUN apt-get update &&\
    apt-get install -y --no-install-recommends default-jre &&\
    rm -rf /var/lib/apt/lists/*
WORKDIR /gdp_etl_quality_gate
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]