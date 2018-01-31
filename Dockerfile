FROM ubuntu:xenial

RUN apt-get -q update \
	&& apt-get -qy install python-pip \
	&& pip install python-telegram-bot --upgrade 

COPY bot.py /usr/local/bin/bot.py

ENTRYPOINT /usr/local/bin/bot.py
