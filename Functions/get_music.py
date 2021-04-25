import os
import deezer
import requests
from PIL import Image
IMG_FILENAME_TEMPLATE = "img"


def get_music(update, context):
    try:
        need_tracks = int(context.args[0])
        music_name = " ".join(context.args[1:])

        if need_tracks < 1:
            raise ValueError
    except (ValueError, IndexError):
        update.message.reply_text("Некорректно указаны данные для нахождения трека.")
        return

    client = deezer.Client()
    tracks = client.search(music_name, relation="track")  # Поиск треков.
    tracks_found = len(tracks)
    if tracks_found == 0:
        update.message.reply_text("Такие треки не найдены. :(")
        return

    for track_num, track in enumerate(tracks):
        if track_num == need_tracks:
            return
        track_data = track.asdict()  # Перевод данных о треке в словарь.
        name = track_data["title"]
        album = track_data["album"]["title"]
        image_url = track_data["album"]["cover_medium"]
        explicit = track_data["explicit_lyrics"]
        link = track_data["link"]
        if explicit:
            sign = " 🅴"
        else:
            sign = ""
        info = name + sign + " | " + album + " | " + link

        # Получение и сохранение обложки альбома.
        image = Image.open(requests.get(image_url, stream=True).raw)
        image_filename = IMG_FILENAME_TEMPLATE + "." + image_url.split(".")[-1]
        image.save(image_filename)

        # Отправка обложки и данных.
        with open(image_filename, "rb") as f:
            update.message.reply_photo(photo=f, caption=info)
        os.remove(image_filename)




