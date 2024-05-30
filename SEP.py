import numpy as np
import cmath as cm

#FAZER UMA FUNÇÃO PARA CONVERTER PRA PU AS POTENCIAS

Nz = 3      #Numero de Impedâncias
PQN = 2      #Numero de Barras de Carga
PV = 0      #Numero de Barras de Geração
Vslack = cm.rect(1.05,0)
PQ = np.zeros(PQN,dtype=complex)
PQ[0] =

ZN = np.zeros(Nz,dtype=complex) #Array para as impedancias
YN = np.zeros(Nz*Nz,dtype=complex)
YN = YN.reshape(Nz,Nz)

#Inserindo as impedancias manualmente
ZN[0] = complex(0.02,0.04)      #Z12
ZN[1] = complex(0.01,0.03)    #Z13
ZN[2] = complex(0.0125,0.025)  #Z23

YN[0,0] = ((1/ZN[0])+(1/ZN[1]))     #ADMITANCIA 11
YN[1,1] = ((1/ZN[0])+(1/ZN[2]))     #ADMITANCIA 22
YN[2,2] = ((1/ZN[1])+(1/ZN[2]))     #ADMITANCIA 33

YN[0,1] = -1/ZN[0]     #ADMITANCIA 12
YN[1,0] = YN[0,1]     #ADMITANCIA 21
YN[0,2] = -1/ZN[1]     #ADMITANCIA 25
YN[2,0] = YN[0,2]     #ADMITANCIA 52
YN[1,2] = -1/ZN[2]     #ADMITANCIA 45
YN[2,1] = YN[1,2]     #ADMITANCIA 54

print(YN)       #MATRIZ ADMITANCIA

precision = 0.00001
IT=1
aux = np.zeros(PQN,dtype=complex)
Vpq = np.zeros(PQN,dtype=complex)
while IT > precision:

    #faz
    Vpq[0] = (1/YN[1,1])*(aux)


    if IT <= precision:
        break
