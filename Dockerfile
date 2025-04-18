FROM python:3.12-slim

# Отключаем интерактивные диалоги при apt
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем системные зависимости для сборки Essentia
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfftw3-dev \
    libyaml-dev \
    libboost-all-dev \
    cmake \
    swig \
    git \
 && rm -rf /var/lib/apt/lists/*

# Клонируем и собираем Essentia из исходников
WORKDIR /opt
RUN git clone --depth 1 https://github.com/MTG/essentia.git \
 && cd essentia \
 && mkdir build && cd build \
 && cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_BINDINGS_PYTHON=ON -DBUILD_EXAMPLES=OFF \
 && make -j$(nproc) && make install && ldconfig

# Рабочая директория для бота
WORKDIR /app

# Ставим зависимости бота (уберите 'essentia' из requirements.txt)
COPY requirements.txt /app/
RUN pip install --no-cache-dir python-telegram-bot python-dotenv

# Копируем код проекта
COPY . /app
RUN mkdir -p /app/downloads

# Запуск
CMD ["python", "telegram_bot.py"]
