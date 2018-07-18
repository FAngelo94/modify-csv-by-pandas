
import pandas as pd
import time
from datetime import datetime

def remove_NaN(data):
    """
    Remove the rows that contain NaN and null in the 'objectId' column
    data: dataframe we want to modify
    """
    data = data[pd.notnull(data['objectId'])]
    data = data[data['objectId']!="null"]
    return data

def col_time(data):
    """
    Read the column timestamp and create a new column with the date using format
    "%Y-%I-%d %H:%M:%S"
    data: dataframe we want to modify
    """
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
    """
    Substitute the name of events in the "eventName" column with numeric values
    data: dataframe we want to modify
    """
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

def create_new_csv(data,name):
    """
    Save a dataframe in a new file csv
    data: dataframe we want to modify
    name: name of the new csv file
    """
    #Crea un nuovo file csv
    #data: il dataframe che si vuole modificare
    #name: nome del nuovo file
    data.to_csv(name+".csv")
    
def modify_hour(data,hour,ms):
    """
    Function to add hour to the date of the dataframe 
    data: dataframe we want to modify
    hour: how many hours we want sum to the date
    ms  : number of charapter present in the table, after the seconds
        (example: for "2018-07-02 11:30:30.05" ms=3 in order to remove ".05")
    """
    #data: il dataframe che si vuole modificare
    #ore: quante ore si vogliono sommare alla data 
    #ms: numero di caratteri, nella data presente in tabella, presenti dopo i secondi
    #(esempio: per "2018-07-02 11:30:30.05" ms=3 per eliminare ".05")
    i = 0
    array = []
    while(i<len(data['time'])):
        d = str(data['time'][i])
        d = d[0:len(d)-ms]
        time.mktime(datetime.strptime(d, "%Y-%m-%d %H:%M:%S").timetuple())
        d=datetime.fromtimestamp(time.mktime(datetime.strptime(d, "%Y-%m-%d %H:%M:%S").timetuple())+(60*60*hour))
        array.append(d)
        i += 1
    data['time']=array
    return data

#Codice di esempio che usa i metodi sopra (senza creare nuovi file):
#cOSTANTI
'''
FILE_MONGO = "mongo.csv"

mongo = pd.read_csv(FILE_MONGO)
mongo = remove_NaN(mongo)
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
'''