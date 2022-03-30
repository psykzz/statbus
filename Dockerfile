FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./statbus /app/statbus
ADD ./uwsgi.ini /app/uwsgi.ini
