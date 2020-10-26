from ubuntu

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends --no-install-suggests \
            ca-certificates \
 && update-ca-certificates \
 && apt-get install -y --no-install-recommends --no-install-suggests \
	curl \
        bzip2 \
        wget \
        sudo \
	python3 \
        python3-distutils \
        python3-apt \
        python3-dev \
	gnupg2 \
	unzip \
	vim \
	cron \

 # install PIP
 && wget https://bootstrap.pypa.io/get-pip.py \
 && sudo python3 get-pip.py \


# Install Google Chrome
 && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
 && apt-get update && apt-get install -y google-chrome-stable \

# install chromedriver
 && wget https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip \
 && unzip chromedriver_linux64.zip \
 && mv chromedriver /usr/bin/ \

 && pip3 install httpserver\
    && pip3 install prometheus_client\
    && pip3 install selenium\
    && pip3 install requests\
    && pip3 install regex\
    && pip3 install bs4\
    && pip3 install pymongo\
    && pip3 install simplejson


COPY  cron-linkedin /etc/cron.d/
COPY data_collector.py /bin/
COPY prom_collector.py /bin/
COPY credential.py /bin/
RUN chmod +x /bin/data_collector.py
CMD python3 -u /bin/data_collector.py