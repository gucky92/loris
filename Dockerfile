# this is an official Python runtime, used as the parent image
FROM continuumio/anaconda3

ADD . /app
WORKDIR /app
RUN apt-get update && apt-get install netcat -y
RUN pip install --user .
# unblock port 80 for the Flask app to run on
WORKDIR /app
EXPOSE 1234
EXPOSE 3306
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
