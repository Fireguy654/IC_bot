import os
import requests
from random import randrange, sample
from PIL import Image
import info

URL = "https://pixabay.com/api/"
IMG_FILENAME_TEMPLATE = "img"
api_key = info.PIXABAY_KEY


def get_image(update, context):
    if not context.args:
        update.message.reply_text("Вы не ввели текст, по которому хотите найти картинку.")
        return
    params = {"key": api_key, "q": " ".join(context.args)}

    image_response = requests.get(URL, params=params)
    response_json = image_response.json()
    images_found = len(response_json["hits"])
    if images_found == 0:
        update.message.reply_text(f"К сожалению, таких фотографий не найдено.")
        return
    image_url = response_json["hits"][randrange(images_found)]['largeImageURL']

    image = Image.open(requests.get(image_url, stream=True).raw)
    image_filename = IMG_FILENAME_TEMPLATE + "." + image_url.split(".")[-1]
    image.save(image_filename)

    with open(image_filename, "rb") as f:
        update.message.reply_photo(f)
    os.remove(image_filename)


def get_few_images(update, context):
    try:
        images_num = int(context.args[0])
        images_text = " ".join(context.args[1:])
    except (ValueError, IndexError):
        update.message.reply_text("Неверно введены параметры, пожалуйста, попробуйте ещё раз.")
        return

    params = {"key": api_key, "q": images_text}
    image_response = requests.get(URL, params=params)
    response_json = image_response.json()
    images_found = len(response_json["hits"])
    if images_found == 0:
        update.message.reply_text(f"К сожалению, таких фотографий не найдено.")
        return
    elif images_found < images_num:
        update.message.reply_text(f"Нашлось лишь {images_found} фотографий, вот они:")
        chosen_images_nums = range(images_found)
    else:
        chosen_images_nums = sample(range(images_found), images_num)

    for num_in_row, image_num in enumerate(chosen_images_nums):
        image_url = response_json["hits"][image_num]['webformatURL']

        image = Image.open(requests.get(image_url, stream=True).raw)
        image_filename = IMG_FILENAME_TEMPLATE + "." + image_url.split(".")[-1]
        image.save(image_filename)

        with open(image_filename, "rb") as f:
            update.message.reply_photo(f, caption=f"Держите фотографию №{num_in_row + 1}.")
        os.remove(image_filename)

