FROM alpine

ADD . /root
WORKDIR /root

RUN echo "Installing system packages..."
RUN apk add --no-cache mysql-client python3 python3-dev ca-certificates libc-dev g++ && \
		python3 -m ensurepip && \
    pip3 install --no-cache-dir --upgrade pip setuptools

RUN echo "Installing python dependencies..."
RUN pip3 install --no-cache-dir --upgrade pip && \
		pip3 install --no-cache-dir -r requirements.txt

CMD /root/setup.sh $MYSQL_HOST $MYSQL_ROOT_PASSWORD

