import flet as ft
import library.accounts


def createTabel():
    accounts = library.accounts.loadAccounts()
    rows = []

    username = ft.TextField(label="Логин")
    password = ft.TextField(label="Пароль")

    def submit__(e):
        if username.value == '' and password.value == '':
            return
        __id = len(accounts.data)+1
        accounts.data.clear()
        accounts.put(library.accounts.AccountData(
            username.value, password.value, __id))
        accounts.save()
        e.page.controls[0].tabs[0].content = createTabel()
        e.page.update()
    submit = ft.TextButton(text='Подтвердить', on_click=submit__)
    for account in accounts.data:
        rows.append(ft.DataRow(cells=[ft.DataCell(
            ft.Text(f"{account.username}")), ft.DataCell(ft.Text(f"{account.password}"))]))
    table = ft.Column([ft.DataTable(
        column_spacing=460,
        columns=[
            ft.DataColumn(ft.Text("Логин")),
            ft.DataColumn(ft.Text("Пароль"))
        ],
        rows=rows,
    ), ft.Row([username, password], alignment=ft.MainAxisAlignment.CENTER), submit], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    return table
