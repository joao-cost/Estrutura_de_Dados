class No:
    def __init__(self, id, valor, dado_extra=None):
        self.id = id
        self.valor = valor
        self.dado_extra = dado_extra
        self.esquerda = None
        self.direita = None

class BST:
    def __init__(self):
        self.raiz = None
        self.comparacoes = 0

    def inserir(self, id, valor, dado_extra=None):
        self.comparacoes = 0
        if self.raiz is None:
            self.raiz = No(id, valor, dado_extra)
        else:
            self._inserir_recursivo(self.raiz, id, valor, dado_extra)
        return self.comparacoes

    def _inserir_recursivo(self, no, id, valor, dado_extra):
        self.comparacoes += 1
        if id < no.id:
            if no.esquerda is None:
                no.esquerda = No(id, valor, dado_extra)
            else:
                self._inserir_recursivo(no.esquerda, id, valor, dado_extra)
        elif id > no.id:
            if no.direita is None:
                no.direita = No(id, valor, dado_extra)
            else:
                self._inserir_recursivo(no.direita, id, valor, dado_extra)
        # IDs duplicados são ignorados

    def buscar(self, id):
        self.comparacoes = 0
        return self._buscar_recursivo(self.raiz, id)

    def _buscar_recursivo(self, no, id):
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
        self.comparacoes = 0
        self.raiz = self._remover_recursivo(self.raiz, id)
        return self.comparacoes

    def _remover_recursivo(self, no, id):
        if no is None:
            return None

        self.comparacoes += 1
        if id < no.id:
            no.esquerda = self._remover_recursivo(no.esquerda, id)
        elif id > no.id:
            no.direita = self._remover_recursivo(no.direita, id)
        else:
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda

            temp = self._no_valor_minimo(no.direita)
            no.id = temp.id
            no.valor = temp.valor
            no.direita = self._remover_recursivo(no.direita, temp.id)
        
        return no

    def _no_valor_minimo(self, no):
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    # Métricas
    def obter_altura(self):
        return self._obter_altura_recursivo(self.raiz)

    def _obter_altura_recursivo(self, no):
        if no is None:
            return 0
        return 1 + max(self._obter_altura_recursivo(no.esquerda), self._obter_altura_recursivo(no.direita))

    def contar_nos(self):
        return self._contar_nos_recursivo(self.raiz)

    def _contar_nos_recursivo(self, no):
        if no is None:
            return 0
        return 1 + self._contar_nos_recursivo(no.esquerda) + self._contar_nos_recursivo(no.direita)

    def obter_contagem_rotacoes(self):
        return 0 # BST não tem rotações

    # Travessias (Percursos)
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
