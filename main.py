from telegram import Telegram
from punterplace import Punter
from time import gmtime, strftime, sleep
import sys
from time import gmtime, strftime
import function as func
from datetime import datetime



class Main():

    def __init__(self):
        self.hedless=True#botar como False
        self.x=int(datetime.now().strftime('%d')) + 30*int(datetime.now().strftime('%m'))
        self.login=0
        self.senha=0
        self.fist=False
    
    def configs(self):
        self.new_login=False
        
        configs=func.consult_csv()
        
        self.login=configs['Login']
        self.senha=configs['Senha']
        self.hedless=bool(int(configs['Visivel']))
        #self.canal=configs['Canal']
        self.hedless = True if self.hedless==False else False
        self.tele=Telegram(profiles=True, headless=True)
        self.punter=Punter(headless=self.hedless)

    def start(self): 
        self.tele.open_telegram()
        self.punter.open()
        sleep(2)
        if not self.tele.open_canal_sinal('InPlayScanner_BOT'):
            func.salve_csv(f'\nErro no Open Canal telegram!')
            return False

        elif not self.tele.scroll_dowm():
            func.salve_csv(f'\nErro no Open scroll dowm telegram!')
            return False

        elif not self.punter.login(self.login,self.senha):
            func.salve_csv(f'\nErro no Login Punter!')
            return False

        else: return True

    def conect_new_telegram(self):
        self.tele=Telegram(profiles=True, headless=False)
        self.tele.open_telegram()
        input('Esperando conexão! Após conectar, aperte ENTER!')
        self.close()

    def get_telegram_sinal(self):
        sinal=self.tele.get_menssagems()

        try:
            if not self.fist:
                self.fist=sinal[-1]

            sinal=sinal[(sinal.index(self.fist)):][1:]
        except:
            pass

        return sinal

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
        sleep(1) 

        if self.punter.select_aposta(sinal['taxa'], f"{sinal['time']}x{sinal['time2']}") or self.punter.select_aposta(sinal['taxa'], f"{sinal['time']}x{sinal['time2']}"):
            if self.punter.apostar(sinal['taxa'], f"{sinal['time']}x{sinal['time2']}"):
                func.salve_csv('Aposta feita!')
                self.punter.home()
                return

        func.salve_csv('Erro na aposta!')
        func.beep()
        self.punter.home()    

    def close(self):
        self.tele.close()
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

if not func.check_profile():
    bot.conect_new_telegram()

sinais=[]


def execute():
    tent=0
    bot.restart()
    while True:

        if tent>=300:
            tent=0
            bot.restart()
            print('Restartou')

        sleep(3)
        sinais_get=bot.get_telegram_sinal()

        for sinal in sinais_get:
            if sinal:
                sinal=func.analise_sinal(sinal)

                if sinal not in sinais and sinal!=False:
                    hora=strftime("%d-%m %H:%M:%S", gmtime())

                    func.salve_csv(f'\n{hora} -  Sinal recebido {sinal}')
                    
                    bot.make_apost(sinal)
                
                    sinais.append(sinal)

        sleep(2)
        tent+=1


execute()

