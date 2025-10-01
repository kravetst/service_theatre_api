FROM python:3.11-slim

LABEL maintainer=taraskravetc28@gmail.com

ENV PYTHONBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /vol/web/media

COPY . /app/

EXPOSE 8000

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

RUN chown -R django-user:django-user /vol/
RUN chmod -R 755 /vol/web/

USER django-user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
