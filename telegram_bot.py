import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, filters, CallbackContext, CommandHandler
from essentia.standard import MonoLoader, RhythmExtractor2013, KeyExtractor

# Camelot mapping
CAMELot_MAP = {
    # Major keys
    (0, 'major'): '8B', (7, 'major'): '9B', (2, 'major'): '10B', (9, 'major'): '11B',
    (4, 'major'): '12B', (11, 'major'): '1B', (6, 'major'): '2B', (1, 'major'): '3B',
    (8, 'major'): '4B', (3, 'major'): '5B', (10, 'major'): '6B', (5, 'major'): '7B',
    # Minor keys
    (9, 'minor'): '8A', (4, 'minor'): '9A', (11, 'minor'): '10A', (6, 'minor'): '11A',
    (1, 'minor'): '12A', (8, 'minor'): '1A', (3, 'minor'): '2A', (10, 'minor'): '3A',
    (5, 'minor'): '4A', (0, 'minor'): '5A', (7, 'minor'): '6A', (2, 'minor'): '7A',
}

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DOWNLOAD_DIR = 'downloads'


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Пришли мне аудиофайл, и я определю его BPM и Camelot key."
    )


def handle_audio(update: Update, context: CallbackContext):
    msg = update.message
    audio = msg.audio or msg.document
    if not audio:
        return msg.reply_text("Пожалуйста, отправь мне аудиофайл (mp3, wav и т.п.).")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file = context.bot.get_file(audio.file_id)
    local_path = os.path.join(DOWNLOAD_DIR, f"{audio.file_id}.mp3")
    file.download(local_path)

    tempo, key, scale = analyze_audio(local_path)
    camelot = CAMELot_MAP.get((int(key), scale), 'Unknown')

    msg.reply_text(
        f"🎵 BPM: {tempo:.2f}\n🎹 Key: {key} ({scale})\n🔄 Camelot: {camelot}"
    )


def analyze_audio(path: str):
    loader = MonoLoader(filename=path)
    audio = loader()

    tempo, _, _, _, _ = RhythmExtractor2013(method="multifeature")(audio)
    key, scale, _ = KeyExtractor()(audio)

    return tempo, int(key), scale


if __name__ == '__main__':
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(filters.AUDIO | filters.Document.ALL, handle_audio))
    updater.start_polling()
    updater.idle()
