import numpy as np


def inicializar_matrizes():
    # Define a matriz de impedância (Z)
    matriz_impedancia = np.array([
        [0, 0, 0, 0, 0.0015 + 1j * 0.020],
        [0, 0, 0, 0.0090 + 1j * 0.1, 0.0045 + 1j * 0.050],
        [0, 0, 0, 0.00075 + 1j * 0.01, 0],
        [0, 0.0090 + 1j * 0.1, 0.00075 + 1j * 0.01, 0, 0.00152 + 1j * 0.015],
        [0.0015 + 1j * 0.020, 0.0045 + 1j * 0.050, 0, 0.00152 + 1j * 0.015, 0]
    ], dtype=complex)

    # Define a matriz de admitância shunt (B)
    matriz_admitancia_shunt = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1.72, 0.88],
        [0, 0, 0, 0, 0],
        [0, 1.72, 0, 0, 0.44],
        [0, 0.88, 0, 0.44, 0]
    ], dtype=complex)

    return matriz_impedancia, matriz_admitancia_shunt


def calcular_matriz_admitancia(matriz_impedancia, matriz_admitancia_shunt):
    # Inicializa a matriz de admitância Y1 (recíproca da matriz de impedância para elementos não nulos)
    matriz_admitancia_Y1 = np.zeros_like(matriz_impedancia, dtype=complex)
    for k in range(5):
        for n in range(5):
            if matriz_impedancia[k, n] != 0:
                matriz_admitancia_Y1[k, n] = 1 / matriz_impedancia[k, n]

    # Inicializa a matriz de admitância (Y)
    matriz_admitancia = np.zeros_like(matriz_impedancia, dtype=complex)
    soma_tmp = np.sum(matriz_admitancia_Y1, axis=1) + (1j * np.sum(matriz_admitancia_shunt, axis=1) / 2)

    for k in range(5):
        for n in range(5):
            if n == k:
                matriz_admitancia[k, n] = soma_tmp[k]
            else:
                matriz_admitancia[k, n] = -matriz_admitancia_Y1[k, n]

    return matriz_admitancia


def inicializar_valores():
    # Define os valores iniciais para o cálculo de fluxo de potência
    tipos_barra = np.array([1, 2, 3, 2, 2])  # Tipos de barras: 1 = slack, 2 = PQ, 3 = PV
    tensoes = np.array([1.0, 1, 1.05, 1, 1], dtype=complex)
    potencias_ativas = np.array([1, -8, 4.4, 0, 0])
    potencias_reativas = np.array([1, -2.8, -0.4, 0, 0])
    angulos_tensao = np.array([0, 1, 1, 1, 1])  # Ângulos de tensão (não usados diretamente nos cálculos)

    # Estende os arrays de tensões, potências ativas e reativas para iterações
    tensoes = np.vstack([tensoes, np.zeros((3, 5), dtype=complex)])
    potencias_ativas = np.vstack([potencias_ativas, np.zeros((3, 5), dtype=complex)])
    potencias_reativas = np.vstack([potencias_reativas, np.zeros((3, 5), dtype=complex)])

    return tipos_barra, tensoes, potencias_ativas, potencias_reativas, angulos_tensao


def atualizar_tensoes(tipos_barra, tensoes, potencias_ativas, potencias_reativas, matriz_admitancia, reativo_min,
                      reativo_max):
    # Atualiza as tensões nas iterações de fluxo de potência
    erros = np.ones((5, 2), dtype=float)  # Matriz de erro para verificação de convergência
    tolerancia = 0.00001  # Tolerância de convergência
    iteracao = 1  # Contador de iteração

    while iteracao < 300:
        tensoes[2, :] = tensoes[0, :]  # Faz backup das tensões atuais para cálculo de erro

        # Verifica a convergência
        if np.all(erros[1:, 0] <= tolerancia) and np.all(erros[1:, 1] <= tolerancia):
            num_iteracoes = iteracao
            iteracao = 1000
            break

        # Atualiza as tensões
        for k in range(1, 5):
            soma_tensao = sum(matriz_admitancia[k, m] * tensoes[0, m] for m in range(5) if m != k)
            if tipos_barra[k] == 2:  # Barra PQ
                tensoes[0, k] = ((potencias_ativas[0, k] - 1j * potencias_reativas[0, k]) / np.conj(
                    tensoes[0, k]) - soma_tensao) / matriz_admitancia[k, k]
            elif tipos_barra[k] == 3:  # Barra PV
                potencias_reativas[0, k] = -np.imag(
                    np.conj(tensoes[0, k]) * (tensoes[0, k] * matriz_admitancia[k, k] + soma_tensao))
                potencias_reativas[0, k] = np.clip(potencias_reativas[0, k], reativo_min,
                                                   reativo_max)  # Aplica limites de Q
                tensoes[1, k] = ((potencias_ativas[0, k] - 1j * potencias_reativas[0, k]) / np.conj(
                    tensoes[0, k]) - soma_tensao) / matriz_admitancia[k, k]
                angulo_tmp = np.angle(tensoes[1, k])
                tensoes[0, k] = np.abs(tensoes[0, k]) * np.exp(1j * angulo_tmp)

        # Calcula os erros
        for k in range(1, 5):
            erros[k, 0] = np.abs(np.real(tensoes[0, k]) - np.real(tensoes[2, k]))
            erros[k, 1] = np.abs(np.imag(tensoes[0, k]) - np.imag(tensoes[2, k]))

        iteracao += 1

    return tensoes, potencias_ativas, potencias_reativas


def calcular_potencia_slack(matriz_admitancia, tensoes):
    indice_slack = 0  # Índice da barra slack
    soma_tensao = sum(matriz_admitancia[indice_slack, m] * tensoes[0, m] for m in range(5) if m != indice_slack)
    potencia_ativa_slack = np.real(tensoes[0, indice_slack] * (
                tensoes[0, indice_slack] * matriz_admitancia[indice_slack, indice_slack] + soma_tensao))
    potencia_reativa_slack = -np.imag(tensoes[0, indice_slack] * (
                tensoes[0, indice_slack] * matriz_admitancia[indice_slack, indice_slack] + soma_tensao))
    return potencia_ativa_slack, potencia_reativa_slack


def imprimir_resultados_tensao(tensoes):
    angulos_tensao = np.rad2deg(np.angle(tensoes[0, :]))  # Ângulos de tensão em graus
    magnitudes_tensao = np.abs(tensoes[0, :])  # Magnitudes de tensão

    # Imprime os resultados de tensão
    print('\nTensões das barras')
    for k in range(5):
        print(f'V{k + 1} = {magnitudes_tensao[k]:.4f} < {angulos_tensao[k]:.4f}')


def calcular_fluxo_potencia(matriz_impedancia, matriz_admitancia_shunt, tensoes):
    fluxo_potencia = np.zeros((5, 5), dtype=complex)
    print('\nFluxo de potências nas linhas')
    for k in range(5):
        for m in range(5):
            if matriz_impedancia[k, m] != 0 and k != m:
                fluxo_potencia[k, m] = tensoes[0, k] * np.conj(
                    (tensoes[0, k] - tensoes[0, m]) / matriz_impedancia[k, m] + (
                                1j * matriz_admitancia_shunt[k, m] / 2) * tensoes[0, k])
                print(
                    f'S{k + 1}{m + 1} = {np.real(fluxo_potencia[k, m]):.4f} + {np.imag(fluxo_potencia[k, m]):.4f}i pu')
    return fluxo_potencia


def calcular_perdas_linha(fluxo_potencia):
    perdas_linha = np.zeros_like(fluxo_potencia)
    for k in range(5):
        for m in range(5):
            if k != m:
                perdas_linha[k, m] = fluxo_potencia[k, m] + fluxo_potencia[m, k]

    perdas_ativas = np.real(perdas_linha)
    perdas_reativas = np.imag(perdas_linha)

    # Imprime as perdas de potência nas linhas de transmissão
    print('\nPerdas de potência ativa e reativa nas LTs')
    print(f'Sl45 = {perdas_ativas[3, 4]:.4f} + {perdas_reativas[3, 4]:.4f}i')
    print(f'Sl24 = {perdas_ativas[1, 3]:.4f} + {perdas_reativas[1, 3]:.4f}i')
    print(f'Sl25 = {perdas_ativas[1, 4]:.4f} + {perdas_reativas[1, 4]:.4f}i')


def main():
    matriz_impedancia, matriz_admitancia_shunt = inicializar_matrizes()
    matriz_admitancia = calcular_matriz_admitancia(matriz_impedancia, matriz_admitancia_shunt)
    tipos_barra, tensoes, potencias_ativas, potencias_reativas, angulos_tensao = inicializar_valores()
    reativo_min, reativo_max = -2.8, 4.0

    tensoes, potencias_ativas, potencias_reativas = atualizar_tensoes(tipos_barra, tensoes, potencias_ativas,
                                                                      potencias_reativas, matriz_admitancia,
                                                                      reativo_min, reativo_max)
    potencia_ativa_slack, potencia_reativa_slack = calcular_potencia_slack(matriz_admitancia, tensoes)
    imprimir_resultados_tensao(tensoes)
    fluxo_potencia = calcular_fluxo_potencia(matriz_impedancia, matriz_admitancia_shunt, tensoes)
    calcular_perdas_linha(fluxo_potencia)

    # Imprime fluxo de potência específico
    print(f'Sg1 = {np.real(fluxo_potencia[0, 4]):.4f} + {np.imag(fluxo_potencia[0, 4]):.4f}i pu')


if __name__ == "__main__":
    main()
