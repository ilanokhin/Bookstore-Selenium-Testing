FROM python:3.14-alpine
WORKDIR /docker/project
COPY requirements.txt .

RUN apk update \
  && apk add --no-cache firefox openjdk11-jre curl  \
  && curl -o allure.zip -L "https://github.com/allure-framework/allure2/releases/download/2.38.1/allure-2.38.1.zip" \
  && unzip allure.zip -d /opt/allure \
  && rm allure.zip \
  && ln -s /opt/allure/allure-2.38.1/bin/allure /usr/bin/allure \
  && GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep tag_name | cut -d'"' -f4) \
  && wget https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
  && tar -xzf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
  && mv geckodriver /usr/bin/geckodriver \
  && chmod +x /usr/bin/geckodriver \
  && CHROMEDRIVER_VERSION=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json | jq -r '.versions[-1].version') \
  && wget https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip \
  && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver \
  && pip install --no-cache-dir -r requirements.txt
