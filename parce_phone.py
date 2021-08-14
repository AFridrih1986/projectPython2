from selenium import webdriver
from time import sleep
from PIL import Image
from pytesseract import image_to_string
import base64

class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='files/geckodriver.exe')
        self.navigate()

    def take_screenshot(self):
        self.driver.save_screenshot('files/avito_screenshot.png')

    def tel_recon(self):
        image = Image.open('files/tel.gif')
        self.number_phone = image_to_string(image).strip()

    def crop(self, location, size):
        image = Image.open('files/avito_screenshot.png')
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']
        image.crop((x, y, x+width, y+height)).save('files/tel.gif')
        self.tel_recon()

    def navigate(self):
        self.driver.get('https://www.avito.ru/rostov-na-donu/predlozheniya_uslug/evakuator_1187800124')

        button = self.driver.find_element_by_xpath('//a[@class="button item-phone-button js-item-phone-button button-origin contactBar_greenColor button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card contactBar_height"]')

        button.click()
        sleep(3)
        self.take_screenshot()

        image = self.driver.find_element_by_xpath('//div[@class="item-phone-big-number js-item-phone-big-number"]//*')
        location = image.location
        size = image.size
        self.crop(location, size)

