FROM python:alpine
MAINTAINER ViTuocGia <housni.yakoob@gmail.com>

RUN apk update && apk upgrade
RUN apk add bash \
    && sed -i -e "s/bin\/ash/bin\/bash/" /etc/passwd

CMD ["true"]