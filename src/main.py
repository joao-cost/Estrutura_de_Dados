import sys
import os
import time
import pandas as pd
from bst import BST
from avl import ArvoreAVL
from rbt import ArvoreRubroNegra
from utils import gerar_dados_aleatorios, gerar_dados_ordenados, medir_tempo

# Aumentar limite de recursão para árvores profundas (pior caso BST)
sys.setrecursionlimit(20000)

def executar_benchmark(tamanhos=[100, 1000, 10000]):
    resultados = []

    for tamanho in tamanhos:
        print(f"Executando testes para tamanho: {tamanho}")
        
        # Conjuntos de dados
        dados_aleatorios = gerar_dados_aleatorios(tamanho)
        dados_ordenados = gerar_dados_ordenados(tamanho)
        
        conjuntos_dados = {"Aleatório": dados_aleatorios, "Ordenado": dados_ordenados}
        
        for tipo_dado, dados in conjuntos_dados.items():
            # Árvores
            arvores = {
                "BST": BST(),
                "AVL": ArvoreAVL(),
                "Rubro-Negra": ArvoreRubroNegra()
            }
            
            for nome_arvore, arvore in arvores.items():
                print(f"  Testando {nome_arvore} com dados {tipo_dado}...")
                
                # Inserção
                inicio = time.perf_counter()
                total_comparacoes_insercao = 0
                for item in dados:
                    total_comparacoes_insercao += arvore.inserir(item['id'], item['valor'])
                fim = time.perf_counter()
                tempo_insercao_ms = (fim - inicio) * 1000
                
                # Métricas após inserção
                altura_final = arvore.obter_altura()
                contagem_nos = arvore.contar_nos()
                rotacoes = arvore.obter_contagem_rotacoes()

                # Busca (buscar todas as chaves para média)
                inicio = time.perf_counter()
                total_comparacoes_busca = 0
                for item in dados:
                    encontrado, comps = arvore.buscar(item['id'])
                    total_comparacoes_busca += comps
                fim = time.perf_counter()
                tempo_busca_ms = (fim - inicio) * 1000
                
                # Remoção (remover metade das chaves)
                chaves_para_remover = dados[:tamanho//2]
                inicio = time.perf_counter()
                total_comparacoes_remocao = 0
                for item in chaves_para_remover:
                    total_comparacoes_remocao += arvore.remover(item['id'])
                fim = time.perf_counter()
                tempo_remocao_ms = (fim - inicio) * 1000
                
                resultados.append({
                    "Tamanho": tamanho,
                    "Tipo de Dado": tipo_dado,
                    "Árvore": nome_arvore,
                    "Tempo Inserção (ms)": round(tempo_insercao_ms, 4),
                    "Comparações Médias Inserção": round(total_comparacoes_insercao / tamanho, 2),
                    "Tempo Busca (ms)": round(tempo_busca_ms, 4),
                    "Comparações Médias Busca": round(total_comparacoes_busca / tamanho, 2),
                    "Tempo Remoção (ms)": round(tempo_remocao_ms, 4),
                    "Comparações Médias Remoção": round(total_comparacoes_remocao / (tamanho//2), 2),
                    "Altura Final": altura_final,
                    "Total Nós": contagem_nos,
                    "Rotações": rotacoes
                })

    df = pd.DataFrame(resultados)
    print("\nResultados do Benchmark:")
    print(df)
    
    # Salvar em CSV
    if not os.path.exists("report"):
        os.makedirs("report")
    df.to_csv("report/resultados_benchmark.csv", index=False)
    print("\nResultados salvos em report/resultados_benchmark.csv")

if __name__ == "__main__":
    executar_benchmark()
