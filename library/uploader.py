from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from decoder import Decode
# from library.accounts import Accounts
# t1rxdqq
# RQfuqy!@GsTb9es


class Uploader:
    def __init__(self) -> None:
        # self.accounts = accounts

        self.driver = webdriver.Chrome(self.set_options())
        self.run()
        self.login()
        input()
        we = self.driver.find_element(By.XPATH, "//input[@type='file']")
        print(we)
        input()
        self.stop()

    def set_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.add_argument("force-device-scale-factor=0.3")
        options.add_experimental_option("detach", False)
        return options

    def login(self):
        self.driver.refresh()
        name = self.driver.find_element(By.NAME, 'username')
        name.send_keys('t1rxdqq')

        password = self.driver.find_element(By.NAME, 'password')
        password.send_keys('RQfuqy!@GsTb9es')

        submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit.click()

    def photo_loader(self, photos: list):
        photos_js = json.dumps(photos)
        script = """
            var base64_images = arguments[0];
            var fileInput = document.querySelector('input[type="file"]');
            var dataTransfer = new DataTransfer();

            base64_images.forEach(function(data) {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', 'data:image/jpeg;base64,' + data, true);
                xhr.responseType = 'blob';
                xhr.onload = function() {
                    var file = new File([xhr.response], 'image_' + Date.now() + '.jpg', {type: 'image/jpeg'});
                    dataTransfer.items.add(file);
                    fileInput.files = dataTransfer.files;
                };
                xhr.send();
            });
            """
        self.driver.execute_script(script, photos_js)

    def post(self, data: Decode):
        # load photos
        self.photo_loader(data.photos)
        # title
        title = self.driver.find_element(By.ID, 'product-name')
        title.send_keys(data.title)
        # description
        description = self.driver.find_element(By.ID, 'product-description')
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
            By.XPATH, "//button[text()='Жіночий одяг']")
        section.click()
        # section category
        section_category = self.driver.find_element(
            By.XPATH, f"//button[text()={data.category}]")
        section_category.click()
        # section subcategory
        section_subcategory = self.driver.find_element(
            By.XPATH, f"//button[text()={data.subcategory}]")
        section_subcategory.click()
        # more size label
        size_label = self.driver.find_element(
            By.XPATH, "//span[text()='В мене є декілька розмірів']")
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
        price.send_keys(data.price)
        # tags
        tags = self.driver.find_element(
            By.XPATH, "//input[@placeholder='Введіть ключові слова']")
        tags.send_keys(
            'Одежа, Сукня, Футболка, Штани, Сорочка, Пальто, Куртка, Светр, Плаття, Юбка, Шорти, Кардиган, Блузка, Жилет, Костюм, Сукня Zara,')
        # verification
        verification = self.driver.find_element(
            By.XPATH, "//label[@for='i-took-pic']")
        verification.click()
        # posting button
        posting_button = self.driver.find_element(
            By.XPATH, "//button[@class='b-button b-add-product__add-button' and text()='Додати річ']")
        posting_button.click()

    def run(self):
        self.driver.get("https://shafa.ua/uk/new")

    def stop(self):
        self.driver.quit()


dr = Uploader()
