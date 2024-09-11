import flet as ft
import apps.accounts
import apps.downloads


class AppData:
    pass


def tabGenerator(name, contents, alignment=ft.alignment.center):
    return ft.Tab(
        text=name,
        content=ft.Container(
            content=contents, alignment=alignment)
    )


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Shafa Bot v2'
        self.page.window.width = 720
        self.page.window.height = 600
        self.page.window.resizable = True
        self.page.window.center()
        self.page.window.full_screen = False
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.page.add(ft.Tabs(      # add tabs
            selected_index=0,
            animation_duration=300,
            tab_alignment=ft.TabAlignment.CENTER,
            tabs=[
                tabGenerator(
                    'Аккаунты', apps.accounts.createTabel(), ft.alignment.top_center),
                tabGenerator('Загрузки', apps.downloads.createTabel()),
                tabGenerator('Запуск', ft.Text("This is Tab 2")),
            ],
            expand=1,
        ))

    def quit(self):
        self.page.window_destroy()


def run():
    ft.app(App)


if __name__ == '__main__':
    run()
