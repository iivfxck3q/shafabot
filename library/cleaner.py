import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Cleaner:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

        self.driver = webdriver.Edge(self.set_options())
        self.run()
        self.login()

    def set_options(self) -> webdriver.EdgeOptions:
        options = webdriver.EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        # options.add_argument("force-device-scale-factor=0.3")
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

    def start(self):
        post_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//img[contains(@src, 'https://image-thumbs.shafastatic.net/')]"))
        )
        self.driver.execute_script("arguments[0].click();", post_button)

        posting_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[text()='Деактивувати']"))
        )
        posting_button.click()

        time.sleep(2)

        self.driver.get('https://shafa.ua/uk/my/clothes/active')

    def run(self):
        self.driver.get("https://shafa.ua/uk/my/clothes/active")

    def stop(self):
        self.driver.quit()
