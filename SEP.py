import cmath

import numpy as np
import cmath as cm

Nb = 5      #NUMERO DE BARRAS

Sb = 100000000
Vb13 = 15000
Vb245 = 345000

Zb13 = (Vb13**2)/Sb
Zb245 = (Vb245**2)/Sb

#Matriz Admitancia v2

Yt = np.zeros(Nb*Nb,dtype=complex)

#Impedancias
Zt = np.array([complex(0.0015+0.02j),complex(0.0045+0.05j),complex(0.009+0.1j),complex(0.00075+0.01j),complex(0.00152+0.015j)], dtype=complex)        #Z15 - Z52 - Z24 - Z43 - Z45

B24 = complex(0+1.72j)
B25 = complex(0+0.88j)
B45 = complex(0+0.44j)



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

Pesp = np.array([0,-8,0,0,0])           #Potencia Ativas Pg-Pl P1 - P2 - P3 - P4 - P5
Qesp = np.array([0,-2.8,0,0,0])         #Potencia Reativas Qg-Ql Q1 - Q2 - Q3 - Q4 - Q5

#CALCULANDO AS TENSOES 

Vt = np.array([1, 1, 1.05, 1, 1],dtype=complex)     #Tensoes Iniciais em cada barra em ordem 1 - 2 - 3 - 4 - 5
Vta = np.zeros(Nb,dtype=complex)
auxR = np.zeros(Nb)
auxIm = np.zeros(Nb)

#Barras PQ     2 - 4 - 5  OU SEJA NAO CONHEÇO A TENSAO DESSES
#Barras PV     1 - 3      OU SEJA NAO CONHEÇO NO MINIMO O Q DELES

Npv = 2     #Numeros barras PV

Qcalc = np.zeros(Npv,dtype=complex)       # Barra 1 - 3
Vtp = np.zeros(Npv, dtype=complex)         # Barra 1 - 3

i=1
while i!=0:

    Vta = Vt
    Qcalc[0] = np.conj(Vta[0])*((Vta[0]*Yt[0][0]) + Yt[0][1]*Vta[1] + Yt[0][2]*Vta[2] + Yt[0][3]*Vta[3] + Yt[0][4]*Vta[4])
    Qcalc[1] = np.conj(Vta[2])*((Vta[2]*Yt[2][2]) + Yt[2][1]*Vta[1] + Yt[2][0]*Vta[0] + Yt[2][3]*Vta[3] + Yt[2][4]*Vta[4])      #Nao confundir aqui é da barra 3

    Qcalc[0] = - Qcalc[0].imag
    Qcalc[1] = - Qcalc[1].imag      #Nao confundir aqui é da barra 3

    if Qcalc[0] < -2.8:
        Qcalc[0] = -2.8
    else:
        if(Qcalc[0] > 4):
            Qcalc[0] = 4

    if Qcalc[1] < -2.8:
        Qcalc[1] = -2.8
    else:
        if(Qcalc[1] > 4):
            Qcalc[1] = 4

    Vtp[0] = (1/Yt[0][0])*(((Pesp[0]-complex(0,Qcalc[0]))/np.conj(Vta[0])) - Yt[0][1]*Vta[1] - Yt[0][2]*Vta[2] - Yt[0][3]*Vta[3] - Yt[0][4]*Vta[4])
    Vtp[1] = (1/Yt[2][2])*(((Pesp[2]-complex(0,Qcalc[1]))/np.conj(Vta[2])) - Yt[2][1]*Vta[1] - Yt[2][0]*Vta[0] - Yt[2][3]*Vta[3] - Yt[2][4]*Vta[4])

    #Modificar o Vtp para polar e mudar o seu angulo

    Vtpang0 = np.angle(Vtp[0])
    Vtpang1 = np.angle(Vtp[1])

    Vt[0] = abs(Vta[0]) * np.exp(1j*Vtpang0)
    Vt[2] = abs(Vta[2]) * np.exp(1j*Vtpang1)

    # Vta[0] = cmath.polar(Vta[0])
    # Vta[2] = cmath.polar(Vta[2])


    Vt[1]=(1/Yt[1][1])*(((Pesp[1]-complex(0,Qesp[1]))/(np.conj(Vta[1]))) - Yt[1][0]*Vta[0] - Yt[1][2]*Vta[2] - Yt[1][3]*Vta[3] - Yt[1][4]*Vta[4])
    Vt[3]=(1/Yt[3][3])*(((Pesp[3]-complex(0,Qesp[3]))/(np.conj(Vta[3]))) - Yt[3][0]*Vta[0] - Yt[3][2]*Vta[2] - Yt[3][1]*Vta[1] - Yt[3][4]*Vta[4])
    Vt[4]=(1/Yt[4][4])*(((Pesp[4]-complex(0,Qesp[4]))/(np.conj(Vta[4]))) - Yt[4][0]*Vta[0] - Yt[4][2]*Vta[2] - Yt[4][3]*Vta[3] - Yt[4][1]*Vta[1])

    auxR[1] = Vt[1].real - Vta[1].real
    auxR[3] = Vt[3].real - Vta[3].real
    auxR[4] = Vt[4].real - Vta[4].real

    auxIm[1] = Vt[1].imag - Vta[1].imag
    auxIm[3] = Vt[3].imag - Vta[3].imag
    auxIm[4] = Vt[4].imag - Vta[4].imag

    auxR[1] = abs(auxR[1])
    auxR[3] = abs(auxR[3])
    auxR[4] = abs(auxR[4])

    auxIm[1] = abs(auxIm[1])
    auxIm[3] = abs(auxIm[3])
    auxIm[4] = abs(auxIm[4])

    if(auxR[1]<=0.00001 and auxIm[1]<=0.00001 and auxR[3]<=0.00001 and auxIm[3]<=0.00001 and auxR[4]<=0.00001 and auxIm[4]<=0.00001):
        i=0

print("Tensões das barras")
print(Vt)

# Nz = 3      #Numero de Impedâncias
# PQN = 2      #Numero de Barras de Carga
# PV = 0      #Numero de Barras de Geração
# Vslack = cm.rect(1.05,0)
#
# sq = np.zeros(PQN,dtype=complex)        #Potencia da Carga em PU LEMBRAR QUE NO TRABALHO TEM UMA BARRA COM CARGA E GERACAO DAI PRECISA CALCULAR CORRETAMENTE
# sq[0] = -(2.566 - 1j*1.102)             #O menos faz parte da formula, ja to deixando pronto pra facilitar
# sq[1] = -(1.386 - 1j*0.452)
#
# ZN = np.zeros(Nz,dtype=complex) #Array para as impedancias
# YN = np.zeros(Nz*Nz,dtype=complex)
# YN = YN.reshape(Nz,Nz)
#
# #Inserindo as impedancias manualmente
# ZN[0] = complex(0.02,0.04)      #Z12
# ZN[1] = complex(0.01,0.03)    #Z13
# ZN[2] = complex(0.0125,0.025)  #Z23
#
# YN[0,0] = ((1/ZN[0])+(1/ZN[1]))     #ADMITANCIA 11
# YN[1,1] = ((1/ZN[0])+(1/ZN[2]))     #ADMITANCIA 22
# YN[2,2] = ((1/ZN[1])+(1/ZN[2]))     #ADMITANCIA 33
#
# YN[0,1] = -1/ZN[0]     #ADMITANCIA 12
# YN[1,0] = YN[0,1]     #ADMITANCIA 21
# YN[0,2] = -1/ZN[1]     #ADMITANCIA 25
# YN[2,0] = YN[0,2]     #ADMITANCIA 52
# YN[1,2] = -1/ZN[2]     #ADMITANCIA 45
# YN[2,1] = YN[1,2]     #ADMITANCIA 54
#
# #print(YN)       #MATRIZ ADMITANCIA
#
# precision = 0.00001
# IT=1
# IT2=1
# aux = np.zeros(PQN,dtype=complex)
# aux[0] = 1      #V2 IT-1
# aux[1] = 1      #V3 IT-1
# Vpq = np.zeros(PQN,dtype=complex)
# while IT > precision:
#
#     #faz
#     Vpq[0] = (1/YN[1, 1])*((sq[0]/np.conj(aux[0]))-((YN[0,1]*Vslack)+(YN[1,2]*aux[1])))      #ITERACAO PARA V2
#
#     Vpq[1] = (1 / YN[2, 2]) * ((sq[1] / np.conj(aux[1])) - ((YN[0, 2] * Vslack) + (YN[1, 2] * aux[0])))
#
#     RV2N_1,a = cm.polar(aux[0])
#     RV2N,b = cm.polar(Vpq[0])
#     RV3N_1,c = cm.polar(aux[1])
#     RV3N,d = cm.polar(Vpq[1])
#     IT = RV2N_1 - RV2N
#     IT2 = RV3N_1 - RV3N
#     if(IT2>IT):
#         IT=IT2
#     aux[0] = Vpq[0]
#     aux[1] = Vpq[1]
#
#
#     if IT <= precision:
#         break
#
# # V2 = cm.polar(Vpq[0])
# # V3 = cm.polar(Vpq[1])
# # print(V2)
# # print(V3)