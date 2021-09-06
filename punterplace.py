from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from libraries.web_base import Webdriver
from function import salve_csv
from time import sleep
from datetime import datetime


class Punter:
    URL='https://m.punterplace.com/login?next=/trade'
    LOGIN = (By.XPATH,'//div[contains(@class, "row-4-email-container")]//input ')
    LOGIN_SENHA = (By.XPATH,'//div[contains(@class, "row-5-password-container")]//input ')
    LOGIN_BUTTON = (By.XPATH,'//*[@id="app"]/div[3]/div/div[5]/div[2]/button/div')

    ABAS = (By.XPATH,'//div[contains(@class, "market-option")]')
    LIGAS = (By.XPATH,'//div[contains(@class, "MarketContainer")]//div[contains(@class, "competition-head")]')
    JOGOS = (By.XPATH,'//div[contains(@class, "unselected-event-header")]')

    BUSCA = (By.XPATH,'//div[@class="header-search-icon"]')
    INPUT_BUSCA = (By.XPATH,'//input[@class="search-text-field"]')
    RESULT = (By.XPATH,'//*[@class="search-results"]//div[contains(@class, "search-result-event ir")]')

    ASIAN_TOTAL = (By.XPATH,'//div[contains(text(), "Asian Total")]')
    ASIAN_MAIS = (By.XPATH,'(//div[contains(@class, "ahou narrow")])[1]//*[contains(text(), "Mais")]')
    ASIAN_TOTAL_BODY = (By.XPATH,'(//div[contains(@class, "ahou narrow")] )[1]')
    ASIAN_TOTAL_GOLS = (By.XPATH,'(//div[contains(@class, "ahou narrow")] )[1]//div[contains(@class, "line-with-handicap")]')
    BUTTON_APOSTA =  (By.XPATH,'//button[contains(text(), "Apostar")]')
    PLACAR =  (By.XPATH,'//div[@class="scores-container"]')


    def __init__(self, headless=False, apostar=True):
        self.driver = Webdriver(profiles=False, headless=headless)
        self.APOSTAR = apostar

    def start(self):
        self.driver.start()
        self.driver.open_page(self.URL)
    
    def login(self, login, senha):
        self.driver.fill(self.LOGIN, login)
        self.driver.fill(self.LOGIN_SENHA, senha)
        self.driver.click(self.LOGIN_BUTTON)
        if self.driver.exist(self.BUSCA):
            return True
        else: 
            self.driver.screenshot(f'screen/ERRO LOGIN PUNTER.png')    
            return False

    def home(self):
        self.driver.open_page('https://m.punterplace.com/trade')
 
    def busca(self, time):
        self.driver.click(self.BUSCA) 
        sleep(1)
        self.driver.fill(self.INPUT_BUSCA, time)
        self.driver.send_key(Keys.ENTER, self.INPUT_BUSCA)
        sleep(1)

        if self.driver.exist(self.RESULT):
            result=self.driver.find_elements(self.RESULT)
     
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
            
            try:
                placar=self.driver.find_element(self.PLACAR).text
                
                if ((int(placar[0])+int(placar[-1])) - (gol_taxa-0.5)) * -1>0.25:
                    salve_csv('Gols da partida diferentes do sinal')
                    self.driver.screenshot(f'screen/{times} - {gol_taxa}.png')
                    return False

                over=self.driver.find_elements(self.ASIAN_TOTAL_BODY)

            except: 
                salve_csv('Erro na verificação do placar')
                return False

            if len(over)==0:
                self.driver.click(self.ASIAN_TOTAL)
                sleep(1)
                over=self.driver.find_elements(self.ASIAN_TOTAL_BODY)
            
            if len(over)>0:  
                mais=self.driver.find_elements(self.ASIAN_MAIS)
                if len(mais)>0:
                    self.driver.move_element(mais[0])
                    self.driver.click(mais[0]) 
                return True
            else:
                self.driver.screenshot(f'screen/{times} - {gol_taxa}.png')
                salve_csv('Não achado body Asian Total')
                return False
        except:
            self.driver.screenshot(f'screen/Erro_check_asian{times} - {gol_taxa}.png')
            salve_csv('Não achado body Asian Total')
            return False
        
    def select_aposta(self, gol_taxa, times):
        if not self.check_asian(gol_taxa, times):
            self.driver.screenshot(f'screen/{times} - {gol_taxa}.png')
            return False

        for c in range(1,10):#buscar por jogo ao vivo
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

        self.driver.screenshot(f'screen/{times} - {gol_taxa}.png')
        salve_csv('Taxa não achada')
        return False

    def aba(self, aba):
        self.driver.open_page('https://m.punterplace.com/trade')
        sleep(3)
        abas=self.driver.find_elements(self.ABAS)
        for c in abas:
            if aba == c.text:
                self.driver.click(c)
                return True
        return False

    def ligas(self, liga):
        ligas=self.driver.find_elements(self.LIGAS)
        for c in ligas:
            if liga in c.text:
                self.driver.click(c)
                return True
        return False     

    def jogos(self, jogo):
        jogos=self.driver.find_elements(self.JOGOS)
        for c in jogos:
            if jogo in c.text:
                self.driver.click(c)
                return True
        return False     

    def apostar(self):

        if self.driver.exist(self.BUTTON_APOSTA, wait=3):
            if self.driver.find_element(self.BUTTON_APOSTA).is_enabled():
                if self.APOSTAR:
                    self.driver.click(self.BUTTON_APOSTA)
                else:
                    self.driver.screenshot(f'screen/simulacao_aposta_{datetime.now().timestamp()}.png')
                return True
            else:
                salve_csv('Botão de aposta indisponível')
                return False

    def atualizar(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()
 

