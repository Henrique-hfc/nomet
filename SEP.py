import numpy as np
import cmath as cm

Nb = 5      #NUMERO DE BARRAS

Sb = 100000000
Vb13 = 15000
Vb245 = 345000

Zb13 = (Vb13**2)/Sb
Zb245 = (Vb245**2)/Sb

Vt = np.array([1, 1, 1.05, 1, 1],dtype=complex)     #Tensoes Iniciais em cada barra em ordem 1 - 2 - 3 - 4 - 5

#Matriz Admitancia v2

Yt = np.zeros(Nb*Nb,dtype=complex)

#Impedancias
Zt = np.array([complex(0.0015, 0.02),complex(0.0045, 0.05),complex(0.009, 0.1),complex(0.00075, 0.01),complex(0.00152, 0.015)],dtype=complex)        #Z15 - Z52 - Z24 - Z43 - Z45

B24 = complex(0, 1.72)
B25 = complex(0, 0.88)
B45 = complex(0, 0.44)

#DIAGONAL PRINCIPAL
Yt[0] = 1/Zt[0]                                             #Y11
Yt[6] = (1/Zt[1])+(1/Zt[2]+(B24/2)+(B25/2))                 #Y22
Yt[12] = 1/Zt[3]                                            #Y33
Yt[18] = (1/Zt[3])+(1/Zt[4])+(1/Zt[2])+(B24/2)+(B45/2)      #Y44
Yt[24] = (1/Zt[0])+(1/Zt[4])+(1/Zt[1])+(B25/2)+(B45/2)      #Y55

Yt[4] = -(1/Zt[0])                                          #Y15
Yt[8] = -(1/Zt[2])                                          #Y24
Yt[9] = -(1/Zt[1])                                          #Y25
Yt[13] = -(1/Zt[3])                                         #Y34
Yt[16] = Yt[8]                                              #Y42
Yt[17] = Yt[13]                                             #Y43
Yt[19] = -(1/Zt[4])                                         #Y44
Yt[20] = Yt[4]                                              #Y45
Yt[21] = Yt[9]                                              #Y52
Yt[23] = Yt[19]                                             #Y54

Yt = Yt.reshape(Nb, Nb) #Preferi trabalhar em vetor por isso depois joguei pra matriz


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