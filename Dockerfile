FROM python:3.14-alpine
WORKDIR /docker/project
COPY requirements.txt .

RUN apk add --no-cache chromium-chromedriver firefox geckodriver openjdk11-jre curl  \
  && curl -o allure.zip -L "https://github.com/allure-framework/allure2/releases/download/2.38.1/allure-2.38.1.zip" \
  && unzip allure.zip -d /opt/allure \
  && rm allure.zip \
  && ln -s /opt/allure/allure-2.38.1/bin/allure /usr/bin/allure \
  && pip install --no-cache-dir -r requirements.txt
