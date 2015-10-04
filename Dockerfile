FROM python:3.5-onbuild
CMD [ "uwsgi", "--ini", "uwsgi.ini" ]
