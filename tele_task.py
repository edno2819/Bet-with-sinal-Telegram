from libraries.telegram import Telegram
import time


class TelegramTask:
    def __init__(self, profiles=True, headless=True):
        self.tele = Telegram(profiles, headless=headless)
    
    def open_telegram(self):
        self.tele.open_telegram()
    
    def open_canal_sinal(self, canal):
        self.tele.open_canal_sinal(canal)
        self.tele.scroll_dowm()
        return True
    
    def refesh_msgs(self):
        elens = self.tele.get_menssagens_elem()
        if not elens:
            return 
        index = len(elens)
        try:
            elens[index-3].click()
            elens[-1].click()
        except:
            pass

    def get_sinais(self):
        self.refesh_msgs()
        return self.tele.get_menssagens()

