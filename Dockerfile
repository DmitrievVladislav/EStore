FROM python:3.11.1

SHELL ["/bin/bash", "-c"]

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install psycopg2
RUN pip install -r /requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver"]