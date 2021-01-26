# -*- coding: utf-8 -*-

import time
import json
import subprocess
from sys import executable, platform
from pynput.keyboard import GlobalHotKeys
import pyautogui
import pyperclip
from urllib.parse import quote
import requests
from langdetect import detect, DetectorFactory

from apiconf import *


def translator(text, lang_param):
    translate = requests.post(API_URL.format(lang=lang_param,
                                            text=quote(text),
                                            email=EMAIL))

    if translate.status_code == 200:
        response = json.loads(translate.text)
        response_data = response["responseData"]
        response_text = response_data["translatedText"]
        return response_text


def set_lang_param(text):
    lang_param = None
    DetectorFactory.seed = 0
    try:
        detected_language = detect(text)
        print(detected_language)

        if detected_language == 'bg':
            detected_language = 'ru'
        if detected_language == 'ru':
            lang_param = 'ru|en'
        else:
            lang_param = ''.join([detected_language, '|ru'])
    except Exception as e:
        lang_param = 'no language detected'
    return lang_param


def get_xsel_clip():
    text = subprocess.check_output('xsel', universal_newlines=True)
    return text


def get_selection():
    if platform == "linux" or platform == "darwin":
        copied_text = get_xsel_clip();
    elif platform == "win32":
        copied_text = pyperclip.paste()
    return copied_text

def on_activate_t():
    clip = get_selection();
    lang_pair = set_lang_param(clip)
    translated_text = translator(clip, lang_pair)
    subprocess.Popen([executable, 'notify.py', translated_text, lang_pair])

def hotkey_listen():
    with GlobalHotKeys({'<ctrl>+<alt>+t': on_activate_t}) as hot:
        hot.join()


if __name__ == '__main__':
    print(f'running on {platform}')
    hotkey_listen();