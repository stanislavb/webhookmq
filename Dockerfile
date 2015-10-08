FROM python:3.5-onbuild
ENV DJANGO_SETTINGS_MODULE=webhookmq.settings
EXPOSE 8080
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
