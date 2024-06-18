import numpy as np


def inicializar_matrizes():
    # Define a matriz Z (matriz de impedância)
    Z = np.array([
        [0, 0, 0, 0, 0.0015 + 1j * 0.020],
        [0, 0, 0, 0.0090 + 1j * 0.1, 0.0045 + 1j * 0.050],
        [0, 0, 0, 0.00075 + 1j * 0.01, 0],
        [0, 0.0090 + 1j * 0.1, 0.00075 + 1j * 0.01, 0, 0.00152 + 1j * 0.015],
        [0.0015 + 1j * 0.020, 0.0045 + 1j * 0.050, 0, 0.00152 + 1j * 0.015, 0]
    ], dtype=complex)

    # Define a matriz B (matriz de admitância shunt)
    B = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1.72, 0.88],
        [0, 0, 0, 0, 0],
        [0, 1.72, 0, 0, 0.44],
        [0, 0.88, 0, 0.44, 0]
    ], dtype=complex)

    return Z, B


def calcular_matriz_admitancia(Z, B):
    # Inicializa a matriz Y1 (recíproca da matriz Z para elementos não nulos)
    Y1 = np.zeros_like(Z, dtype=complex)
    for k in range(5):
        for n in range(5):
            if Z[k, n] != 0:
                Y1[k, n] = 1 / Z[k, n]

    # Inicializa a matriz Y (matriz de admitância)
    Y = np.zeros_like(Z, dtype=complex)
    tmp = np.sum(Y1, axis=1) + (1j * np.sum(B, axis=1) / 2)

    for k in range(5):
        for n in range(5):
            if n == k:
                Y[k, n] = tmp[k]
            else:
                Y[k, n] = -Y1[k, n]

    return Y


def inicializar_valores():
    # Define os valores iniciais para o cálculo de fluxo de potência
    D = np.array([1, 2, 3, 2, 2])  # Tipos de barras: 1 = slack, 2 = PQ, 3 = PV
    V = np.array([1.0, 1, 1.05, 1, 1], dtype=complex)
    P = np.array([1, -8, 4.4, 0, 0])
    Q = np.array([1, -2.8, -0.4, 0, 0])
    T = np.array([0, 1, 1, 1, 1])  # Ângulos de tensão (não usados diretamente nos cálculos)

    # Estende os arrays V, P, Q para iterações
    V = np.vstack([V, np.zeros((3, 5), dtype=complex)])
    P = np.vstack([P, np.zeros((3, 5), dtype=complex)])
    Q = np.vstack([Q, np.zeros((3, 5), dtype=complex)])

    return D, V, P, Q, T


def atualizar_tensoes(D, V, P, Q, Y, Qmin, Qmax):
    # Atualiza as tensões nas iterações de fluxo de potência
    E = np.ones((5, 2), dtype=float)  # Matriz de erro para verificação de convergência
    Erro = 0.00001  # Tolerância de convergência
    z = 1  # Contador de iteração

    while z < 300:
        V[2, :] = V[0, :]  # Faz backup das tensões atuais para cálculo de erro

        # Verifica a convergência
        if np.all(E[1:, 0] <= Erro) and np.all(E[1:, 1] <= Erro):
            num = z
            z = 1000
            break

        # Atualiza as tensões
        for k in range(1, 5):
            Tsum = sum(Y[k, m] * V[0, m] for m in range(5) if m != k)
            if D[k] == 2:  # Barra PQ
                V[0, k] = ((P[0, k] - 1j * Q[0, k]) / np.conj(V[0, k]) - Tsum) / Y[k, k]
            elif D[k] == 3:  # Barra PV
                Q[0, k] = -np.imag(np.conj(V[0, k]) * (V[0, k] * Y[k, k] + Tsum))
                Q[0, k] = np.clip(Q[0, k], Qmin, Qmax)  # Aplica limites de Q
                V[1, k] = ((P[0, k] - 1j * Q[0, k]) / np.conj(V[0, k]) - Tsum) / Y[k, k]
                tmp_angle = np.angle(V[1, k])
                V[0, k] = np.abs(V[0, k]) * np.exp(1j * tmp_angle)

        # Calcula os erros
        for k in range(1, 5):
            E[k, 0] = np.abs(np.real(V[0, k]) - np.real(V[2, k]))
            E[k, 1] = np.abs(np.imag(V[0, k]) - np.imag(V[2, k]))

        z += 1

    return V, P, Q


def calcular_potencia_slack(Y, V):
    k = 0  # Índice da barra slack
    Tsum = sum(Y[k, m] * V[0, m] for m in range(5) if m != k)
    P_slack = np.real(V[0, k] * (V[0, k] * Y[k, k] + Tsum))
    Q_slack = -np.imag(V[0, k] * (V[0, k] * Y[k, k] + Tsum))
    return P_slack, Q_slack


def imprimir_resultados_tensao(V):
    Va = np.rad2deg(np.angle(V[0, :]))  # Ângulos de tensão em graus
    Vm = np.abs(V[0, :])  # Magnitudes de tensão

    # Imprime os resultados de tensão
    print('\nTensões das barras')
    for k in range(5):
        print(f'V{k + 1} = {Vm[k]:.4f} < {Va[k]:.4f}')


def calcular_fluxo_potencia(Z, B, V):
    S = np.zeros((5, 5), dtype=complex)
    print('Fluxo de potências nas linhas')
    for k in range(5):
        for m in range(5):
            if Z[k, m] != 0 and k != m:
                S[k, m] = V[0, k] * np.conj(((V[0, k] - V[0, m]) / Z[k, m]) + (1j * B[k, m] / 2) * V[0, k])
                print(f'S{k + 1}{m + 1} = {np.real(S[k, m]):.4f} + {np.imag(S[k, m]):.4f}i pu')
    return S


def calcular_perdas_linha(S):
    Sl = np.zeros((5, 5), dtype=complex)
    for k in range(5):
        for m in range(5):
            if k != m:
                Sl[k, m] = S[k, m] + S[m, k]

    Slr = np.real(Sl)
    Sli = np.imag(Sl)

    # Imprime as perdas nas linhas
    print('\nPerdas de potência ativa e reativa nas LTs')
    print(f'Sl45 = {Slr[3, 4]:.4f} + {Sli[3, 4]:.4f}i')
    print(f'Sl24 = {Slr[1, 3]:.4f} + {Sli[1, 3]:.4f}i')
    print(f'Sl25 = {Slr[1, 4]:.4f} + {Sli[1, 4]:.4f}i')


def main():
    Z, B = inicializar_matrizes()
    Y = calcular_matriz_admitancia(Z, B)
    D, V, P, Q, T = inicializar_valores()
    Qmin, Qmax = -2.8, 4.0

    V, P, Q = atualizar_tensoes(D, V, P, Q, Y, Qmin, Qmax)
    P_slack, Q_slack = calcular_potencia_slack(Y, V)
    imprimir_resultados_tensao(V)
    S = calcular_fluxo_potencia(Z, B, V)
    calcular_perdas_linha(S)

    # Imprime fluxo de potência específico
    print(f'Sg1 = {np.real(S[0, 4]):.4f} + {np.imag(S[0, 4]):.4f}i pu')


if __name__ == "__main__":
    main()
