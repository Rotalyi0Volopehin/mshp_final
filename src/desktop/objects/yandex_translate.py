"""
Переводчик текста квестов
"""
import requests
import os


class Translator:
    """
    Класс переводчика, для работы необходимо облако yandex cloud и токен
    """
    def __init__(self):
        self.url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
        token_path = os.path.join('quests', 'token')
        file = open(token_path, 'r')
        data = file.read()
        self.token_string = 'Bearer ' + data
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': self.token_string}
        self.translate_data = {
            "folder_id": "b1gb641rullkr99au8k2",
            "texts": ["Hello"],
            "targetLanguageCode": "ru"
        }
        file.close()

    def translate(self, text="Привет", target_language="en"):
        if target_language == "ru":
            return text
        self.translate_data = {
            "folder_id": "b1gb641rullkr99au8k2",
            "texts": [text],
            "targetLanguageCode": target_language
        }
        response = requests.post(self.url, json=self.translate_data,
                                 headers=self.headers)
        if response.status_code == 200:
            response_string = (str(response.json()['translations']))
            translated_text = response_string[response_string.find('text') + 8:
                                              response_string.find("detectedLanguageCode") - 4]
            return translated_text
        else:
            return str(response.status_code)
