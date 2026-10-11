FROM python:3.14-slim
WORKDIR /docker/project
COPY requirements.txt .

RUN apt-get update && apt-get install -y firefox-esr openjdk-21-jre-headless wget unzip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb && rm google-chrome-stable_current_amd64.deb

RUN VER=$(google-chrome --version | grep -oP '[\d\.]+') \
    && wget https://storage.googleapis.com/chrome-for-testing-public/$VER/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip && rm chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver && chmod +x /usr/bin/chromedriver

RUN VER=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep tag_ | grep -oP '[\d\.]+') \
    && wget https://github.com/mozilla/geckodriver/releases/download/v$VER/geckodriver-v$VER-linux64.tar.gz \
    && tar -xzf geckodriver-v$VER-linux64.tar.gz && rm geckodriver-v$VER-linux64.tar.gz \
    && mv geckodriver /usr/bin/geckodriver && chmod +x /usr/bin/geckodriver

RUN VER=2.38.1 \
    && wget https://github.com/allure-framework/allure2/releases/download/$VER/allure-$VER.zip \
    && unzip allure-$VER.zip -d /opt/allure && rm allure-$VER.zip \
    && ln -s /opt/allure/allure-$VER/bin/allure /usr/bin/allure

RUN pip install --no-cache-dir -r requirements.txt