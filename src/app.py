import streamlit as st
import graphviz
from bst import BST
from avl import ArvoreAVL
from rbt import ArvoreRubroNegra
import random
import string
from utils import gerar_dados_aleatorios, gerar_dados_ordenados, gerar_string_aleatoria, gerar_valor_numerico
import pandas as pd
import time

st.set_page_config(page_title="Estruturas de Dados - Apresentação", layout="wide")

# --- BARRA LATERAL (SIDEBAR) ---
# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # Título Condicional (Baseado no estado anterior ou padrão)
    modo_atual = st.session_state.get("modo_selecionado", "Apresentação (Slides)")
    if modo_atual == "Apresentação (Slides)":
        st.title("🌲 Comparação de Árvores")
        st.markdown("---")

    st.header("🎮 Painel de Controle")
    
    # Seleção de Modo
    modo = st.radio("Modo de Acesso:", ["Apresentação (Slides)", "Playground Interativo"], key="modo_selecionado")
    st.markdown("---")

    # Controles do Playground (Só aparecem no modo Playground)
    if modo == "Playground Interativo":
        st.subheader("🌳 Gerenciamento da Árvore")
        tipo_arvore = st.selectbox("Tipo de Estrutura:", ["BST", "AVL", "Rubro-Negra"])
        
        # Inicializar estado da sessão para árvores
        if "bst" not in st.session_state:
            st.session_state.bst = BST()
        if "avl" not in st.session_state:
            st.session_state.avl = ArvoreAVL()
        if "rbt" not in st.session_state:
            st.session_state.rbt = ArvoreRubroNegra()
        
        # Inicializar contador de ID
        if "next_id" not in st.session_state:
            st.session_state.next_id = 1

        # Selecionar a árvore atual
        if tipo_arvore == "BST":
            arvore = st.session_state.bst
        elif tipo_arvore == "AVL":
            arvore = st.session_state.avl
        else:
            arvore = st.session_state.rbt

        st.markdown("---")
        
        # Abas para Operações (Mais organizado)
        tab_add, tab_rem, tab_search, tab_view, tab_conf = st.tabs(["➕ Inserir", "➖ Remover", "🔎 Buscar", "👀 Ver", "⚙️ Config"])
        
        with tab_add:

            usar_auto_id = st.checkbox("Gerar ID Automaticamente?", value=False)
            
            with st.form("form_inserir"):
                col_id, col_val, col_extra = st.columns([1, 2, 1])
                with col_id:
                    if usar_auto_id:
                        id_inserir = st.session_state.next_id
                        st.text_input("ID (Auto)", value=str(id_inserir), disabled=True)
                    else:
                        id_inserir = st.number_input("ID (Chave)", value=0, step=1)
                with col_val:
                    valor_inserir = st.text_input("Valor (Texto/Num)", placeholder="Ex: 100")
                with col_extra:
                    extra_inserir = st.text_input("Categoria (Opcional)", placeholder="Ex: VIP")
                
                btn_inserir = st.form_submit_button("Adicionar Nó", type="primary")
                
                if btn_inserir:
                    # Lógica para valor padrão se vazio
                    valor_final = valor_inserir if valor_inserir.strip() else gerar_valor_numerico()
                    extra_final = extra_inserir if extra_inserir.strip() else None
                    
                    arvore.inserir(int(id_inserir), valor_final, extra_final)
                    
                    # Incrementar ID se foi automático
                    if usar_auto_id:
                        st.session_state.next_id += 1

                    msg_extra = f" | Cat: {extra_final}" if extra_final else ""
                    st.success(f"✅ Nó {id_inserir} ({valor_final}{msg_extra}) inserido!")
                    st.rerun()

        with tab_rem:
            with st.form("form_remover"):
                id_remover = st.number_input("ID para Remover", value=0, step=1)
                btn_remover = st.form_submit_button("Remover Nó", type="primary")
                
                if btn_remover:
                    arvore.remover(int(id_remover))
                    st.warning(f"🗑️ Nó {id_remover} removido!")
                    st.rerun()

        with tab_search:
            tipo_busca = st.radio("Tipo de Busca:", ["Por ID (Chave)", "Por Valor (Texto)"], horizontal=True)
            
            with st.form("form_buscar"):
                if tipo_busca == "Por ID (Chave)":
                    id_buscar = st.number_input("ID para Buscar", value=0, step=1)
                    val_buscar = None
                else:
                    val_buscar = st.text_input("Valor para Buscar")
                    id_buscar = None
                
                btn_buscar = st.form_submit_button("Buscar", type="primary")
                
                if btn_buscar:
                    if tipo_busca == "Por ID (Chave)":
                        resultado = arvore.buscar(int(id_buscar))
                        
                        # Tratamento para retorno (nó, comparações) ou apenas nó
                        no_encontrado = None
                        if isinstance(resultado, tuple):
                            no_encontrado = resultado[0]
                        else:
                            no_encontrado = resultado

                        if no_encontrado:
                            dado_extra_str = f" | Categoria: {no_encontrado.dado_extra}" if getattr(no_encontrado, 'dado_extra', None) else ""
                            st.success(f"✅ Encontrado! ID: {no_encontrado.id} | Valor: {no_encontrado.valor}{dado_extra_str}")
                        else:
                            st.error(f"❌ Nó com ID {id_buscar} não encontrado.")
                    else:
                        # Busca linear por valor (O(n))
                        todos_nos = arvore.percurso_em_ordem() # Retorna lista de tuplas (id, valor)
                        encontrados = [no for no in todos_nos if no[1] == val_buscar]
                        
                        if encontrados:
                            st.success(f"✅ Encontrado(s) {len(encontrados)} nó(s) com valor '{val_buscar}':")
                            for item in encontrados:
                                st.write(f"- ID: **{item[0]}**")
                        else:
                            st.error(f"❌ Nenhum nó com valor '{val_buscar}' encontrado.")
                            st.caption("Nota: A busca por valor é mais lenta (O(n)) pois a árvore é ordenada pelo ID.")

        with tab_view:
            st.markdown("**Travessias (Percursos)**")
            if st.button("Em-Ordem (In-Order)"):
                st.code(str(arvore.percurso_em_ordem()))
            if st.button("Pré-Ordem (Pre-Order)"):
                st.code(str(arvore.percurso_pre_ordem()))
            if st.button("Pós-Ordem (Post-Order)"):
                st.code(str(arvore.percurso_pos_ordem()))

        with tab_conf:
            if st.button("🧹 Limpar Árvore Atual"):
                if tipo_arvore == "BST":
                    st.session_state.bst = BST()
                elif tipo_arvore == "AVL":
                    st.session_state.avl = ArvoreAVL()
                else:
                    st.session_state.rbt = ArvoreRubroNegra()
                st.success("Árvore resetada!")
                st.rerun()

        # Métricas na Sidebar
        st.markdown("---")
        st.subheader("📊 Métricas em Tempo Real")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Altura", arvore.obter_altura())
        col_m2.metric("Nós", arvore.contar_nos())
        col_m3, col_m4 = st.columns(2)
        col_m3.metric("Rotações", arvore.obter_contagem_rotacoes())
        col_m4.metric("Comparações", arvore.comparacoes)

    elif modo == "Apresentação (Slides)":
        st.subheader("📽️ Navegação")
        
        # Inicializar índice se não existir
        if 'slide_index' not in st.session_state:
            st.session_state.slide_index = 0
            
        slides = [
            "Introdução",
            "Árvore Binária de Busca (BST)",
            "Árvore AVL",
            "Árvore Rubro-Negra",
            "Comparação e Conclusão"
        ]

        # Botões de Navegação na Sidebar
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅️ Ant.", use_container_width=True):
                if st.session_state.slide_index > 0:
                    st.session_state.slide_index -= 1
                    st.rerun()
        with col_next:
            if st.button("Prox. ➡️", use_container_width=True):
                if st.session_state.slide_index < len(slides) - 1:
                    st.session_state.slide_index += 1
                    st.rerun()
        
        # Barra de progresso e info
        st.progress((st.session_state.slide_index + 1) / len(slides))
        st.info(f"Slide {st.session_state.slide_index + 1}/{len(slides)}:\n**{slides[st.session_state.slide_index]}**")

# --- CORPO PRINCIPAL ---
if modo == "Apresentação (Slides)":
    # st.title("🌲 Comparação de Árvores de Busca") # Movido para sidebar

    
    # Controle de Slides (Lógica mantida para referência, mas controle visual movido para sidebar)
    if 'slide_index' not in st.session_state:
        st.session_state.slide_index = 0
    
    slides = [
        "Introdução",
        "Árvore Binária de Busca (BST)",
        "Árvore AVL",
        "Árvore Rubro-Negra",
        "Comparação e Conclusão"
    ]

    # Conteúdo dos Slides
    slide_atual = slides[st.session_state.slide_index]


    # Conteúdo dos Slides
    slide_atual = slides[st.session_state.slide_index]
    
    # st.markdown("---") # Removido para ganhar espaço

    if slide_atual == "Introdução":
        st.header("Estruturas de Dados Avançadas")
        st.subheader("Análise Comparativa: BST vs AVL vs Rubro-Negra")
        
        with st.expander("👥 Integrantes do Grupo", expanded=True):
            st.markdown("""
            *   **Fellipe Melhoranca B. Tomasella**
            *   **Inglid Pablina de A. Sandeski**
            *   **João Vitor de S. Costa**
            *   **Vitor Linsbinski de Oliveira**
            """)

        st.markdown("""
        ### O Desafio
        Armazenar e buscar dados de forma eficiente.
        
        ### Os Competidores
        1.  **BST (Árvore Binária de Busca):** A base de tudo. Simples, mas perigosa.
        2.  **AVL:** A perfeccionista. Balanceamento estrito.
        3.  **Rubro-Negra:** A pragmática. Balanceamento eficiente.
        
        ### Objetivo do Trabalho
        Implementar do zero (Python), testar e comparar o desempenho dessas estruturas.
        """)

    elif slide_atual == "Árvore Binária de Busca (BST)":
        st.header("1. Árvore Binária de Busca (BST)")
        
        tab_teoria, tab_codigo = st.tabs(["📘 Teoria", "💻 Código (Implementação)"])
        
        with tab_teoria:
            col_txt, col_img = st.columns(2)
            with col_txt:
                st.markdown("""
                **Introdução Teórica:**
                A BST é a estrutura fundamental. A regra é simples: para qualquer nó, todos os valores à **esquerda** são menores e todos à **direita** são maiores.
                
                **Principais Funções:**
                *   `inserir(id, valor)`: Percorre a árvore comparando IDs até achar uma posição vazia.
                *   `buscar(id)`: Navegação binária (Esquerda/Direita).
                *   `remover(id)`: Mais complexa, exige lidar com 3 casos (sem filhos, 1 filho, 2 filhos).
                
                **Análise de Complexidade:**
                *   **Melhor/Médio:** O(log n) - Árvore equilibrada.
                *   **Pior:** O(n) - Árvore degenerada (lista ligada).
                """)
            with col_img:

                st.warning("Visualização do Pior Caso da BST:")
                st.markdown("Se inserirmos dados ordenados (1, 2, 3, 4, 5), a BST vira uma **Lista Ligada**.")
                dot = graphviz.Digraph()
                dot.attr(rankdir='TB')
                dot.node('1', '1')
                dot.node('2', '2')
                dot.node('3', '3')
                dot.node('4', '4')
                dot.node('5', '5')
                dot.edge('1', '2')
                dot.edge('2', '3')
                dot.edge('3', '4')
                dot.edge('4', '5')
                st.graphviz_chart(dot)

        with tab_codigo:
            st.markdown("### Implementação Base")
            st.markdown("A lógica de inserção é recursiva e simples:")
            st.code("""
    def _inserir_recursivo(self, no, novo_no):
        self.comparacoes += 1
        if novo_no.id < no.id:
            if no.esquerda is None:
                no.esquerda = novo_no
            else:
                self._inserir_recursivo(no.esquerda, novo_no)
        else:
            if no.direita is None:
                no.direita = novo_no
            else:
                self._inserir_recursivo(no.direita, novo_no)
            """, language="python")

    elif slide_atual == "Árvore AVL":
        st.header("2. Árvore AVL (Adelson-Velsky e Landis)")
        
        tab_teoria, tab_codigo = st.tabs(["📘 Teoria", "💻 Código (Diferenciais)"])
        
        with tab_teoria:
            col_txt, col_img = st.columns(2)
            with col_txt:
                st.markdown("""
                **Introdução Teórica:**
                A AVL (criada por Adelson-Velsky e Landis em 1962) foi a primeira árvore binária de busca auto-balanceável.
                
                **O Conceito de Equilíbrio:**
                *   **Fator de Balanceamento (FB):** Para cada nó, calculamos `Altura(Esq) - Altura(Dir)`.
                *   **Regra:** O FB deve ser sempre **-1, 0 ou +1**.
                *   Se o FB for **+2 ou -2**, a árvore está desbalanceada e precisa de correção.
                
                **As 4 Rotações de Correção:**
                1.  **Rotação Simples à Direita (LL):** Quando o desequilíbrio é na esquerda-esquerda.
                2.  **Rotação Simples à Esquerda (RR):** Quando o desequilíbrio é na direita-direita.
                3.  **Rotação Dupla à Direita (LR):** Esquerda depois Direita.
                4.  **Rotação Dupla à Esquerda (RL):** Direita depois Esquerda.
                
                **Custo:**
                Mantém a altura em **O(log n)**, garantindo buscas rápidas, mas as rotações na inserção/remoção têm um pequeno custo constante extra.
                """)
            with col_img:
                st.success("Exemplo de Balanceamento:")
                dot = graphviz.Digraph()
                dot.node('B', 'B (Raiz)')
                dot.node('A', 'A')
                dot.node('C', 'C')
                dot.edge('B', 'A')
                dot.edge('B', 'C')
                st.graphviz_chart(dot)

        with tab_codigo:
            st.markdown("### O Segredo: Rotações")
            st.markdown("Diferente da BST, a AVL se 'conserta' girando nós:")
            st.code("""
    def _rotacionar_direita(self, z):
        self.rotacoes += 1
        y = z.esquerda
        T3 = y.direita

        # Realizar rotação
        y.direita = z
        z.esquerda = T3

        # Atualizar alturas
        z.altura = 1 + max(self.obter_altura_no(z.esquerda), self.obter_altura_no(z.direita))
        y.altura = 1 + max(self.obter_altura_no(y.esquerda), self.obter_altura_no(y.direita))

        return y
            """, language="python")

    elif slide_atual == "Árvore Rubro-Negra":
        st.header("3. Árvore Rubro-Negra (Red-Black)")
        
        tab_teoria, tab_codigo = st.tabs(["📘 Teoria", "💻 Código (Diferenciais)"])
        
        with tab_teoria:
            col_txt, col_img = st.columns(2)
            with col_txt:
                st.markdown("""
                **Introdução Teórica:**
                A Árvore Rubro-Negra (Red-Black Tree) é uma estrutura mais pragmática. Ela não busca o equilíbrio perfeito (como a AVL), mas um equilíbrio "bom o suficiente" para garantir O(log n).
                
                **Como funciona?**
                Cada nó tem uma cor (🔴 ou ⚫). As regras de coloração garantem que o caminho mais longo da raiz até uma folha não seja mais que o dobro do caminho mais curto.
                
                **As 5 Propriedades (Regras):**
                1.  Todo nó é **Vermelho** ou **Preto**.
                2.  A **Raiz** é sempre **Preta**.
                3.  Todas as folhas (NIL) são **Pretas**.
                4.  Se um nó é **Vermelho**, seus filhos DEVEM ser **Pretos** (não pode haver vermelhos consecutivos).
                5.  Todo caminho de um nó até suas folhas descendentes deve ter o mesmo número de nós **Pretos**.
                
                **Vantagem:**
                Exige menos rotações que a AVL nas operações de escrita (inserção/remoção), sendo muito usada em bancos de dados e sistemas de arquivos.
                """)
            with col_img:
                st.error("Visualização das Cores:")
                dot = graphviz.Digraph()
                dot.node('10', '10', color='black', fontcolor='black')
                dot.node('5', '5', color='red', fontcolor='red')
                dot.node('15', '15', color='black', fontcolor='black')
                dot.edge('10', '5')
                dot.edge('10', '15')
                st.graphviz_chart(dot)

        with tab_codigo:
            st.markdown("### O Conserto (Fixup)")
            st.markdown("Após inserir (sempre Vermelho), verificamos se quebramos regras e recolorimos/rotacionamos:")
            st.code("""
    def _consertar_insercao(self, k):
        while k.pai.cor == "VERMELHO":
            if k.pai == k.pai.pai.direita:
                u = k.pai.pai.esquerda # Tio
                if u.cor == "VERMELHO":
                    # Caso 1: Tio Vermelho -> Recolorir
                    u.cor = "PRETO"
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    k = k.pai.pai
                else:
                    # Caso 2/3: Tio Preto -> Rotações
                    if k == k.pai.direita:
                        k = k.pai
                        self._rotacionar_esquerda(k)
                    k.pai.cor = "PRETO"
                    k.pai.pai.cor = "VERMELHO"
                    self._rotacionar_direita(k.pai.pai)
            # ... (Espelho para o outro lado)
        self.raiz.cor = "PRETO"
            """, language="python")

    elif slide_atual == "Comparação e Conclusão":
        st.header("4. Comparação Final e Resultados")
        
        # --- ÁREA DE CONTROLE DO BENCHMARK ---
        with st.expander("⚙️ Painel de Controle do Benchmark (Ao Vivo)", expanded=False):
            st.write("Execute novos testes ou limpe os dados existentes.")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                tamanhos_teste = st.multiselect(
                    "Tamanhos para Testar:", 
                    options=[100, 500, 1000, 2000, 5000, 10000],
                    default=[100, 1000]
                )
                if st.button("🚀 Rodar Benchmark Agora"):
                    if not tamanhos_teste:
                        st.error("Selecione pelo menos um tamanho.")
                    else:
                        with st.spinner(f"Rodando testes para {tamanhos_teste}... Isso pode demorar um pouco."):
                            # Importar aqui para evitar problemas de recarregamento
                            from main import executar_benchmark
                            try:
                                executar_benchmark(tamanhos_teste)
                                st.success("Benchmark finalizado! Recarregando dados...")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Erro ao rodar benchmark: {e}")

            with col_b2:
                st.write("Gestão de Arquivos")
                if st.button("🗑️ Apagar Resultados Antigos"):
                    try:
                        import os
                        if os.path.exists("report/resultados_benchmark.csv"):
                            os.remove("report/resultados_benchmark.csv")
                            st.success("Dados apagados!")
                            st.rerun()
                        elif os.path.exists("../report/resultados_benchmark.csv"):
                            os.remove("../report/resultados_benchmark.csv")
                            st.success("Dados apagados!")
                            st.rerun()
                        else:
                            st.warning("Nenhum arquivo encontrado para apagar.")
                    except Exception as e:
                        st.error(f"Erro ao apagar: {e}")

        st.markdown("---")
        
        # Tentar carregar o CSV
        try:
            # Tenta caminhos diferentes dependendo de onde o script é executado
            caminhos = ["report/resultados_benchmark.csv", "../report/resultados_benchmark.csv", "resultados_benchmark.csv"]
            df = None
            for caminho in caminhos:
                try:
                    df = pd.read_csv(caminho)
                    break
                except FileNotFoundError:
                    continue
            
            if df is not None:
                st.success("✅ Resultados do Benchmark carregados com sucesso!")
                
                # Filtros
                tamanhos = df["Tamanho"].unique()
                tamanho_selecionado = st.selectbox("Selecione o Tamanho da Amostra:", tamanhos, index=len(tamanhos)-1)
                
                df_filtrado = df[df["Tamanho"] == tamanho_selecionado]
                
                st.markdown(f"### Desempenho para {tamanho_selecionado} elementos")
                
                # Tentar renderizar gráficos
                try:
                    # Gráficos de Tempo
                    st.subheader("⏱️ Tempo de Execução (ms)")
                    col_t1, col_t2, col_t3 = st.columns(3)
                    
                    with col_t1:
                        st.caption("Inserção")
                        st.bar_chart(df_filtrado, x="Arvore", y="Tempo Insercao (ms)", color="Tipo de Dado")
                    with col_t2:
                        st.caption("Busca")
                        st.bar_chart(df_filtrado, x="Arvore", y="Tempo Busca (ms)", color="Tipo de Dado")
                    with col_t3:
                        st.caption("Remoção")
                        st.bar_chart(df_filtrado, x="Arvore", y="Tempo Remocao (ms)", color="Tipo de Dado")

                    # Gráficos de Comparações
                    st.subheader("🔍 Comparações Médias")
                    st.bar_chart(df_filtrado, x="Arvore", y=["Comparacoes Medias Insercao", "Comparacoes Medias Busca"], color=["#FF5733", "#33FF57"])

                    # Métricas Estruturais
                    st.subheader("📏 Estrutura da Árvore")
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        st.caption("Altura Final")
                        st.bar_chart(df_filtrado, x="Arvore", y="Altura Final", color="Tipo de Dado")
                    with col_e2:
                        st.caption("Rotações (Total)")
                        st.bar_chart(df_filtrado, x="Arvore", y="Rotacoes", color="Tipo de Dado")

                except Exception as e:
                    st.error(f"Erro ao renderizar gráficos (Provável incompatibilidade de versões): {e}")
                    st.warning("⚠️ Exibindo dados brutos como fallback. Tente atualizar suas bibliotecas: `pip install -U streamlit altair typing_extensions`")
                    st.dataframe(df_filtrado)

                st.markdown("""
                > **Nota:** Observe como a altura da BST explode com dados ordenados, enquanto AVL e Rubro-Negra se mantêm estáveis.
                """)

            else:
                st.warning("⚠️ Arquivo 'resultados_benchmark.csv' não encontrado. Rode o `main.py` primeiro para gerar os dados.")
                # Fallback para tabela estática
                st.markdown("### Complexidade Teórica (Big O)")
                df_complexidade = pd.DataFrame({
                    "Operação": ["Busca (Médio)", "Busca (Pior)", "Inserção (Médio)", "Inserção (Pior)"],
                    "BST": ["O(log n)", "O(n) 💀", "O(log n)", "O(n) 💀"],
                    "AVL": ["O(log n) ⚡", "O(log n)", "O(log n)", "O(log n)"],
                    "Rubro-Negra": ["O(log n)", "O(log n)", "O(log n) 🚀", "O(log n)"]
                })
                st.table(df_complexidade)

        except Exception as e:
            st.error(f"Erro crítico ao carregar arquivo: {e}")
        
        st.markdown("""
        ### Veredito Final
        *   **BST:** Rápida e simples, mas instável.
        *   **AVL:** A rainha da busca.
        *   **Rubro-Negra:** O equilíbrio perfeito para uso geral.
        """)
        if st.button("Soltar Balões 🎉"):
            st.balloons()

# --- MODO PLAYGROUND ---
else:
    st.title(f"🌲 Playground: {tipo_arvore}")
    st.caption("Visualize e manipule a estrutura da árvore em tempo real.")



    # Função de visualização (Reutilizada)
    def obter_dot_graphviz(raiz_arvore, tipo_arvore):
        dot = graphviz.Digraph()
        dot.attr(rankdir='TB')
        
        # Verificar árvore vazia (RBT ou normal)
        if tipo_arvore == "Rubro-Negra":
            if raiz_arvore == arvore.NULO:
                 dot.node("Vazia", "Árvore Vazia", shape="plaintext")
                 return dot
        elif not raiz_arvore:
             dot.node("Vazia", "Árvore Vazia", shape="plaintext")
             return dot

        def adicionar_nos(no):
            if not no:
                return
            
            # Pular NULO na RBT
            if tipo_arvore == "Rubro-Negra" and no == arvore.NULO:
                 return

            rotulo = f"{no.id}\n({no.valor})"
            cor = "black"
            cor_fonte = "black"
            estilo = "solid"
            
            if tipo_arvore == "Rubro-Negra":
                if no.cor == "VERMELHO":
                    cor = "red"
                    cor_fonte = "red"
                    estilo = "filled"
                    fillcolor = "pink" # Melhor visualização
                else:
                    cor = "black"
                    cor_fonte = "white"
                    estilo = "filled"
                    fillcolor = "black"
            
            dot.node(str(no.id), rotulo, color=cor, fontcolor=cor_fonte, style=estilo, fillcolor=fillcolor if 'fillcolor' in locals() else "white")
            
            if no.esquerda and (tipo_arvore != "Rubro-Negra" or no.esquerda != arvore.NULO):
                dot.edge(str(no.id), str(no.esquerda.id))
                adicionar_nos(no.esquerda)
            
            if no.direita and (tipo_arvore != "Rubro-Negra" or no.direita != arvore.NULO):
                dot.edge(str(no.id), str(no.direita.id))
                adicionar_nos(no.direita)

        adicionar_nos(raiz_arvore)
        return dot

    # Exibição
    grafico = obter_dot_graphviz(arvore.raiz, tipo_arvore)
    st.graphviz_chart(grafico, use_container_width=True)

    st.markdown("---")
    st.markdown("**Legenda:**")
    if tipo_arvore == "Rubro-Negra":
        st.markdown("🔴 **Vermelho**")
        st.markdown("⚫ **Preto**")
    else:
        st.markdown("⚪ **Padrão**")
