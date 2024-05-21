import numpy as np
import math

inpdat = open("inputs.txt",'r')  # open reading file
line = inpdat.readline() # get the line
row = line.split(":")      # get row as an array
Rearth = float(row[1])    
line = inpdat.readline() # get the next line
row = line.split(":") 
Gconst = float(row[1])    
line = inpdat.readline() # get the next line
row = line.split(":")     
Mearth = float(row[1]) 
inpdat.close()     # close the file after done reading

Horbit = float(input("Enter orbit height in km: ")) # input from user

# Calculations
R = (Rearth + Horbit)*1000.0    # in meters
v = np.sqrt((Gconst*Mearth)/R)   # in m/s
T = (2*np.pi*math.pow(R,1.5))/(np.sqrt(Gconst*Mearth))  # in seconds
Hang = np.arccos((Rearth*1000.0)/R)   # angle in horizon in radians # Rearth multiplied by 1000 to get in meters
Thor = (Hang/np.pi)*T     # total time in horizon in seconds

outdat = open("outputs.txt", 'w')  # open new file and truncate all data in it
outdat.write("Rorbit(km) \t Vorbit (km/s) \t Torbit(min) \t Theta(deg) \t Thorizon(min)\n")
# converting units for variables
Rorbit = round(R/1000.0,16)
Vorbit = round(v/1000.0,4)
Torbit = round(T/60.0,3)
Theta = round((Hang*180)/np.pi,3)
Thorizon = round(Thor/60.0,3)
# need to round off the values to make them easier to read

# writing in output file
outdat.write(str(Rorbit) + "\t\t" + str(Vorbit) + "\t\t" + str(Torbit) + "\t\t" + str(Theta) + "\t\t" + str(Thorizon) + "\n")

