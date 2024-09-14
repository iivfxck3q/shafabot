import flet as ft
import library.parsers.fashiongirl


def createTabel():
    progress = ft.ProgressBar(value=0)
    progress_text = ft.Text(f'Прогресс {progress.value}%')

    def __init(e):
        global init
        e.page.controls[0].tabs[1].content.content.controls[0].disabled = True
        e.page.update()
        init = library.parsers.fashiongirl.parsing()
        e.page.controls[0].tabs[1].content.content.controls[1].disabled = False
        e.page.update()

    def __start(e):
        library.parsers.fashiongirl.loader(e, init)
    rows = ft.Column(
        [
            ft.TextButton('Инициализация', on_click=__init),
            ft.TextButton(
                'Скачать', on_click=__start, disabled=True),
            progress_text, progress,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return rows
