import numpy as np
import random

# Função para calcular a distância total de uma rota
def calcular_distancia(rota, matriz_distancias):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += matriz_distancias[rota[i] - 1][rota[i + 1] - 1]
    # Adicionar a distância de volta para a cidade inicial
    distancia_total += matriz_distancias[rota[-1] - 1][rota[0] - 1]
    return distancia_total

# Função para escolher a próxima cidade com base na probabilidade
def escolher_proxima_cidade(formiga_atual, cidades_a_visitar, matriz_feromonios, matriz_distancias, alpha, beta):
    probabilidades = []
    for cidade in cidades_a_visitar:
        feromonio = matriz_feromonios[formiga_atual - 1][cidade - 1] ** alpha
        visibilidade = (1 / matriz_distancias[formiga_atual - 1][cidade - 1]) ** beta
        probabilidades.append(feromonio * visibilidade)
    
    # Normalizar probabilidades
    soma_probabilidades = sum(probabilidades)
    probabilidades = [p / soma_probabilidades for p in probabilidades]
    
    # Escolher a cidade com base nas probabilidades
    return random.choices(cidades_a_visitar, weights=probabilidades, k=1)[0]

# Algoritmo ACO
def ACO(matriz_distancias, num_formigas, num_iteracoes, alpha=1, beta=5, evaporacao=0.5):
    num_cidades = len(matriz_distancias)
    matriz_feromonios = np.ones((num_cidades, num_cidades))  # Inicializar matriz de feromônios com 1
    melhor_rota = None
    melhor_distancia = float('inf')

    for _ in range(num_iteracoes):
        todas_rotas = []
        todas_distancias = []
        
        # Inserir formigas aleatoriamente nos vértices
        for _ in range(num_formigas):
            rota = [random.randint(1, num_cidades)]
            cidades_a_visitar = list(range(1, num_cidades + 1))
            cidades_a_visitar.remove(rota[0])
            
            # Construir rota para cada formiga
            while cidades_a_visitar:
                proxima_cidade = escolher_proxima_cidade(rota[-1], cidades_a_visitar, matriz_feromonios, matriz_distancias, alpha, beta)
                rota.append(proxima_cidade)
                cidades_a_visitar.remove(proxima_cidade)
            
            distancia = calcular_distancia(rota, matriz_distancias)
            todas_rotas.append(rota)
            todas_distancias.append(distancia)
            
            # Verificar se é a melhor rota até o momento
            if distancia < melhor_distancia:
                melhor_distancia = distancia
                melhor_rota = rota

        # Atualizar o nível de feromônio
        matriz_feromonios *= (1 - evaporacao)  # Evaporação do feromônio
        for rota, distancia in zip(todas_rotas, todas_distancias):
            for i in range(len(rota) - 1):
                matriz_feromonios[rota[i] - 1][rota[i + 1] - 1] += 1 / distancia
            matriz_feromonios[rota[-1] - 1][rota[0] - 1] += 1 / distancia  # Atualizar para o retorno à cidade inicial
    
    return melhor_rota, melhor_distancia

# Exemplo de matriz de distâncias
matriz_distancias = np.array([
    [0, 9, 3, 6, 11],
    [9, 0, 7, 5, 10],
    [3, 7, 0, 9, 2],
    [6, 5, 9, 0, 8],
    [11, 10, 2, 8, 0]
])

# Definir parâmetros
num_formigas = 100
num_iteracoes = 1000
alpha = 1
beta = 5
evaporacao = 0.5

# Rodar ACO
melhor_rota, melhor_distancia = ACO(matriz_distancias, num_formigas, num_iteracoes, alpha, beta, evaporacao)

print(f"Melhor rota: {melhor_rota}")
print(f"Distância total: {melhor_distancia}")
