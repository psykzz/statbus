FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV STATIC_PATH /static/frontend

COPY ./frontend /static/frontend
COPY ./statbus /app/statbus
ADD ./uwsgi.ini /app/uwsgi.ini

