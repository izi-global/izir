FROM python:alpine
MAINTAINER ViTuocGia <dotiendiep@gmail.com>

EXPOSE 8000

RUN pip3 install gunicorn
RUN pip3 install izi -U
WORKDIR /src
CMD gunicorn --reload --bind=0.0.0.0:8000 __init__:__izi_wsgi__