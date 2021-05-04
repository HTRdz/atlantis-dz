FROM python:3.7

ENV PATH="/scripts:${PATH}"
RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# RUN python manage.py collectstatic --noinput

CMD ["entrypoint.sh"]
