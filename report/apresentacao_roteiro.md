# Roteiro de Apresentação: Comparação de Árvores de Busca

Este roteiro foi dividido para 4 integrantes, focando na lógica, funcionamento e comparação das estruturas.

---

## Integrante 1: Árvore Binária de Busca (BST)

**Conceito Principal:**
A BST é a estrutura fundamental. A regra é simples: para qualquer nó, todos os valores à **esquerda** são menores e todos à **direita** são maiores.

**Como funciona (Lógica):**
*   **Busca:** Começa na raiz. Se o valor buscado for menor, vai para a esquerda; se for maior, vai para a direita. É como uma busca binária em um array ordenado.
*   **Inserção:** Segue a mesma lógica da busca até encontrar uma posição vazia (None) e insere o novo nó lá.

**Problema (O "Pior Caso"):**
*   Se inserirmos dados já ordenados (ex: 1, 2, 3, 4...), a árvore vira uma "lista ligada" (toda torta para a direita).
*   Nesse caso, a eficiência cai de **O(log n)** para **O(n)**. Ou seja, perde a vantagem de ser uma árvore.

**Quando usar:**
*   Apenas quando sabemos que os dados chegarão de forma aleatória.
*   Não recomendada para sistemas críticos onde o desempenho deve ser garantido.

---

## Integrante 2 (Você): Árvore AVL

**Conceito Principal:**
A AVL foi a primeira árvore **auto-balanceada** inventada. O objetivo dela é resolver o problema da BST, garantindo que a altura da árvore seja sempre a menor possível (logarítmica).

**Como funciona (Lógica):**
*   **Fator de Balanceamento:** Cada nó calcula: `Altura da Esquerda - Altura da Direita`.
*   O valor deve ser sempre **-1, 0 ou 1**.
*   Se passar disso (ex: 2 ou -2), a árvore está desbalanceada.
*   **Rotações:** Para consertar, a AVL faz **Rotações** (Simples ou Duplas). É como "girar" os nós para redistribuir o peso e diminuir a altura.

**Vantagens e Desvantagens:**
*   **Vantagem:** É a árvore mais "estritamente" balanceada. A busca é extremamente rápida porque a altura é mínima.
*   **Desvantagem:** Manter esse balanceamento perfeito custa caro. Inserções e remoções exigem muitas rotações, o que pode ser lento.

**Quando usar:**
*   Em cenários onde há **muitas buscas** e **poucas inserções** (ex: um dicionário ou banco de dados de leitura intensiva).

---

## Integrante 3: Árvore Rubro-Negra (Red-Black)

**Conceito Principal:**
A Rubro-Negra também é balanceada, mas de forma mais "relaxada" que a AVL. Ela usa um sistema de cores (Vermelho e Preto) e regras para manter o equilíbrio.

**Como funciona (Lógica):**
*   Todo nó tem uma cor. A raiz é sempre preta.
*   Não podem existir dois nós vermelhos seguidos (pai e filho).
*   O número de nós pretos em qualquer caminho da raiz até uma folha deve ser o mesmo.
*   Se as regras forem violadas na inserção/remoção, ela corrige com **Recoloração** (troca de cores) e **Rotações**.

**Vantagens e Desvantagens:**
*   **Vantagem:** Ela faz **menos rotações** que a AVL. Isso torna a inserção e remoção mais rápidas.
*   **Desvantagem:** A árvore pode ficar um pouco mais alta que a AVL, então a busca é levemente mais lenta (mas ainda muito rápida).

**Quando usar:**
*   É a árvore de propósito geral mais usada no mundo real (ex: `TreeMap` do Java, `std::map` do C++).
*   Ideal quando há um equilíbrio entre operações de busca e modificação (inserção/remoção).

---

## Integrante 4: Comparação e Eficiência

**Análise de Complexidade (Big O):**

| Estrutura | Busca (Médio) | Busca (Pior) | Inserção (Médio) | Inserção (Pior) |
| :--- | :--- | :--- | :--- | :--- |
| **BST** | O(log n) | **O(n)** (Lento!) | O(log n) | **O(n)** |
| **AVL** | **O(log n)** | O(log n) | O(log n) | O(log n) |
| **Rubro-Negra**| O(log n) | O(log n) | **O(log n)** | O(log n) |

**Resultados dos Nossos Testes (Benchmark):**
*   **Dados Aleatórios:** As três árvores têm desempenho similar. A BST é muito rápida porque não perde tempo calculando balanceamento.
*   **Dados Ordenados (O Teste de Fogo):**
    *   A **BST** "morre". O tempo explode e a altura fica igual ao número de elementos.
    *   A **AVL** e a **Rubro-Negra** mantêm o desempenho estável (logarítmico), provando o valor do balanceamento.

**Comparativo Final:**
1.  **Altura:** AVL < Rubro-Negra < BST (Pior caso). *AVL vence em compactação.*
2.  **Velocidade de Busca:** AVL vence (por pouco) a Rubro-Negra.
3.  **Velocidade de Inserção:** BST (Aleatório) > Rubro-Negra > AVL.

**Conclusão:**
Para sistemas reais, **árvores balanceadas são essenciais**. A Rubro-Negra é geralmente a escolha padrão por ser "boa em tudo", enquanto a AVL é especialista em buscas rápidas.
