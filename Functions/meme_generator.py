import os

from PIL import Image, ImageFont, ImageDraw

MIN_SIZE = 200, 200


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
        if update.message.text == "/stop":
            return stop(update, context)
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
    if update.message.text == "/stop":
        return stop(update, context)
    if update.message.photo:
        photo = update.message.photo[0]
        filename = photo.get_file().download()
        width, height = photo.width, photo.height
        if width <= MIN_SIZE[0] or height <= MIN_SIZE[1]:
            return wrong_res_photo(update, context)
        img = Image.open(filename)
        font = ImageFont.truetype("Data/calibri.ttf", 20)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), context.user_data["text"], font=font)
        img.save(filename)
        update.message.reply_text("Ловите ваш мем :)")
        with open(filename, "rb") as f:
            update.message.reply_photo(f)
        os.remove(filename)
        return -1
    update.message.reply_text(
        "Пожалуйста, отправьте картинку для создания мема." + "\n" +
        'Если вы передумали его создавать, введите "/stop".')
    return 2


def stop(update, context):
    update.message.reply_text("Спасибо, что попытались.")
    return -1


def wrong_res_photo(update, context):
    update.message.reply_text("Разрешение изображения меньше, чем 200x200." + "\n" +
                              "Пожалуйста, отправьте новую картинку. \UF09F9189" + "\n" +
                              'Если вы передумали создавать мем, введите "/stop".')
    return 2

