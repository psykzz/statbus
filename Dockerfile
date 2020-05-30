FROM node as build

WORKDIR /app
COPY ./frontend/ /app
RUN yarn
RUN yarn build

FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV STATIC_PATH /static/frontend
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY --from=build /app/build  /static/frontend
COPY ./statbus /app/statbus
ADD ./uwsgi.ini /app/uwsgi.ini
