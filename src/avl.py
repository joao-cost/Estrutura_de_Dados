class NoAVL:
    def __init__(self, id, valor, dado_extra=None):
        self.id = id
        self.valor = valor
        self.dado_extra = dado_extra
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        # 'self' é como se fosse o "EU" da árvore.
        # Quando criamos uma árvore nova (arvore = ArvoreAVL()), o 'self' é essa árvore específica.
        self.raiz = None        # Começa vazia
        self.comparacoes = 0    # Contador para o benchmark
        self.rotacoes = 0       # Contador de rotações (o custo do equilíbrio)

    def obter_altura_no(self, no):
        if not no:
            return 0
        return no.altura

    def obter_balanceamento(self, no):
        if not no:
            return 0
        return self.obter_altura_no(no.esquerda) - self.obter_altura_no(no.direita)

    def rotacionar_direita(self, y):
        self.rotacoes += 1
        x = y.esquerda
        T2 = x.direita

        x.direita = y
        y.esquerda = T2

        y.altura = 1 + max(self.obter_altura_no(y.esquerda), self.obter_altura_no(y.direita))
        x.altura = 1 + max(self.obter_altura_no(x.esquerda), self.obter_altura_no(x.direita))

        return x

    def rotacionar_esquerda(self, x):
        self.rotacoes += 1
        y = x.direita
        T2 = y.esquerda

        y.esquerda = x
        x.direita = T2

        x.altura = 1 + max(self.obter_altura_no(x.esquerda), self.obter_altura_no(x.direita))
        y.altura = 1 + max(self.obter_altura_no(y.esquerda), self.obter_altura_no(y.direita))

        return y

    def inserir(self, id, valor, dado_extra=None):
        """
        Função PÚBLICA: É a porta de entrada.
        Quem usa a classe só chama arvore.inserir(10, "A").
        Ela prepara o terreno (zera contadores) e chama a função recursiva que faz o trabalho pesado.
        """
        self.comparacoes = 0
        self.raiz = self._inserir_recursivo(self.raiz, id, valor, dado_extra)
        return self.comparacoes

    def _inserir_recursivo(self, no, id, valor, dado_extra):
        """
        Função PRIVADA (começa com _): Faz a mágica da recursão.
        
        A recursão funciona assim:
        1. Se o nó atual é None (chegamos no fim), cria o novo nó aqui!
        2. Se não, decide se vai para esquerda (menor) ou direita (maior).
        3. Na volta da recursão (desempilhando), verifica o balanceamento e rotaciona se precisar.
        """
        self.comparacoes += 1
        if not no:
            return NoAVL(id, valor, dado_extra)
        
        if id < no.id:
            no.esquerda = self._inserir_recursivo(no.esquerda, id, valor, dado_extra)
        elif id > no.id:
            no.direita = self._inserir_recursivo(no.direita, id, valor, dado_extra)
        else:
            return no # Chaves duplicadas não permitidas

        no.altura = 1 + max(self.obter_altura_no(no.esquerda), self.obter_altura_no(no.direita))

        balanceamento = self.obter_balanceamento(no)

        # Caso Esquerda Esquerda
        if balanceamento > 1 and id < no.esquerda.id:
            return self.rotacionar_direita(no)

        # Caso Direita Direita
        if balanceamento < -1 and id > no.direita.id:
            return self.rotacionar_esquerda(no)

        # Caso Esquerda Direita
        if balanceamento > 1 and id > no.esquerda.id:
            no.esquerda = self.rotacionar_esquerda(no.esquerda)
            return self.rotacionar_direita(no)

        # Caso Direita Esquerda
        if balanceamento < -1 and id < no.direita.id:
            no.direita = self.rotacionar_direita(no.direita)
            return self.rotacionar_esquerda(no)

        return no

    def buscar(self, id):
        """
        Função PÚBLICA: Busca um nó pelo ID.
        Retorna o nó encontrado e o número de comparações feitas.
        """
        self.comparacoes = 0
        return self._buscar_recursivo(self.raiz, id)

    def _buscar_recursivo(self, no, id):
        """
        Função PRIVADA: Navega pela árvore (Busca Binária).
        - Se ID procurado == ID do nó: Achou!
        - Se ID procurado < ID do nó: Vai para a esquerda.
        - Se ID procurado > ID do nó: Vai para a direita.
        """
        if no is None:
            return None, self.comparacoes
        
        self.comparacoes += 1
        if id == no.id:
            return no, self.comparacoes
        elif id < no.id:
            return self._buscar_recursivo(no.esquerda, id)
        else:
            return self._buscar_recursivo(no.direita, id)

    def remover(self, id):
        """
        Função PÚBLICA: Remove um nó pelo ID.
        Assim como a inserção, ela chama a recursiva e atualiza a raiz.
        """
        self.comparacoes = 0
        self.raiz = self._remover_recursivo(self.raiz, id)
        return self.comparacoes

    def _remover_recursivo(self, no, id):
        """
        Função PRIVADA: Remove e rebalanceia.
        
        Passo 1: Achar o nó (igual na busca).
        Passo 2: Remover (3 casos):
            - Nó folha (sem filhos): Só apaga.
            - 1 Filho: O filho sobe para o lugar do pai.
            - 2 Filhos: Pega o menor valor da direita (sucessor), coloca no lugar e apaga o sucessor antigo.
        Passo 3: Rebalancear (A mágica da AVL):
            - Recalcula altura.
            - Verifica se desbalanceou.
            - Aplica rotações se necessário.
        """
        if not no:
            return no

        self.comparacoes += 1
        if id < no.id:
            no.esquerda = self._remover_recursivo(no.esquerda, id)
        elif id > no.id:
            no.direita = self._remover_recursivo(no.direita, id)
        else:
            # Achou o nó para remover!
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            
            # Caso com 2 filhos: Pega o sucessor (menor da direita)
            temp = self._no_valor_minimo(no.direita)
            no.id = temp.id
            no.valor = temp.valor
            no.direita = self._remover_recursivo(no.direita, temp.id)

        if no is None:
            return no

        # Atualiza altura
        no.altura = 1 + max(self.obter_altura_no(no.esquerda), self.obter_altura_no(no.direita))
        balanceamento = self.obter_balanceamento(no)

        # Rebalanceamento (Rotações)
        # Caso Esquerda Esquerda
        if balanceamento > 1 and self.obter_balanceamento(no.esquerda) >= 0:
            return self.rotacionar_direita(no)

        # Caso Esquerda Direita
        if balanceamento > 1 and self.obter_balanceamento(no.esquerda) < 0:
            no.esquerda = self.rotacionar_esquerda(no.esquerda)
            return self.rotacionar_direita(no)

        # Caso Direita Direita
        if balanceamento < -1 and self.obter_balanceamento(no.direita) <= 0:
            return self.rotacionar_esquerda(no)

        # Caso Direita Esquerda
        if balanceamento < -1 and self.obter_balanceamento(no.direita) > 0:
            no.direita = self.rotacionar_direita(no.direita)
            return self.rotacionar_esquerda(no)

        return no

    def _no_valor_minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    # Métricas
    def obter_altura(self):
        return self.obter_altura_no(self.raiz)

    def contar_nos(self):
        return self._contar_nos_recursivo(self.raiz)

    def _contar_nos_recursivo(self, no):
        if no is None:
            return 0
        return 1 + self._contar_nos_recursivo(no.esquerda) + self._contar_nos_recursivo(no.direita)
    
    def obter_contagem_rotacoes(self):
        return self.rotacoes

    # Travessias
    def percurso_em_ordem(self):
        resultado = []
        self._em_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _em_ordem_recursivo(self, no, resultado):
        if no:
            self._em_ordem_recursivo(no.esquerda, resultado)
            resultado.append((no.id, no.valor))
            self._em_ordem_recursivo(no.direita, resultado)
    
    def percurso_pre_ordem(self):
        resultado = []
        self._pre_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _pre_ordem_recursivo(self, no, resultado):
        if no:
            resultado.append((no.id, no.valor))
            self._pre_ordem_recursivo(no.esquerda, resultado)
            self._pre_ordem_recursivo(no.direita, resultado)

    def percurso_pos_ordem(self):
        resultado = []
        self._pos_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _pos_ordem_recursivo(self, no, resultado):
        if no:
            self._pos_ordem_recursivo(no.esquerda, resultado)
            self._pos_ordem_recursivo(no.direita, resultado)
            resultado.append((no.id, no.valor))
