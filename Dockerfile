FROM python:3.5-onbuild
ENV DJANGO_SETTINGS_MODULE=webhookmq.settings
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
