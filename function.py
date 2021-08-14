import winsound
import shutil
import csv
import os

def remove_profile():
    mydir= 'profile'
    try:
        shutil.rmtree(mydir)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

def check_profile():
    return os.path.isdir("profile")

def analise_sinal(sinal):

    if 'over top' not in sinal:
        return False

    sinal_=sinal.split('\n')
    sinal_=sinal_[sinal_.index('ALERTA [ over top ]'):]
    dic={}

    for c in range(len(sinal_)):
        if 'Placar' in sinal_[c]:
            index=c

    dic['time']=(sinal_[2].split(' v ')[0]).split('/')[1][1:]
    dic['time2']=(sinal_[2].split(' v ')[1]).split('/')[0]


    try:
       dic['taxa']=int(sinal_[index][8])+int(sinal_[index][12])+0.5
    except:
        print('Erro na captura do Sinal!')

    dic['hora']=sinal_[3]

    return dic

def salve_csv(ask):
    file=open('historico.txt', mode='a')
    file.write(f'\n{ask}:')
    file.close()    

def consult_csv():
    configs={}
    with open('Configs.txt', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n')
        for row in spamreader:
            dic=row[0].split(':')
            configs[dic[0]]=dic[1]
    return configs

def beep():
    frequency = 1000  # Set Frequency To 2500 Hertz
    duration = 1000  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

def trys(func1, func2):
    try:
        func1()
    except:
        func2()