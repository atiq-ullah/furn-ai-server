FROM python:3.12
EXPOSE 8000
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
RUN chmod +x celery_entrypoint.sh