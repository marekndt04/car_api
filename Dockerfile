FROM python:3.8

ENV port 8000

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE ${port}

CMD python app/manage.py runserver 0.0.0.0:${port}
