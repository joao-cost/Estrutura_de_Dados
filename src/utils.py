import random
import time
import string

def gerar_string_aleatoria(tamanho=8):
    """Gera uma string aleatória de tamanho fixo (Mantida para compatibilidade)."""
    letras = string.ascii_lowercase
    return ''.join(random.choice(letras) for i in range(tamanho))

def gerar_valor_numerico():
    """Gera um valor numérico aleatório como string."""
    return str(random.randint(100, 99999))

def gerar_dados_aleatorios(tamanho, min_val=0, max_val=100000):
    """Gera uma lista de dicionários com ID único, valor numérico (str) e categoria aleatória."""
    ids = random.sample(range(min_val, max_val + tamanho), tamanho)
    categorias = ["Financeiro", "RH", "TI", "Vendas", "Logística"]
    return [{"id": i, "valor": gerar_valor_numerico(), "categoria": random.choice(categorias)} for i in ids]

def gerar_dados_ordenados(tamanho):
    """Gera uma lista de dicionários ordenados (pior caso para BST)."""
    categorias = ["Financeiro", "RH", "TI", "Vendas", "Logística"]
    return [{"id": i, "valor": gerar_valor_numerico(), "categoria": random.choice(categorias)} for i in range(tamanho)]

def medir_tempo(func, *args):
    """Mede o tempo de execução de uma função."""
    inicio = time.perf_counter()
    resultado = func(*args)
    fim = time.perf_counter()
    return resultado, fim - inicio
