import flet as ft
import library.parsers.fashiongirl


def createTabel():
    progress = ft.ProgressBar(value=0)
    progress_text = ft.Text(f'Прогресс {progress.value}%')

    def __init(e):
        global init
        init = library.parsers.fashiongirl.parsing()
        print(init)

    def __start(e):
        print('\n\n', init)
        library.parsers.fashiongirl.loader(e, init)
    rows = ft.Column(
        [
            ft.TextButton('Инициализация', on_click=__init),
            ft.TextButton(
                'Скачать', on_click=__start),
            progress_text, progress,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return rows
