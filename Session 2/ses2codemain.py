import numpy as np

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

n = 11      # number of steps of height

H = np.linspace(400000,600000,n) # heights in m
# make array of heights at a distance of 20km each

R = [0]*n
V = [0]*n
W = [0]*n
Hang = [0]*n
Thor = [0]*n
deltaT = [0]*n          # declare 1D arrays

m = 100     # number of steps for acceleration calc

theta = [[0]*(m+2)]*n
elvAng = [[0]*(m+2)]*n
wcraft = [[0]*(m+1)]*n
alpha = [[0]*m]*n           # declare 2D arrays

outivals = open("orbit outputs (i).txt", 'w')
outivals.write("Rorbit(km) \t Vorbit (km/s) \t Worbit(deg/s) \t Hang(deg) \t Thor(min) \t deltaT(s)\n")

# Calculations
for i in range(n):
    R[i] = Rearth*1000 + H[i]   # in meters
    V[i] = np.sqrt((Gconst*Mearth)/R[i])    # in m/s
    W[i] = (V[i]/R[i]) + (2*np.pi)/86400      # in radians/s
    Hang[i] = np.arccos((Rearth*1000.0)/R[i])    # in radians
    Thor[i] = (2*Hang[i])/W[i]      # in seconds
    deltaT[i] = Thor[i]/(2*m+2)         # in seconds
    
    rtemp = round(R[i]/1000,1)
    vtemp = round(V[i]/1000,3)
    wtemp = round((W[i]*180)/np.pi,4)
    htemp = round((Hang[i]*180)/np.pi,2)
    ttemp = round(Thor[i]/60,2)
    dttemp = round(deltaT[i],2)   # rounding off values, converting to km, min, and degrees as needed

    outivals.write(str(rtemp) + "\t\t" + str(vtemp) + "\t\t" + str(wtemp) + "\t\t" + str(htemp) + "\t\t" + str(ttemp) + "\t\t" + str(dttemp) + "\n")

    theta[i] = [0]*(m+2)
    elvAng[i] = [0]*(m+2)
    wcraft[i] = [0]*(m+1)
    alpha[i] = [0]*m            # declare current row of all 2D arrays in the loop again

    theta[i][0] = np.pi/2 - Hang[i]
    theta[i][m+1] = np.pi/2
    elvAng[i][0] = 0
    elvAng[i][m+1] = np.pi/2

    
    height = (H[i]/1000)
    name = "vectors for h " + str(height) + ".txt"       # get files for each height in km
    outdat = open(name, 'w')
    outdat.write("theta(deg) \t elvAng (deg) \t wcraft(deg/s) \t alpha(deg/s^2)\n")

    for j in range(m):
        theta[i][j+1] = np.pi/2 - Hang[i] + (Hang[i]*(j+1))/(m+1)
        elvAng[i][j+1] = np.arctan(np.tan(theta[i][j+1]) - (Rearth*1000)/(R[i]*np.cos(theta[i][j+1])))
        wcraft[i][j] = (elvAng[i][j+1]-elvAng[i][j])/deltaT[i]
    
    wcraft[i][m] = (elvAng[i][m+1]-elvAng[i][m])/deltaT[i]

    thetemp = round((theta[i][0]*180)/np.pi,2)
    elevation = round((elvAng[i][0]*180)/np.pi,2)
    
    outdat.write(str(thetemp) + "\t\t" + str(elevation) + "\n")  # write first line for variables of m+2 size arrays

    thetemp = round((theta[i][1]*180)/np.pi,3)
    elevation = round((elvAng[i][1]*180)/np.pi,3)
    omega = round((wcraft[i][0]*180)/np.pi,4)
    outdat.write(str(thetemp) + "\t\t" + str(elevation) + "\t\t" + str(omega) + "\n")  
    # write second line with omega (m+1 size), but not accel (m size)

    for j in range(m):
        alpha[i][j] = (wcraft[i][j+1]-wcraft[i][j])/deltaT[i]

        thetemp = round((theta[i][j+2]*180)/np.pi,3)
        elevation = round((elvAng[i][j+2]*180)/np.pi,3)
        omega = round((wcraft[i][j+1]*180)/np.pi,4)
        accel = round((alpha[i][j]*180)/np.pi,6)
        outdat.write(str(thetemp) + "\t\t" + str(elevation) + "\t\t" + str(omega) + "\t\t" + str(accel) + "\n")
    
    outdat.close()    # close outdat in every loop so new file can be opened in next loop
    

outivals.close()        # close all files for reading and writing