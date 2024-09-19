import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from library.decoder import Decode
from library.files import File
from pathlib import Path
import os


class Uploader:
    def __init__(self, username, password) -> None:
        self.file = File('data/uploads.data')
        self.username = username
        self.password = password

        try:
            self.driver = webdriver.Edge(self.set_options('edge'))
        except:
            self.driver = webdriver.Chrome(self.set_options('chrome'))

        self.run()
        self.login()

    def set_options(self, arg):
        if arg == 'edge':
            options = webdriver.EdgeOptions()
        else:
            options = webdriver.ChromeOptions()

        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.add_argument("force-device-scale-factor=0.3")
        options.add_experimental_option("detach", False)
        options.add_argument("--headless")
        return options

    def url_has_changed(self, old_url):
        return self.driver.current_url != old_url

    def find_and_click(self, by, value, alternative=False, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value)))
        if alternative:
            element.click()
        else:
            self.driver.execute_script("arguments[0].click();", element)

    def find_and_send(self, by, value, data):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        element.send_keys(data)

    def login(self):
        self.driver.refresh()

        self.find_and_send(By.NAME, 'username', self.username)
        self.find_and_send(By.NAME, 'password', self.password)
        self.find_and_click(By.XPATH, "//button[@type='submit']")

    def photo_loader(self):
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[type="file"]'))
        )

        directory = Path('data/temp/')
        file_names = [file.name for file in directory.iterdir()
                      if file.is_file()]

        for photo in file_names:
            file_input.send_keys(os.path.abspath(f'data/temp/{photo}'))

    def post(self, data: Decode):
        # load photos
        self.photo_loader()
        # title
        self.find_and_send(By.ID, 'product-name', data.title)
        # description
        self.find_and_send(By.ID, 'product-description', data.description)
        # state
        self.find_and_click(By.ID, 'react-select-2-placeholder', True)
        # state new
        self.find_and_click(By.ID, 'react-select-2-option-0')
        # section
        self.find_and_click(By.XPATH, "//button[p[text()='Жіночий одяг']]")
        # section category
        self.find_and_click(By.XPATH, f"//button[text()='{data.category}']")
        # section subcategory
        self.find_and_click(By.XPATH, f"//button[text()='{data.subcategory}']")
        # color selection
        succes = 0
        for color in data.colors:
            try:
                self.find_and_click(
                    By.XPATH, f"//span[text()='{color}']", timeout=1)
                succes += 1
            except:
                continue
        if succes == 0:
            self.find_and_click(By.XPATH, "//span[text()='Різнокольоровий']")
        # size selection
        succes = 0
        for size in data.sizes:
            size_rebuild = str(int(size)-8)
            try:
                self.find_and_click(By.XPATH, f"//p[text()={size_rebuild}]")
                succes += 1
            except:
                continue
        if succes == 0:
            self.find_and_click(By.XPATH, "//p[text()='Інший']")
        # amount
        self.find_and_send(By.XPATH, "//input[@name='count']", data.amount)
        # price
        self.find_and_send(By.ID, 'price', str(int(data.price)+300))
        # conditions
        self.find_and_click(By.XPATH, "//label[@for='price']")
        # tags
        self.find_and_send(By.XPATH, "//input[@placeholder='Введіть ключові слова']",
                           'Одежа, Сукня, Футболка, Штани, Сорочка, Пальто, Куртка, Светр, Плаття, Юбка, Шорти, Кардиган, Блузка, Жилет, Костюм, Сукня Zara,')
        # verification
        self.find_and_click(By.XPATH, "//label[@for='i-took-pic']")
        # posting button
        self.find_and_click(By.XPATH, "//button[text()='Додати річ']")
        # write in file
        for i in range(5):
            if self.driver.current_url == 'https://shafa.ua/uk/new':
                time.sleep(1)
            else:
                break

        self.file.edit_contents(f'{data.url}\n')
        self.driver.get('https://shafa.ua/uk/new')

    def run(self):
        self.driver.get("https://shafa.ua/uk/new")

    def stop(self):
        self.driver.quit()
