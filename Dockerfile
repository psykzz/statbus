FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV STATIC_PATH /static/frontend
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./frontend/build /static/frontend
COPY ./statbus /app/statbus
ADD ./uwsgi.ini /app/uwsgi.ini
