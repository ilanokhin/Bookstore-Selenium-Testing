FROM python:3.14-alpine
WORKDIR /docker/project
COPY requirements.txt .

RUN apk add --no-cache chromium-chromedriver firefox openjdk11-jre wget

RUN VER=0.37.1 \
    && wget https://github.com/mozilla/geckodriver/releases/download/v$VER/geckodriver-v$VER-linux64.tar.gz \
    && tar -xzf geckodriver-v$VER-linux64.tar.gz && rm geckodriver-v$VER-linux64.tar.gz \
    && mv geckodriver /usr/bin/geckodriver && chmod +x /usr/bin/geckodriver

RUN VER=2.38.1 \
    && wget https://github.com/allure-framework/allure2/releases/download/$VER/allure-$VER.zip \
    && unzip allure-$VER.zip -d /opt/allure && rm allure-$VER.zip \
    && ln -s /opt/allure/allure-$VER/bin/allure /usr/bin/allure

RUN pip install --no-cache-dir -r requirements.txt