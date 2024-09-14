import flet as ft
import library.uploader
from library.files import File
from library.decoder import decode
import random
import base64
import os
import time
import library.accounts


def save_base64_image(base64_string, file_path):
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(base64_string))


def createTabel():
    progress = ft.ProgressBar(value=0)
    progress_text = ft.Text(f'Прогресс {progress.value}%')

    accounts = library.accounts.loadAccounts()

    file = File('data/fashiongirl.data')
    data = decode(file.contents)
    random.shuffle(data)

    def __start(e):
        e.page.controls[0].tabs[2].content.content.controls[0].disabled = True
        e.page.update()
        UPLOADER_DATA = []
        for account in accounts.data:
            UPLOADER_DATA.append(library.uploader.Uploader(
                account.username, account.password))

        all_len = len(data)
        directory = os.path.dirname('data/temp/1.jpeg')
        if not os.path.exists(directory):
            os.makedirs(directory)

        for _i, post in enumerate(data):
            for _id, photo in enumerate(post.photos):
                save_base64_image(photo, f'data/temp/{_id}.jpeg')
            for uploader in UPLOADER_DATA:
                uploader.post(post)

            percent = (100*(_i+1))/all_len
            progress.value = round(percent/100, 2)
            progress_text.value = f'Прогресс {round(percent, 2)}%   {
                _i+1}/{all_len}'
            e.page.update()
            time.sleep(2)
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        uploader.stop()

    rows = ft.Column(
        [
            ft.TextButton(
                'Запустить', on_click=__start),
            progress_text, progress,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return rows
