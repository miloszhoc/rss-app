FROM ubuntu:latest
COPY ./ /rss-app
WORKDIR /rss-app
RUN apt-get update && apt-get install python3-pip -y
RUN python3.8 -m pip install -r requirements.txt
ENV FLASK_APP=/rss-app/rss_app/run.py
ENV FLASK_ENV=PRODUCTION
ENV CONFIG=prod
ENV DB_HOST=173.23.1.3
ENV DB_USER=rss_user
ENV DB_PASS=rss_pass
ENV DB_NAME=rss_app_db
ENV DB_TABLE=url
ENV DB_PORT=5432
ENV SENDGRID_KEY=test
ENV FROM_EMAIL=rss_app@rss_app.com
CMD flask db upgrade -d /rss-app/rss_app/migrations && gunicorn --bind 0.0.0.0 --timeout 600 "rss_app.run:create_app('prod')" -k gevent --worker-connections 1000