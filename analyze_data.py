
import pandas as pd
import time
from datetime import datetime
from pandas import Series
from matplotlib import pyplot
from matplotlib.pyplot import figure
import numpy as np

def draw_power_graphics(power,sp=None,before=None,after=None,band=100):
    """
    Draw different graphics for the power (the number of graphics depend of how many
    data are included in the power and the value of band)
    power  : dataframe with the values of the power 
    sp     : array of [array of x, array of y] array 3D with the points we 
            want highlight in the graphics with different colors
    before : we want to consider only the value before a certain date
    after  : we want to consider only the value after a certain date
    band   : how many values of power we want draw in each graphics
    --------------------------------------------------------
    Note: this method use the 'time' and 'value' columns and the date must be passed
        in this format -> %Y-%m-%d %H:%M:%S
    """
    i    = 0
    tmp_power = power.copy()
    if before!=None:
        tmp_power = tmp_power[tmp_power['time']<=before]
    if after!=None:
        tmp_power = tmp_power[tmp_power['time']>=after]
    serie = Series.from_array(tmp_power['value'])
    while(i*band<len(serie)):
        pyplot.figure(figsize=(20, 5))
        pyplot.plot(serie[i*band:(i+1)*band],'ro')
        v = [i*band, (i+1)*band, 0, 1200]
        pyplot.axis(v)
        v = [serie.index[0], serie.index[len(serie)-1], 0, 1200]#xmin,xmax,ymin,ymax
        if sp != None:
            j = 0
            while j<len(sp):
                pyplot.scatter(sp[j][0],sp[j][1],marker=(0, 3))
                j += 1
        pyplot.show()
        i += 1
    
def draw_around_event(power,events,borders,eventName,maxY=1200):
    """
    Draw different graphics for each event saved in events dataframe. 
    In each graphics is drawn the levels of power around the event
    power     : dataframe with the values of the power 
    events    : dataframe with the events (and respective datetime)
    borders   : [min,MAX] how many seconds before and after the events we want to
                consider in the graphics
    eventName : name of the event we want consider for the graphics
    maxY      : the max Y value of power we in the Cartesian axis
    --------------------------------------------------------
    Note: this method use the 'time' and 'value' columns and the date must be passed
        in this format -> %Y-%m-%d %H:%M:%S
    """
    event_consider = events[events['eventName']==eventName].reset_index(drop=True)
    print("number of", eventName ,"in groudtruth=",len(event_consider))
    i     = 0
    while(i<len(event_consider)):
        date   = time.mktime(datetime.strptime(event_consider['time'][i], "%Y-%m-%d %H:%M:%S").timetuple())
        start  = str(datetime.fromtimestamp(date-borders[0]))
        end    = str(datetime.fromtimestamp(date+borders[1]))
        print(date,start,end)
        i += 1
        serie = Series.from_array(power[(power['time']>=start)&(power['time']<=end)]['value'])
        if len(serie)>0:
            v = [serie.index[0], serie.index[len(serie)-1], 0, maxY]#xmin,xmax,ymin,ymax
            pyplot.figure(figsize=(20, 5))
            pyplot.plot(serie,'ro')
            pyplot.axis(v)
            pyplot.show()
        else:
            print("No data of power for this event")
    
def average_energy(power,events,borders,eventName):
    """
    Return, and print, the average of energy used during the event which we are
    interesting (example: eventName="coffee")
    power     : dataframe with the values of the power 
    events    : dataframe with the events (and respective datetime)
    borders   : [min,MAX] how many seconds before and after the events we want to
                consider in the graphics
    eventName : name of the event we want consider for the graphics
    --------------------------------------------------------
    Note: this method use the 'time' and 'value' columns and the date must be passed
        in this format -> %Y-%m-%d %H:%M:%S
    """
    event_consider = events[events['eventName']==eventName].reset_index(drop=True)
    average   = 0
    i          = 0
    count      = 0
    minValue   = 10000
    maxValue   = 0
    minAverage = 10000
    maxAverage = 0  
    while(i<len(event_consider)):
        date   = time.mktime(datetime.strptime(event_consider['time'][i], "%Y-%m-%d %H:%M:%S").timetuple())
        start  = str(datetime.fromtimestamp(date+borders[0]))
        end    = str(datetime.fromtimestamp(date+borders[1]))
        values = power[(power['time']>=start)&(power['time']<=end)]['value']
        sum_values = sum(values)
        tot_values = len(values)
        if tot_values>0:
            if values.max() > maxValue:
                maxValue = values.max()
            if values.min() < minValue:
                minValue = values.min()
            if sum_values/tot_values > maxAverage:
                maxAverage = sum_values/tot_values
            if sum_values/tot_values < minAverage:
                minAverage = sum_values/tot_values
            average = average + sum_values/tot_values
            count += 1
        i += 1
    if count>0:
        average = average / count
        print("number of", eventName ,"in groudtruth and power=",count)
        print("minValue=",minValue,"maxValue=",maxValue)
        print("minAverage=",minAverage,"maxAverage=",maxAverage)
        print("Final Av=",average)
        return average
    else:
        print("Not values found in the range")

def get_special_point(power,events,borders,eventName,numericValue):
    """
    Return, and print, the average of energy used during the event which we are
    interesting (example: eventName="coffee")
    power        : dataframe with the values of the power
    events       : dataframe with the events (and respective datetime)
    borders      : [min,MAX] how many seconds before and after the events we want to
                  consider in the graphics
    eventName    : name of the event we want consider for the graphics
    numericValue : value we want to give in the Y axis for each event
    --------------------------------------------------------
    Note: this method use the 'time' and 'value' columns and the date must be passed
        in this format -> %Y-%m-%d %H:%M:%S
    """
    event_consider = events[events['eventName']==eventName].reset_index(drop=True)
    #around turn_on
    i    = 0  
    count = 0
    event_index = []
    while(i<len(event_consider)):
        date   = time.mktime(datetime.strptime(event_consider['time'][i], "%Y-%m-%d %H:%M:%S").timetuple())
        start  = str(datetime.fromtimestamp(date-borders[0]))
        end    = str(datetime.fromtimestamp(date+borders[1]))
        serie = Series.from_array(power[(power['time']>=start)&(power['time']<=end)]['value'])
        if len(serie)>0:
            event_index.append(serie.index[int(len(serie)/2)])
            count += 1
        i += 1
    print("number of", eventName ,"in groudtruth and power=",count)
    return event_index,[numericValue]*len(event_index)

def return_array_of_power(power,start_date,end_date):
    values = power[(power['time']>start_date)&(power['time']<end_date)]['value']
    s="["
    for i in values:
        s += (str(i)+",")
    return s
''' Exaple 1
power = pd.read_csv("power.csv")
groundtruth = pd.read_csv("groudtruth.csv")
sp = get_special_point(groundtruth,[10,10],"coffee",1000)
print(sp)
draw_power_graphics(power,sp,band=2500)
average_energy(power,groundtruth,[10,10],"on")
draw_around_event(power,groundtruth,[10,10],"coffee")
'''

''' Exaple 2
power = pd.read_csv("power.csv")
groundtruth = pd.read_csv("groudtruth.csv")
sp = get_special_point(groundtruth,[10,10],"coffee",1000)
sp_2 = get_special_point(groundtruth,[10,10],"on",1000)
draw_power_graphics(power,[sp,sp_2],band=2500)
'''

power = pd.read_csv("power.csv")
groundtruth = pd.read_csv("groudtruth.csv")
sp1 = get_special_point(power,groundtruth,[7,7],"coffee",1000)
sp2 = get_special_point(power,groundtruth,[7,7],"on",1000)
print("-"*20,"ENERGY FOR ON","-"*20)
average_energy(power,groundtruth,[-7,7],"on")
print("-"*20,"ENERGY FOR COFFEE","-"*20)
average_energy(power,groundtruth,[-7,7],"coffee")
print("-"*20,"ENERGY AFTER COFFEE","-"*20)
average_energy(power,groundtruth,[7,21],"coffee")
print("-"*20,"ENERGY AFTER ON","-"*20)
average_energy(power,groundtruth,[7,21],"on")
print("-"*20,"ENERGY BEFORE COFFEE","-"*20)
average_energy(power,groundtruth,[-21,-7],"coffee")
print("-"*20,"ENERGY BEFORE ON","-"*20)
average_energy(power,groundtruth,[-21,-7],"on")

draw_power_graphics(power,[sp1,sp2],band=2500)
#draw_around_event(power,groundtruth,[10,10],"coffee")