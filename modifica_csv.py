
import pandas as pd
import time
from datetime import datetime

def rimuovi_NaN(data):
    #Elimina le righe contenenti NaN e null nella colonna 'objectId'
    #data: il dataframe che si vuole modificare
    data = data[pd.notnull(data['objectId'])]
    data = data[data['objectId']!="null"]
    return data

def col_time(data):
    #Legge la colonna "timestamp" e una nuova colonna con la data in formato
    #"%Y-%I-%d %H:%M:%S"
    #data: il dataframe che si vuole modificare
    timestamp = data['timestamp']
    datacorrect = []
    i = 0
    while(i<len(timestamp)):
        d = str(datetime.fromtimestamp(timestamp[i]/1e3))
        datacorrect.append(d[0:len(d)-7])
        i += 1
    data['time'] = datacorrect
    return data

def col_eventNumber(data):
    #Sostituisce i nomi degli eventi sulla colonna "eventName" con dei valori numerici
    #data: il dataframe che si vuole modificare
    events = data['eventName']
    eventNumber = []
    i=0
    while(i<len(events)):
        if(events[i]=="heating"):
            eventNumber.append(700)
        if(events[i]=="coffee"):
            eventNumber.append(1500)
        if(events[i]=="standby"):
            eventNumber.append(200)
        if(events[i]=="off"):
            eventNumber.append(0)
        if(events[i]=="on"):
            eventNumber.append(500)
        i += 1
    data['eventNumber'] = eventNumber
    return data

def crea_csv_nuovo(data,name):
    #Crea un nuovo file csv
    #data: il dataframe che si vuole modificare
    #name: nome del nuovo file
    data.to_csv(name+".csv")
    
def modifica_ore(data,ore,ms):
    #data: il dataframe che si vuole modificare
    #ore: quante ore si vogliono sommare alla data 
    #ms: numero di caratteri, nella data presente in tabella, presenti dopo i secondi
    #(esempio: per "2018-07-02 11:30:30.05" ms=3 per eliminare ".05")
    d = str(data['time'][0])
    d = d[0:len(d)-ms]
    time.mktime(datetime.strptime(d, "%Y-%I-%d %H:%M:%S").timetuple())
    d=datetime.fromtimestamp(time.mktime(datetime.strptime(d, "%Y-%I-%d %H:%M:%S").timetuple())+(60*60*2))
    data['time']=d
    return data

#Codice di esempio che usa i metodi sopra (senza creare nuovi file):
#cOSTANTI
FILE_MONGO = "mongo.csv"

mongo = pd.read_csv(FILE_MONGO)
mongo = rimuovi_NaN(mongo)
print(mongo.head())
nespresso   = mongo[mongo['objectId']=="nespresso_jolmilano"].reset_index(drop=True)
print(nespresso.head(3))
groundtruth = mongo[mongo['objectId']=="nespresso_jolmilano_groundtruth"].reset_index(drop=True)
print(groundtruth.head(3))

nespresso = col_time(nespresso)
nespresso = col_eventNumber(nespresso)
nespresso.head()

groundtruth = col_time(groundtruth)
groundtruth = col_eventNumber(groundtruth)
groundtruth.head()