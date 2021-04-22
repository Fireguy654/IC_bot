import os

from PIL import Image, ImageFont, ImageDraw
from telegram.ext import ConversationHandler


def create_meme_processing(update, context):
    if not context.args:
        update.message.reply_text(
            "Отправьте надпись к мему." + "\n" +
            'Если вы передумали его создавать, введите "/stop".')
        return 1
    context.user_data["text"] = " ".join(context.args)
    return 2


def get_meme_text(update, context):
    if update.message.text:
        context.user_data["text"] = update.message.text.strip()
        update.message.reply_text(
            "Пожалуйста, отправьте картинку для создания мема." + "\n" +
            'Если вы передумали его создавать, введите "/stop".')
        return 2
    update.message.reply_text(
        "Ошибка, пожалуйста, отправьте надпись к мему." + "\n" +
        'Если вы передумали его создавать, введите "/stop".')
    return 1


def get_meme_photo(update, context):
    if update.message.photo:
        filename = update.message.photo[0].get_file().download()
        img = Image.open(filename)
        font = ImageFont.truetype("Data/calibri.ttf", 20)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), context.user_data["text"], font=font)
        img.save(filename)
        update.message.reply_text("Ловите ваш мем :)")
        with open(filename, "rb") as f:
            update.message.reply_photo(f)
        os.remove(filename)
        return ConversationHandler.END
    update.message.reply_text(
        "Пожалуйста, отправьте картинку для создания мема." + "\n" +
        'Если вы передумали его создавать, введите "/stop".')
    return 2


def stop_meme(update, context):
    update.message.reply_text("Спасибо, что попытались.")
    return ConversationHandler.END
