import numpy as np
import cmath as cm

#FAZER UMA FUNÇÃO PARA CONVERTER PRA PU AS POTENCIAS

Nz = 3      #Numero de Impedâncias
PQN = 2      #Numero de Barras de Carga
PV = 0      #Numero de Barras de Geração
Vslack = cm.rect(1.05,0)

sq = np.zeros(PQN,dtype=complex)        #Potencia da Carga em PU LEMBRAR QUE NO TRABALHO TEM UMA BARRA COM CARGA E GERACAO DAI PRECISA CALCULAR CORRETAMENTE
sq[0] = -(2.566 - 1j*1.102)             #O menos faz parte da formula, ja to deixando pronto pra facilitar
sq[1] = -(1.386 - 1j*0.452)

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
IT2=1
aux = np.zeros(PQN,dtype=complex)
aux[0] = 1      #V2 IT-1
aux[1] = 1      #V3 IT-1
Vpq = np.zeros(PQN,dtype=complex)
while IT > precision:

    #faz
    Vpq[0] = (1/YN[1, 1])*((sq[0]/np.conj(aux[0]))-((YN[0,1]*Vslack)+(YN[1,2]*aux[1])))      #ITERACAO PARA V2

    Vpq[1] = (1 / YN[2, 2]) * ((sq[1] / np.conj(aux[1])) - ((YN[0, 2] * Vslack) + (YN[1, 2] * aux[0])))

    RV2N_1,a = cm.polar(aux[0])
    RV2N,b = cm.polar(Vpq[0])
    RV3N_1,c = cm.polar(aux[1])
    RV3N,d = cm.polar(Vpq[1])
    IT = RV2N_1 - RV2N
    IT2 = RV3N_1 - RV3N
    if(IT2>IT):
        IT=IT2
    aux[0] = Vpq[0]
    aux[1] = Vpq[1]


    if IT <= precision:
        break

V2 = cm.polar(Vpq[0])
V3 = cm.polar(Vpq[1])
print(V2)
print(V3)