FROM ubuntu:16.04

ADD ./install/sources.list /etc/apt/sources.list
ADD ./install/install.sh /app/install.sh
ADD ./install/ssl /app/ssl
ADD ./install/requirements.txt /app/requirements.txt

RUN ["bash","/app/install.sh"]


RUN apt install -y  tzdata
RUN rm /etc/localtime
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone


ADD ./install/run.sh /run.sh
ADD ./install/face_web /app/face_web
CMD ["bash","/run.sh"]
