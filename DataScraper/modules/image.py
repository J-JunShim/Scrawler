import os
import winreg
import requests

from io import BytesIO
from PIL import Image


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
    resp = requests.get(src)
    arr = imread(BytesIO(
        resp.content), resp.headers['Content-Type'].split('/')[-1].split(';')[0].split('+')[0])

    return arr


def save_images(srcList, query, directory):
    from datetime import datetime

    def timestamp():
        return datetime.now().strftime('%Y-%m-%d_%H%M%S')

    directory = get_user_directory(
        'images') if directory is None else os.path.abspath(directory)

    if not os.path.isdir(directory):
        os.makedirs(directory)

    print(f"\n\nDownloading {len(srcList)} images to '{directory}'...")

    total = 0
    for i, src in enumerate(srcList, 1):
        try:
            filename = f'img{timestamp()}_{query}{i}'
            pil = download_image(src).convert('RGB')

            pil.save(f'{directory}{filename}.jpg')
        except KeyboardInterrupt:
            print('\nStop downloading!')
            break
        except:
            total -= 1
            print(f'failed: {filename}')
            pass
        else:
            total += 1
            print(f'success: {filename}')

    print(f'\n{total if total>0 else 0}/{len(srcList)} files safely done')
