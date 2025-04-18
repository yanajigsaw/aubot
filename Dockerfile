# Берём официальную Ubuntu
FROM ubuntu:24.04

# Не ругаемся на диалоги и сразу обновляем пакеты
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3-pip python3-dev \
       libfftw3-dev libyaml-dev libboost-all-dev cmake swig git \
    && rm -rf /var/lib/apt/lists/*

# Ставим Python‑пакеты
RUN pip3 install --no-cache-dir \
      python-telegram-bot \
      python-dotenv \
      essentia

# Копируем код бота внутрь контейнера
WORKDIR /app
COPY . /app

# Создаём папку для временных файлов
RUN mkdir -p /app/downloads

# Экспортим порт (для webhook‑режима, если понадобится)
EXPOSE 8443

# Запускаем бот
CMD ["python3", "telegram_bot.py"]
