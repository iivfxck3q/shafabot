import library.files
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

    def put(self, data: AccountData):
        self.data.append(data)

    def save(self):
        save_txt = ''
        for data in self.data:
            save_txt += str(data)+'\n'
        library.files.write_txt('data/accounts.data',
                                save_txt)
        self.data = []
        print('save!')

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
        accounts = decode(library.files.read_txt("data/accounts.data"))
    except:
        accounts = Accounts()
        if not os.path.exists('data'):
            os.makedirs('data')
    return accounts
