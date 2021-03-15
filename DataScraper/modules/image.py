import os
import winreg
import requests

from io import BytesIO
from PIL import Image

from matplotlib import pyplot as plt


def get_user_directory(extraDir=None):
    directory = os.path.join(os.path.expanduser('~'), 'Downloads')

    # if os.name == 'nt':
    #     sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    #     downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'

    #     with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
    #         directory = winreg.QueryValueEx(key, downloads_guid)[0]

    return os.path.join(directory, extraDir) if extraDir else directory


def download_image(src):
    response = requests.get(src)

    return Image.open(BytesIO(response.content))


def image_array(src):
    response = requests.get(src)
    imageArray = plt.imread(BytesIO(
        response.content), response.headers['Content-Type'].split('/')[-1].split(';')[0].split('+')[0])

    return imageArray
