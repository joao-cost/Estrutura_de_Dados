class No:
    def __init__(self, id, valor, cor="VERMELHO"):
        self.id = id
        self.valor = valor
        self.esquerda = None
        self.direita = None
        self.pai = None
        self.cor = cor  # "VERMELHO" ou "PRETO"

class ArvoreRubroNegra:
    def __init__(self):
        self.NULO = No(0, None)
        self.NULO.cor = "PRETO"
        self.NULO.esquerda = None
        self.NULO.direita = None
        self.raiz = self.NULO
        self.comparacoes = 0
        self.rotacoes = 0

    def buscar(self, id):
        self.comparacoes = 0
        return self._buscar_recursivo(self.raiz, id)

    def _buscar_recursivo(self, no, id):
        if no == self.NULO:
            return None, self.comparacoes
        
        self.comparacoes += 1
        if id == no.id:
            return no, self.comparacoes
        elif id < no.id:
            return self._buscar_recursivo(no.esquerda, id)
        else:
            return self._buscar_recursivo(no.direita, id)

    def inserir(self, id, valor):
        self.comparacoes = 0
        no = No(id, valor)
        no.pai = None
        no.id = id
        no.esquerda = self.NULO
        no.direita = self.NULO
        no.cor = "VERMELHO"

        y = None
        x = self.raiz

        while x != self.NULO:
            y = x
            self.comparacoes += 1
            if no.id < x.id:
                x = x.esquerda
            elif no.id > x.id:
                x = x.direita
            else:
                return self.comparacoes # Duplicado

        no.pai = y
        if y == None:
            self.raiz = no
        elif no.id < y.id:
            y.esquerda = no
        else:
            y.direita = no

        if no.pai == None:
            no.cor = "PRETO"
            return self.comparacoes

        if no.pai.pai == None:
            return self.comparacoes

        self._consertar_insercao(no)
        return self.comparacoes

    def _consertar_insercao(self, k):
        while k.pai.cor == "VERMELHO":
            if k.pai == k.pai.pai.direita:
                u = k.pai.pai.esquerda
                if u.cor == "VERMELHO":
                    u.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:
                    if k == k.pai.esquerda:
                        k = k.pai
                        self._rotacionar_direita(k)
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self._rotacionar_esquerda(k.pai.pai)
            else:
                u = k.pai.pai.direita
                if u.cor == "VERMELHO":
                    u.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:
                    if k == k.pai.direita:
                        k = k.pai
                        self._rotacionar_esquerda(k)
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self._rotacionar_direita(k.pai.pai)
            if k == self.raiz:
                break
        self.raiz.cor = "PRETO"

    def _rotacionar_esquerda(self, x):
        self.rotacoes += 1
        y = x.direita
        x.direita = y.esquerda
        if y.esquerda != self.NULO:
            y.esquerda.pai = x
        y.pai = x.pai
        if x.pai == None:
            self.raiz = y
        elif x == x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y
        y.esquerda = x
        x.pai = y

    def _rotacionar_direita(self, x):
        self.rotacoes += 1
        y = x.esquerda
        x.esquerda = y.direita
        if y.direita != self.NULO:
            y.direita.pai = x
        y.pai = x.pai
        if x.pai == None:
            self.raiz = y
        elif x == x.pai.direita:
            x.pai.direita = y
        else:
            x.pai.esquerda = y
        y.direita = x
        x.pai = y

    def remover(self, id):
        self.comparacoes = 0
        no = self._encontrar_no(self.raiz, id)
        if no == self.NULO:
            return self.comparacoes
        
        self._deletar_no(no)
        return self.comparacoes

    def _encontrar_no(self, no, id):
        if no == self.NULO or id == no.id:
            return no
        
        self.comparacoes += 1
        if id < no.id:
            return self._encontrar_no(no.esquerda, id)
        return self._encontrar_no(no.direita, id)

    def _deletar_no(self, z):
        y = z
        y_cor_original = y.cor
        if z.esquerda == self.NULO:
            x = z.direita
            self._transplantar(z, z.direita)
        elif z.direita == self.NULO:
            x = z.esquerda
            self._transplantar(z, z.esquerda)
        else:
            y = self._minimo(z.direita)
            y_cor_original = y.cor
            x = y.direita
            if y.pai == z:
                x.pai = y
            else:
                self._transplantar(y, y.direita)
                y.direita = z.direita
                y.direita.pai = y

            self._transplantar(z, y)
            y.esquerda = z.esquerda
            y.esquerda.pai = y
            y.cor = z.cor
        
        if y_cor_original == "PRETO":
            self._consertar_delecao(x)

    def _transplantar(self, u, v):
        if u.pai == None:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        v.pai = u.pai

    def _minimo(self, no):
        while no.esquerda != self.NULO:
            no = no.esquerda
        return no

    def _consertar_delecao(self, x):
        while x != self.raiz and x.cor == "PRETO":
            if x == x.pai.esquerda:
                w = x.pai.direita
                if w.cor == "VERMELHO":
                    w.cor = "PRETO"
                    x.pai.cor = "VERMELHO"
                    self._rotacionar_esquerda(x.pai)
                    w = x.pai.direita
                
                if w.esquerda.cor == "PRETO" and w.direita.cor == "PRETO":
                    w.cor = "VERMELHO"
                    x = x.pai
                else:
                    if w.direita.cor == "PRETO":
                        w.esquerda.cor = "PRETO"
                        w.cor = "VERMELHO"
                        self._rotacionar_direita(w)
                        w = x.pai.direita
                    
                    w.cor = x.pai.cor
                    x.pai.cor = "PRETO"
                    w.direita.cor = "PRETO"
                    self._rotacionar_esquerda(x.pai)
                    x = self.raiz
            else:
                w = x.pai.esquerda
                if w.cor == "VERMELHO":
                    w.cor = "PRETO"
                    x.pai.cor = "VERMELHO"
                    self._rotacionar_direita(x.pai)
                    w = x.pai.esquerda
                
                if w.direita.cor == "PRETO" and w.esquerda.cor == "PRETO":
                    w.cor = "VERMELHO"
                    x = x.pai
                else:
                    if w.esquerda.cor == "PRETO":
                        w.direita.cor = "PRETO"
                        w.cor = "VERMELHO"
                        self._rotacionar_esquerda(w)
                        w = x.pai.esquerda
                    
                    w.cor = x.pai.cor
                    x.pai.cor = "PRETO"
                    w.esquerda.cor = "PRETO"
                    self._rotacionar_direita(x.pai)
                    x = self.raiz
        x.cor = "PRETO"

    # Métricas
    def obter_altura(self):
        return self._obter_altura_recursivo(self.raiz)

    def _obter_altura_recursivo(self, no):
        if no == self.NULO:
            return 0
        return 1 + max(self._obter_altura_recursivo(no.esquerda), self._obter_altura_recursivo(no.direita))

    def contar_nos(self):
        return self._contar_nos_recursivo(self.raiz)

    def _contar_nos_recursivo(self, no):
        if no == self.NULO:
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
        if no != self.NULO:
            self._em_ordem_recursivo(no.esquerda, resultado)
            resultado.append((no.id, no.valor))
            self._em_ordem_recursivo(no.direita, resultado)

    def percurso_pre_ordem(self):
        resultado = []
        self._pre_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _pre_ordem_recursivo(self, no, resultado):
        if no != self.NULO:
            resultado.append((no.id, no.valor))
            self._pre_ordem_recursivo(no.esquerda, resultado)
            self._pre_ordem_recursivo(no.direita, resultado)

    def percurso_pos_ordem(self):
        resultado = []
        self._pos_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _pos_ordem_recursivo(self, no, resultado):
        if no != self.NULO:
            self._pos_ordem_recursivo(no.esquerda, resultado)
            self._pos_ordem_recursivo(no.direita, resultado)
            resultado.append((no.id, no.valor))
