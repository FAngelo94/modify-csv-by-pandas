
#import libraries
from format_csv import *
from analyze_data import *

power = pd.read_csv("power.csv")
groundtruth = pd.read_csv("groudtruth.csv")
sp = get_special_point(power,groundtruth,[10,10],"coffee",1000)
sp_2 = get_special_point(power,groundtruth,[10,10],"on",1000)
draw_power_graphics(power,[sp,sp_2],band=2500)
#draw_around_event(power,groundtruth,[10,10],"coffee")
average_energy(power,groundtruth,[7,8],"coffee")
average_energy(power,groundtruth,[10,10],"on")
average_energy(power,groundtruth,[-10,20],"on")