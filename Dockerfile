FROM python:3.12

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y libcairo2 libcairo2-dev pkg-config python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
