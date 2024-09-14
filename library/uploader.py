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
        # self.accounts = accounts
        self.file = File('data/uploads.data')
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome(self.set_options())
        self.run()
        self.login()

    def set_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.add_argument("force-device-scale-factor=0.3")
        options.add_experimental_option("detach", False)
        options.add_argument("--headless")
        return options

    def url_has_changed(self, old_url):
        return self.driver.current_url != old_url

    def login(self):
        self.driver.refresh()
        name = self.driver.find_element(By.NAME, 'username')
        name.send_keys(self.username)

        password = self.driver.find_element(By.NAME, 'password')
        password.send_keys(self.password)

        submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit.click()

    def photo_loader(self, photos: list):
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'input[type="file"]'))
        )

        directory = Path('data/temp/')
        file_names = [file.name for file in directory.iterdir()
                      if file.is_file()]

        for photo in file_names:
            file_input.send_keys(os.path.abspath(f'data/temp/{photo}'))

        accept = self.driver.find_element(
            By.XPATH, "//button[text()='Перейти до завантаження фотографій']")
        # accept.click()

    def post(self, data: Decode):
        # check
        if data.url in self.file.contents:
            return
        # title
        title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'product-name'))
        )
        title.send_keys(data.title)

        # Ожидаем описание
        description = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'product-description'))
        )
        description.send_keys(data.description)
        # state
        state = self.driver.find_element(By.ID, 'react-select-2-placeholder')
        state.click()
        # state new
        state_new = self.driver.find_element(
            By.ID, 'react-select-2-option-0')
        state_new.click()
        # section
        section = self.driver.find_element(
            By.XPATH, "//button[p[text()='Жіночий одяг']]")
        section.click()
        # section category
        section_category = self.driver.find_element(
            By.XPATH, f"//button[text()='{data.category}']")
        section_category.click()
        # section subcategory
        section_subcategory = self.driver.find_element(
            By.XPATH, f"//button[text()='{data.subcategory}']")
        section_subcategory.click()
        # more size label
        size_label = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='В мене є декілька розмірів']"))
        )
        size_label.click()
        # size selection
        succes = 0
        for size in data.sizes:
            size_rebuild = str(int(size)-8)
            try:
                size_button = self.driver.find_element(
                    By.XPATH, f"//p[text()={size_rebuild}]")
                size_button.click()
                succes += 1
            except:
                continue
        if succes == 0:
            size_button = self.driver.find_element(
                By.XPATH, "//p[text()='Інший']")
            size_button.click()
        # color selection
        succes = 0
        for color in data.colors:
            try:
                color_button = self.driver.find_element(
                    By.XPATH, f"//span[text()={color}]")
                color_button.click()
                succes += 1
            except:
                continue
        if succes == 0:
            color_button = self.driver.find_element(
                By.XPATH, "//span[text()='Різнокольоровий']")
            color_button.click()
        # amount
        amount = self.driver.find_element(By.XPATH, "//input[@name='count']")
        amount.send_keys(data.amount)
        # price
        price = self.driver.find_element(By.ID, 'price')
        price.send_keys(str(int(data.price)+300))
        # conditions
        conditions = self.driver.find_element(
            By.XPATH, "//label[@for='price']")
        conditions.click()
        # tags
        tags = self.driver.find_element(
            By.XPATH, "//input[@placeholder='Введіть ключові слова']")
        tags.send_keys(
            'Одежа, Сукня, Футболка, Штани, Сорочка, Пальто, Куртка, Светр, Плаття, Юбка, Шорти, Кардиган, Блузка, Жилет, Костюм, Сукня Zara,')
        # load photos
        self.photo_loader(data.photos)
        # verification
        verification = self.driver.find_element(
            By.XPATH, "//label[@for='i-took-pic']")
        self.driver.execute_script("arguments[0].click();", verification)
        # posting button
        posting_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[text()='Додати річ']"))
        )
        posting_button.click()

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
