import webdriver_Per
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


class Telegram():
    __URL='https://web.telegram.org/z/'
    __BARRA_DE_BUSCA= (By.XPATH, '//*[@id="telegram-search-input"]')
    __MSG= (By.XPATH,'//*[@class="text-content "]')
    __FIST_ITEM_CHAT_SEARCH = (By.XPATH,'//*[@class="ListItem chat-item-clickable search-result no-selection"]')
    __DESCER_MSG = (By.XPATH,'//*[@class="ScrollDownButton-inner"]')#//*[@class="icon-arrow-down"]
    EXIST_SCROLL_DOWM=(By.XPATH,'//*[@class="unread-count"]')
    

    def __init__(self, profiles=False, headless=False):
        self.driver = webdriver_Per.Webdriver(profiles, headless)
    
    def open_telegram(self):
        self.driver.start()
        self.driver.open_page(self.__URL)
    
    def open_canal_sinal(self, nome):
        try:
            self.driver.click(self.__BARRA_DE_BUSCA)
            self.driver.fill(self.__BARRA_DE_BUSCA, nome)
            time.sleep(5)
            self.driver.click(self.__FIST_ITEM_CHAT_SEARCH)
            return True
        except:
            self.driver.screem(f'ERRO OPEN CANAL')
            return False

    def scroll_dowm(self):
        try:
            if self.driver.exist(self.EXIST_SCROLL_DOWM):
                self.driver.click(self.__DESCER_MSG)
            return True
        except:
            self.driver.screem(f'ERRO SCROLL DOWM')
            return False

    def check_conected(self):
        return self.driver.exist(self.__BARRA_DE_BUSCA)

    def open_chat(self, number):
        self.driver.click(self.__BARRA_DE_BUSCA)
        self.driver.fill(self.__BARRA_DE_BUSCA, number)
        time.sleep(2)
        self.driver.send_key(Keys.ENTER,self.__BARRA_DE_BUSCA)

    def send_menssege(self,text):
        self.driver.send_key(text)
        self.driver.send_key(Keys.ENTER)
    
    def get_menssagem(self, index=-1):
        elem=self.driver.find_elements(self.__MSG)
        if len(elem)==0:
            return False
            
        msg=elem[index].text
        return msg

    def get_menssagems(self):
        
        elem=self.driver.find_elements(self.__MSG)
        
        if len(elem)==0:
            print('N capturou nem uma menssagem')
            return False

        self.driver.move_element(elem[-1])
        elem=self.driver.find_elements(self.__MSG)

        msg=list()
        p= len(elem) if len(elem)<15 else 15
        for index in range(len(elem)-p,len(elem)):
            msg.append(elem[index].text)

        self.driver.move_element(elem[-1])
        return msg

    def atualizar(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()


