import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from essentia.standard import MonoLoader, RhythmExtractor2013, KeyExtractor

# Camelot mapping
CAMELot_MAP = {
    (0, 'major'): '8B', (7, 'major'): '9B', (2, 'major'): '10B', # …
    (9, 'minor'): '8A', (4, 'minor'): '9A', (11, 'minor'): '10A', # …
}

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DOWNLOAD_DIR = 'downloads'

def start(update: Update, ctx: CallbackContext):
    update.message.reply_text(
        "Привет! Пришли аудио, я верну BPM, Key и Camelot."
    )

def handle_audio(update: Update, ctx: CallbackContext):
    msg = update.message
    audio = msg.audio or msg.document
    if not audio:
        return msg.reply_text("Пожалуйста, отправь mp3 или wav.")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    file = ctx.bot.get_file(audio.file_id)
    path = os.path.join(DOWNLOAD_DIR, f"{audio.file_id}.mp3")
    file.download(path)

    tempo, key, scale = analyze_audio(path)
    camelot = CAMELot_MAP.get((int(key), scale), 'Unknown')
    msg.reply_text(f"🎵 BPM: {tempo:.2f}\n🎹 Key: {key} ({scale})\n🔄 Camelot: {camelot}")

def analyze_audio(path: str):
    audio = MonoLoader(filename=path)()
    tempo, _, _, _, _ = RhythmExtractor2013(method="multifeature")(audio)
    key, scale, _ = KeyExtractor()(audio)
    return tempo, int(key), scale

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.audio | Filters.document, handle_audio))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
