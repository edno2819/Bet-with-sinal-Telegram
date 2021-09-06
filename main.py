from libraries.tele_task import TelegramTask
from libraries.punterplace import Punter
from time import sleep
from datetime import datetime
import function as func
import sys



CONFIGS = func.consult_csv()
CONFIGS['Apostar'] = bool(int(CONFIGS['Apostar']))
CONFIGS['Visivel'] = bool(int(CONFIGS['Visivel']))
SINAIS = []

class Main():

    def __init__(self):
        self.x=int(datetime.now().strftime('%d')) + 30*int(datetime.now().strftime('%m'))
        self.hedless=True
        self.fist=False
        self.login=0
        self.senha=0
    
    def configs(self):
        self.new_login=False
                
        self.login = CONFIGS['Login']
        self.senha = CONFIGS['Senha']
        self.hedless = False if CONFIGS['Visivel'] else True
        self.tele = TelegramTask(profiles=True)
        self.punter = Punter(headless=self.hedless, apostar=CONFIGS['Apostar'])

    def start(self): 
        self.tele.open_telegram()
        self.punter.start()

        if not self.tele.open_canal_sinal('InPlayScanner_BOT'):
            func.salve_csv(f'\nErro no Open Canal telegram!')
            return False

        elif not self.punter.login(self.login,self.senha):
            func.salve_csv(f'\nErro no Login Punter!')
            return False
            
        return True

    def conect_new_telegram(self):
        self.tele_visi=TelegramTask(profiles=True, headless= False)
        self.tele_visi.open_telegram()
        input('Esperando conexão! Após conectar, Reinicie o programa!')
        self.tele_visi.tele.close()

    def get_telegram_sinais(self):
        sinais = self.tele.get_sinais()

        if not self.fist:
            self.fist = sinais[-1]

        sinais = sinais[(sinais.index(self.fist)):][1:]

        if sinais!=[]:
            self.fist = sinais[-1]
        
        return sinais

    def make_apost(self, sinal):
        self.punter.aba('Ao vivo')
        sleep(1)

        if self.punter.busca(sinal['time'])==False:
            self.punter.aba('Ao vivo')
            sleep(1)
            if self.punter.busca(sinal['time2'])==False:
                func.salve_csv('Jogo não encontrado!')
                self.punter.home()
                func.beep()
                return
                
        if self.punter.select_aposta(sinal['taxa'], f"{sinal['time']}x{sinal['time2']}") or self.punter.select_aposta(sinal['taxa'], f"{sinal['time']}x{sinal['time2']}"):
            if self.punter.apostar():
                func.salve_csv('Aposta feita!')
                self.punter.home()
                return

        func.salve_csv('Erro na aposta!')
        func.beep()
        self.punter.home()    

    def close(self):
        self.tele.tele.close()
        self.punter.close()

    def restart(self, x=3):
        for c in range(0,x):
            try:
                self.close()
            except: pass
            if self.start():
                return True
        return False

bot = Main()
bot.configs()

def close():
    try:
        bot.close()
    except:
        bot.tele_visi.tele.close()
    sys.exit()

def execute():
    if not func.check_profile():
        bot.conect_new_telegram()
        
    print('Iniciando Bot')
    tent=0

    bot.restart()
    while True:

        if tent>=300:
            tent = 0
            bot.restart()
            print('\nRestartou')

        sleep(3)
        #try:
        sinais_get = bot.get_telegram_sinais()

        for sinal in sinais_get:
            if sinal:
                sinal = func.analise_sinal(sinal)

                if sinal not in SINAIS and sinal!=False:
                    aviso = f'\n{datetime.now().strftime("%H:%M:%S %d/%m/%Y")} -  Sinal recebido {sinal}'
                    func.salve_csv(aviso)
                    print(aviso)
                    
                    bot.make_apost(sinal)
                
                    SINAIS.append(sinal)
        # except:
        #     func.salve_csv(traceback.format_exc())
        #     bot.restart()

  


        tent+=1
    


