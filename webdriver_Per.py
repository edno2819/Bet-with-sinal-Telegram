from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from webdrivermanager import ChromeDriverManager
from selenium.webdriver.remote.remote_connection import LOGGER, logging

LOGGER.setLevel(logging.WARNING)



class Webdriver():
    def __init__(self, profiles=False, headless=False):
        self.options = webdriver.ChromeOptions()

        dir_path = os.getcwd()
        profile = os.path.join(dir_path, "profile", "wpp")

        self.options.add_argument("--headless") if headless==True else self.options.add_argument("--start-maximized")
        
        self.options.add_argument(r"--user-data-dir={}".format(profile)) if profiles==True else 0

        self.update_webdriver()
    
    def start(self):
        self.driver = webdriver.Chrome(r"chromedriver.exe", options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def update_webdriver(self):
        try:
            if 'browserVersion' in self.driver.capabilities:
                version=self.driver.capabilities['browserVersion']
            else:
                version=self.driver.capabilities['version']

            gdd = ChromeDriverManager()
            gdd.download_and_install(version)
        except:
            pass 

    def open_page(self,url):
        self.driver.get(url)
    
    def find_element(self, locator, elem=None):
        by, locator = locator
        if elem:
            return elem.find_element(by, locator)
        else:
            return self.driver.find_element(by, locator)

    def hover_to(self, locator):
        elem = locator
        if type(locator) is tuple:
            elem = EC.visibility_of_element_located(locator)
            elem = self.wait.until(elem)
        ActionChains(self.driver).move_to_element(elem).perform()

    def move_element(self, elem):
        loc=elem.location_once_scrolled_into_view
        self.driver.execute_script(f"window.scrollBy({loc['x']},{loc['y']})","")

    def click(self, locator, hover_to=True):
        elem = locator
        if type(locator) is tuple:
            elem = EC.element_to_be_clickable(locator)
            elem = self.wait.until(elem)
        if hover_to:
            self.hover_to(elem)
        elem.click()
        
    def exist(self,element):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
                    )
            return True
        except:
            return False
    
    def move_to(self):
        pass

    def wait_element(self):
        pass
    
    def fill(self, element, text):
        if type(element)==tuple:
            if self.exist(element):
                self.driver.find_element(element[0],element[1]).click()
                self.driver.find_element(element[0],element[1]).clear()
                self.driver.find_element(element[0],element[1]).send_keys(text)
        else:
            element.click()
            element.clear()
            element.send_keys(text)
    
    def get_element_attribute(self, locator, attribute):
        elem = locator
        if type(locator) is tuple:
            elem = EC.presence_of_element_located(locator)
            elem = self.wait.until(elem)
        attribute = elem.get_attribute(attribute)
        return attribute

    def find_element(self, locator, elem=None):
        by, locator = locator
        if elem:
            return elem.find_element(by, locator)
        else:
            return self.driver.find_element(by, locator)

    def find_elements(self, locator, elem=None):
        by, locator = locator
        if elem:
            return elem.find_elements(by, locator)
        else:
            return self.driver.find_elements(by, locator)

    def send_key(self, key, element=None):
        if element:
            return self.driver.find_element(element[0],element[1]).send_keys(key)
        else:
            return ActionChains(self.driver).send_keys(key).perform()

    def refresh(self):
        self.driver.refresh()

    def switch_to_frame(self, frame="son_frame"):
        if frame == 'root_frame':
            self.driver.switch_to.default_content()
        else:
            self.driver.switch_to.frame(frame)
    
    def zoom(self,zoom):
        self.driver.execute_script(f"document.body.style.zoom='{zoom}'")

    def screem(self, info=''):
        self.zoom('60%')
        time=str(datetime.timestamp(datetime.now())).replace('.','_')
        self.driver.save_screenshot(f'screen\\{info}_{time}.png')
        self.zoom('100%')

    def close(self):
        self.driver.close()
