FROM ubuntu:latest
RUN apt-get update && apt-get install -y cron
RUN apt-get install -y apt-utils
RUN apt-get install -y curl
ADD crontab /etc/cron.d/simple-cron
RUN chmod 0644 /etc/cron.d/simple-cron
RUN crontab /etc/cron.d/simple-cron
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log