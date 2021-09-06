import PySimpleGUI as sg
from main import execute, close
import threading
import sys


sg.change_look_and_feel('DarkAmber')
bot = threading.Thread(target=execute)
bot_close = threading.Thread(target=close)

layout=[
    [sg.Text('Punter Place Bot', size=(100, 1), justification='center', font=("Helvetica", 20), relief=sg.RELIEF_RIDGE)],
    [sg.Text('', size=(7,0))], 
    [sg.Button('Iniciar', border_width=5, size=(100, 1), key=("run"))],
    [sg.Output(key='-OUT-', size=(80, 40))]]


window = sg.Window('Punter Place Bot', layout, size=(450, 250), icon='images.ico')

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancelar'):
        bot_close.start()
        break
    if event == 'run':
        bot.start()



window.close()
sys.exit()

