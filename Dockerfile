FROM python:3.7-slim

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 8050
ENV NAME World

CMD ["python3", "app.py"]
