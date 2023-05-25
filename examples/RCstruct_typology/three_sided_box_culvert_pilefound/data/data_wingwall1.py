import math
estrName='Aleta 1'
nmbAleta=1
titSchedule=estrName.upper()

scale=1/25 # escala del dibujo

#Footing
wFoot=1.90 #ancho zapata
lWall=3.50 #longitud muro
thFoot=0.35 #espesor de la zapata
wToe=0  #ancho de la puntera

# Wall 
wTop=0.25  #espesor del muro en coronación
hWallMax=2.6
hWallMin=1.26
slopeBack=0  #pendiente del trasdós (H/V)
alpha_degrees=math.degrees(math.atan(slopeBack)) 

# excavaciones y rellenos
Hexcav=thFoot+0.6+0.1
Hrell=Hexcav

reinf=369.92 # kg acero (cimentación+alzado)

delta_talud=18.29 #ángulo del talud con la aleta
