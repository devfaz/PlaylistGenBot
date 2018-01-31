FROM ubuntu:xenial

RUN apt-get -q update \
	&& apt-get -qy install python-pip \
	&& pip install python-telegram-bot --upgrade 

COPY pastebin.py /usr/local/lib/python2.7/dist-packages/pastebin.py
COPY bot.py /usr/local/bin/bot.py

ENTRYPOINT /usr/local/bin/bot.py
