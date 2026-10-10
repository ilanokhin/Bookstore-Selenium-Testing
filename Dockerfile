FROM python:3.14-alpine

WORKDIR /docker/project

# Установка зависимостей
RUN apk update \
  && apk add --no-cache \
    chromium firefox \
    openjdk11-jre \
    curl wget unzip \
  && rm -rf /var/cache/apk/*

# Скачиваем latest ChromeDriver
RUN CHROME_VERSION=$(chromium-browser --version | awk '{print $NF}' | cut -d'.' -f1-3) \
  && CHROMEDRIVER_URL="https://googlechromelabs.github.io/chrome-for-testing/" \
  && wget -q "https://edgedl.me.gstatic.com/edgedl/chrome/chrome-for-testing/${CHROME_VERSION}.0/linux-x64/chromedriver-linux64.zip" \
  && unzip chromedriver-linux64.zip \
  && mv chromedriver-linux64/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver \
  && rm -rf chromedriver-linux64.zip chromedriver-linux64

# Скачиваем latest GeckoDriver
RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep tag_name | cut -d'"' -f4) \
  && curl -L "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" | tar xz \
  && mv geckodriver /usr/bin/geckodriver \
  && chmod +x /usr/bin/geckodriver

# Allure 2.38.1 (фиксированная версия)
RUN curl -o allure.zip -L "https://github.com/allure-framework/allure2/releases/download/2.38.1/allure-2.38.1.zip" \
  && unzip allure.zip -d /opt/allure \
  && rm allure.zip \
  && ln -s /opt/allure/allure-2.38.1/bin/allure /usr/bin/allure

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
