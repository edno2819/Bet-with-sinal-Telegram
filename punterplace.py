from webdriver_Per import Webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from function import salve_csv
import function as func

class Punter():
    __URL='https://m.punterplace.com/login?next=/trade'
    __LOGIN =(By.XPATH,'//div[contains(@class, "TextField__Container")]//input')
    __LOGIN_BUTTON =(By.XPATH,'//*[@id="app"]/div[3]/div/div[5]/div[2]/button/div')

    __ABAS = (By.XPATH,'//div[contains(@class, "market-option")]')
    __LIGAS = (By.XPATH,'//div[contains(@class, "MarketContainer")]//div[contains(@class, "competition-head")]')
    __JOGOS = (By.XPATH,'//div[contains(@class, "unselected-event-header")]')

    __BUSCA = (By.XPATH,'//div[@class="header-search-icon"]')
    __INPUT_BUSCA = (By.XPATH,'//input[@class="search-text-field"]')
    #__RESULT = (By.XPATH,'//*[@class="search-results"]//div[contains(@class, "search-result")]')
    __RESULT = (By.XPATH,'//*[@class="search-results"]//div[contains(@class, "search-result-event ir")]')

    __ASIAN_TOTAL = (By.XPATH,'//div[contains(text(), "Asian Total")]')
    __ASIAN_MAIS = (By.XPATH,'(//div[contains(@class, "ahou narrow")])[1]//*[contains(text(), "Mais")]')
    __ASIAN_TOTAL_BODY = (By.XPATH,'//div[contains(@class, "ahou narrow")]')
    __ASIAN_TOTAL_GOLS = (By.XPATH,'//div[contains(@class, "ahou narrow")]//div[contains(@class, "line-with-handicap")]')
    #(//div[contains(@class, "ahou narrow")])[1]//div[contains(@class, "line-with-handicap")][2]//a[1] 
    __BUTTON_APOSTA =  (By.XPATH,'//button[contains(text(), "Apostar")]')
    __PLACAR =  (By.XPATH,'//div[@class="scores-container"]')


    def __init__(self, headless=False):
        self.driver = Webdriver(profiles=False, headless=headless)

    def open(self):
        self.driver.start()
        self.driver.open_page(self.__URL)
    
    def login(self, login, senha):
        try:
            input_login, input_senha = self.driver.find_elements(self.__LOGIN)
            self.driver.fill(input_login, login)
            self.driver.fill(input_senha, senha)
            self.driver.click(self.__LOGIN_BUTTON)
            if self.driver.exist(self.__BUSCA):
                return True
            else: 
                self.driver.screem(f'ERRO LOGIN PUNTER')    
                return False
        except:
            self.driver.screem(f'ERRO LOGIN PUNTER')    
            return False

    def home(self):
        self.driver.open_page('https://m.punterplace.com/trade')
 
    def busca(self, time):
        self.driver.click(self.__BUSCA) 
        sleep(1)
        self.driver.fill(self.__INPUT_BUSCA, time)
        sleep(1)

        if self.driver.exist(self.__RESULT):
            result=self.driver.find_elements(self.__RESULT)
     
            if len(result)>0:
                for re in result:
                    if 'women' not in re.text.lower():
                        self.driver.click(re)
                        return True
                return False
                
        else: return False

    def check_asian(self, gol_taxa, times):
        sleep(1)
            
        try:
            placar=self.driver.find_element(self.__PLACAR).text
            
            if ((int(placar[0])+int(placar[-1])) - (gol_taxa-0.5)) * -1>0.25:
                salve_csv('Gols da partida diferentes do sinal')
                self.driver.screem(f'{times} - {gol_taxa}')
                return False

            over=self.driver.find_elements(self.__ASIAN_TOTAL_BODY)

        except: 
            salve_csv('Erro na verificação do placar')
            return False

        if len(over)==0:
            self.driver.click(self.__ASIAN_TOTAL)
            sleep(1)
            over=self.driver.find_elements(self.__ASIAN_TOTAL_BODY)
        
        if len(over)>0:  
            mais=self.driver.find_elements(self.__ASIAN_MAIS)
            if len(mais)>0:
                self.driver.move_element(mais[0])
                self.driver.click(mais[0]) 
            return True
        else:
            self.driver.screem(f'{times} - {gol_taxa}')
            salve_csv('Não achado body Asian Total')
            return False
        
    def select_aposta(self, gol_taxa, times):
        if not self.check_asian(gol_taxa, times):
            self.driver.screem(f'{times} - {gol_taxa}')
            return False

        for c in range(1,10):
            xpath=f'(//div[contains(@class, "ahou narrow")])[1]//div[contains(@class, "line-with-handicap")][{c}]'
            row_asian=(By.XPATH, xpath)
            try:
                placar=self.driver.find_element(row_asian)
                if float(placar.text.split('\n')[0]) == gol_taxa:
                    self.driver.move_element(placar)
                    cell_aposta=(By.XPATH, xpath +'//a[1]')
                    self.driver.click(self.driver.find_element(cell_aposta))
                    return True
            except:
                break

        self.driver.screem(f'{times} - {gol_taxa}')
        salve_csv('Taxa não achada')
        return False

    def aba(self, aba):
        self.driver.open_page('https://m.punterplace.com/trade')
        sleep(3)
        abas=self.driver.find_elements(self.__ABAS)
        for c in abas:
            if aba == c.text:
                self.driver.click(c)
                return True
        return False

    def ligas(self, liga):
        ligas=self.driver.find_elements(self.__LIGAS)
        for c in ligas:
            if liga in c.text:
                self.driver.click(c)
                return True
        return False     

    def jogos(self, jogo):
        jogos=self.driver.find_elements(self.__JOGOS)
        for c in jogos:
            if jogo in c.text:
                self.driver.click(c)
                return True
        return False     

    def apostar(self, gol_taxa, times):

        if self.driver.exist(self.__BUTTON_APOSTA):
            try:
                self.driver.click(self.__BUTTON_APOSTA)
                return True
            except:
                self.driver.screem(f'{times} - {gol_taxa}')
                salve_csv('Botão de aposta não disponível')
                return False
        else:
            self.driver.screem(f'{times} - {gol_taxa}')
            salve_csv('Botão de aposta não encontrado')
            return False

    def atualizar(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()
 

