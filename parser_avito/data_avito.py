from selenium import webdriver
from time import sleep
from PIL import Image
from pytesseract import image_to_string
import base64


class Bot:
    def __init__(self, url: str):
        self.driver = webdriver.Firefox(executable_path='../files/geckodriver.exe')
        self.url = url
        self.navigate()

    # def take_screenshot(self):
    #     self.driver.save_screenshot('files/avito_screenshot.png')
    #
    # def tel_recon(self):
    #     image = Image.open('files/tel.gif')
    #     self.number_phone = image_to_string(image).strip()
    #
    # def crop(self, location, size):
    #     image = Image.open('files/avito_screenshot.png')
    #     x = location['x']
    #     y = location['y']
    #     width = size['width']
    #     height = size['height']
    #     image.crop((x, y, x + width, y + height)).save('files/tel.gif')
    #     self.tel_recon()

    def navigate(self):
        self.driver.get(self.url)

        buttons = self.driver.find_elements_by_css_selector('button.button-button-3p4ra')
        for button in buttons:
            button.click()
            sleep(3)
            # print(button)



        images = self.driver.find_elements_by_css_selector('img.button-phone-image-3Vvg8')
        for image in images:
            print(image)

        # location = image.location
        # size = image.size
        # self.crop(location, size)


if __name__ == '__main__':
    Bot('https://www.avito.ru/ivanovo/predlozheniya_uslug/transport_perevozki/spetstekhnika-ASgBAgICAkSYC8SfAZoL3J8B')
