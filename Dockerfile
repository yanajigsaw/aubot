# Используем официальный образ Essentia с Python привязками
# (ubuntu20.04-v2.1_beta5 или latest nightly при необходимости)
FROM ghcr.io/mtg/essentia:ubuntu20.04-v2.1_beta5

# Рабочая директория для кода бота
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . /app

# Создаём папку для сохранения загружаемых аудиофайлов
RUN mkdir -p downloads

# Точка входа: запуск бота
CMD ["python", "telegram_bot.py"]