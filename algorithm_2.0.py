
#import libraries
from format_csv import *
from analyze_data import *

power = pd.read_csv("power_2.csv")
groundtruth = pd.read_csv("groudtruth_2.csv")

sp1 = get_special_point(power,groundtruth,[7,7],"coffee",1000)
sp2 = get_special_point(power,groundtruth,[7,7],"on",1000)
print("-"*20,"ENERGY FOR ON","-"*20)
average_energy(power,groundtruth,[-5,9],"on")
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

draw_power_graphics(power,[sp1,sp2],band=12000)