from library.files import File
import re
import os


class AccountData:
    def __init__(self, username, password, id) -> None:
        self.username = username
        self.password = password
        self.id = id

    def __repr__(self):
        return f"AccountData(username='{self.username}', password='{self.password}', id='{self.id}')"


class Accounts:
    def __init__(self):
        self.data = []
        self.file = File('data/accounts.data')

    def put(self, data: AccountData):
        self.data.append(data)

    def save(self):
        save_txt = ''
        for data in self.data:
            save_txt += str(data)+'\n'
        self.file.edit_contents(save_txt)
        self.data = []

    def __repr__(self):
        return f"Accounts(data={self.data})"


def decode(data: str) -> Accounts:
    data = data.splitlines()
    accounts = Accounts()
    for id, _ in enumerate(data):
        match = re.search(
            r"username='(.+?)', password='(.+?)', id='(.+?)'", _)
        username = match.group(1)
        password = match.group(2)
        id = match.group(3)
        accounts.put(AccountData(username, password, id))
    return accounts


def loadAccounts():
    try:
        files = File('data/accounts.data')
        files.get_contents()
        accounts = decode(files.contents)
    except:
        accounts = Accounts()
        if not os.path.exists('data'):
            os.makedirs('data')
    return accounts
