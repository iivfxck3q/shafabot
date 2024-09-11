import os


class File:
    def __init__(self, path) -> None:
        self.path = path
        self.contents = None

        self.checks()

    def save(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(self.contents)

    def checks(self):
        directory = os.path.dirname(self.path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            self.get_contents()
        except:
            self.contents = ''

    def get_contents(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            self.contents = file.read()

    def edit_contents(self, data):
        for line in data.splitlines():
            if line in self.contents:
                continue
            self.contents += line+'\n'
        self.save()
