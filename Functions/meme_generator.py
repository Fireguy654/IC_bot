import os

from PIL import Image, ImageFont, ImageDraw
import speech_recognition as sr
import ffmpy  # Используется для проеобразования аудиофайлов.


FONT_SIZE_TO_WEIGHT = 1.618
MSG_ABOUT_STOP = 'Если вы передумали его создавать, введите "/stop".'
MSG_TO_SEND_PHOTO = "Пожалуйста, отправьте картинку для создания мема."
VOICE_FILENAME = "voice.wav"


def create_meme_processing(update, context):
    if not context.args:
        update.message.reply_text(
            "Отправьте надпись к мему, это можно сделать даже с помощью голосового сообщения." + "\n" +
            MSG_ABOUT_STOP)
        return 1
    context.user_data["text"] = " ".join(context.args)
    return 2


def get_meme_text(update, context):
    if update.message.text:
        if update.message.text == "/stop":  # Обработка команды стоп.
            return stop(update, context)
        context.user_data["text"] = update.message.text.strip()
        update.message.reply_text(
            MSG_TO_SEND_PHOTO + "\n" +
            MSG_ABOUT_STOP)
        return 2
    if update.message.voice:  # Распознавание и преобразование голосовухи в текст.
        filename = update.message.voice.get_file().download()
        ffmpy.FFmpeg(executable="Data\\ffmpeg\\ffmpeg.exe",
                     inputs={filename: None},
                     outputs={VOICE_FILENAME: None}).run()  # Преобразование OGA в wav.
        os.remove(filename)
        audio = sr.AudioFile(VOICE_FILENAME)
        sr_obj = sr.Recognizer()
        with audio as source:
            audio_data = sr_obj.record(source)
            try:
                text = sr_obj.recognize_google(audio_data, language="ru-RU")
            except sr.UnknownValueError:  # Обработка ошибки распознавания текста.
                update.message.reply_text("Вы ничего не сказали, попробуйте ещё раз, чтобы создать мем." + "\n"
                                          + MSG_ABOUT_STOP)
                return 1
            except sr.RequestError:  # Обработка ошибки, когда сервисы google недоступны.
                update.message.reply_text("Сервисы по распознаванию речи недоступны," +
                                          " пожалуйста, попробуйте позже.")
                return -1
        os.remove(VOICE_FILENAME)
        context.user_data["text"] = text
        update.message.reply_text(MSG_TO_SEND_PHOTO + "\n" +
                                  MSG_ABOUT_STOP)
        return 2
    update.message.reply_text(
        "Ошибка, пожалуйста, отправьте надпись к мему." + "\n" +
        MSG_ABOUT_STOP)
    return 1


def get_meme_photo(update, context):
    if update.message.text == "/stop":
        return stop(update, context)
    if update.message.photo:
        photo = update.message.photo[0]
        filename = photo.get_file().download()

        img = Image.open(filename)
        try:
            font_size = img.height // 10
            if font_size <= 5 or \
                    (font_size // FONT_SIZE_TO_WEIGHT) * len(context.user_data["text"]) > img.width * 0.9:
                context.user_data["error"] = "res"
                img.close()
                os.remove(filename)
                return send_error(update, context)  # Обработка случая, когда размер шрифта мал или текст не влезает.
            text_dist = (img.width // 2 -
                         int(font_size * len(context.user_data["text"]) // (FONT_SIZE_TO_WEIGHT * 2)),
                         int(img.height * 0.98) - font_size)  # Определение места текста.
        except ValueError:
            os.remove(filename)
            return send_error(update, context)
        font = ImageFont.truetype("Data/Uni_Sans.ttf", font_size)
        draw = ImageDraw.Draw(img)
        draw.text(text_dist, context.user_data["text"], font=font)
        img.save(filename)

        update.message.reply_text("Ловите ваш мем. :)")
        with open(filename, "rb") as f:
            update.message.reply_photo(f)
        os.remove(filename)
        return -1
    update.message.reply_text(
        "Пожалуйста, отправьте картинку для создания мема." + "\n"
        + MSG_ABOUT_STOP)
    return 2


def stop(update, context):
    update.message.reply_text("Спасибо, что попытались.")
    return -1


def send_error(update, context):
    if context.user_data.get("error") == "res":
        update.message.reply_text("Извините, это изображение не подходит для создания мема," +
                                  " попробуйте другое.\n" + MSG_ABOUT_STOP)
        return 2
    update.message.reply_text("Извините, произошла ошибка.")
    return -1

