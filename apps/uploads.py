import flet as ft
import library.uploader
import library.cleaner
from library.files import File
from library.decoder import decode
import random
import base64
import os
import time
from PIL import Image, ImageDraw
import io
import library.accounts


def save_base64_image(base64_string, file_path):
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))

    width, height = image.size

    random_x = random.randint(0, width - 1)
    random_y = random.randint(0, height - 1)

    draw = ImageDraw.Draw(image)
    draw.point((random_x, random_y), fill="black")

    image.save(file_path)


def createTabel():
    progress = ft.ProgressBar(value=0)
    progress_text = ft.Text(f'Прогресс {progress.value}%')

    def __cleaner(e):
        accounts = library.accounts.loadAccounts()
        CLEANER_DATA = []
        for account in accounts.data:
            CLEANER_DATA.append(library.cleaner.Cleaner(
                account.username, account.password))
        while True:
            for _iu, cleaner in enumerate(CLEANER_DATA):
                try:
                    cleaner.start()
                except:
                    CLEANER_DATA.remove(cleaner)

    def __start(e):
        accounts = library.accounts.loadAccounts()

        file = File('data/fashiongirl.data')
        data = decode(file.contents)

        e.page.controls[0].tabs[2].content.content.controls[0].disabled = True
        e.page.update()
        UPLOADER_DATA = []
        RANDOM_DATA = []
        for account in accounts.data:
            UPLOADER_DATA.append(library.uploader.Uploader(
                account.username, account.password))

            data_copy = data[:]
            random.shuffle(data_copy)
            RANDOM_DATA.append(data_copy)

        all_len = len(data)
        directory = os.path.dirname('data/temp/1.jpeg')
        if not os.path.exists(directory):
            os.makedirs(directory)

        for _i, post in enumerate(data):
            for _iu, uploader in enumerate(UPLOADER_DATA):
                for _id, photo in enumerate(RANDOM_DATA[_iu][_i].photos):
                    save_base64_image(photo, f'data/temp/{_id}.jpeg')
                uploader.post(RANDOM_DATA[_iu][_i])
                time.sleep(2)
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

            percent = (100*(_i+1))/all_len
            progress.value = round(percent/100, 2)
            progress_text.value = f'Прогресс {round(percent, 2)} pidarasa %   {
                _i+1}/{all_len}'
            e.page.update()

        uploader.stop()

    rows = ft.Column(
        [
            ft.TextButton(
                'Запустить', on_click=__start),
            progress_text, progress,
            ft.TextButton('Очистить', on_click=__cleaner)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return rows
