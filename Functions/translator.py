from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from info import IBM_URL, IBM_KEY

MSG_ABOUT_STOP = 'Если вы передумали делать перевод, введите "/stop".'

# Инизиализация переводчика IBM.
language_translator = LanguageTranslatorV3(version='2018-05-01',
                                           authenticator=IAMAuthenticator(IBM_KEY))
language_translator.set_service_url(IBM_URL)

# Получение списка доступных для перевода языков.
langs_list = [lang_dict["language"] for lang_dict in language_translator.list_languages().get_result()["languages"]]


def translator_start(update, context):
    update.message.reply_text("Введите фразу, которую вы хотите перевести.\n" + MSG_ABOUT_STOP)
    return 1


def get_phrase(update, context):
    if update.message.text:
        if update.message.text == "/stop":
            return stop(update, context)
        context.user_data["text"] = update.message.text
        update.message.reply_text(
            "Пожалуйста, выберите язык, на который вы хотите перевести.\n" +
            "Доступны следующие языки: " +
            ", ".join(langs_list) + ".\n" + MSG_ABOUT_STOP)
    else:
        update.message.reply_text("Пожалуйста, введите фразу, которую вы хотите перевести.\n" + MSG_ABOUT_STOP)
        return 1
    return 2


def select_language(update, context):
    if update.message.text == "/stop":
        return stop(update, context)
    if update.message.text.lower() not in langs_list:
        update.message.reply_text("Выбран некорректный язык, пожалуйста, попробуйте еще раз.\n" + MSG_ABOUT_STOP)
        return 2
    dist_lang = update.message.text.lower()
    # Идентификация языка введённой фразы.
    src_lang = language_translator.identify(context.user_data["text"]).get_result()["languages"][0]["language"]

    try:
        translation = language_translator.translate(text=[context.user_data["text"]],
                                                    source=src_lang,
                                                    target=dist_lang).get_result()["translations"][0]["translation"]
        update.message.reply_text("Переведённая фраза:\n" + f'"{translation}"')
    except Exception:
        update.message.reply_text("Произошла ошибка, возможно, вы попытались перевести на тот же язык.")
    return -1


def stop(update, context):
    update.message.reply_text("Спасибо, что воспользовались переводчиком. :)")
    return -1
