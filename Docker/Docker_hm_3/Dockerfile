FROM python:latest
LABEL authors="Lenovo"

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install psutil -U

COPY memory_info.py .

RUN mkdir -p data

ENTRYPOINT ["python3", "memory_info.py"]