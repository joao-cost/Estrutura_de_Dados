# 🌲 Comparação de Árvores de Busca (BST, AVL, Rubro-Negra)

Este projeto implementa e compara o desempenho de três estruturas de dados fundamentais:
*   **BST** (Binary Search Tree)
*   **AVL** (Adelson-Velsky and Landis)
*   **Rubro-Negra** (Red-Black Tree)

O projeto inclui uma **interface visual interativa** e scripts de **benchmark** para análise de complexidade.

---

## ⚠️ Aviso Importante: Versão do Python

**NÃO USE PYTHON 3.14 (VERSÕES ALPHA/BETA).**

Devido a incompatibilidades com bibliotecas gráficas (`altair`/`streamlit`), este projeto requer uma versão estável do Python.
*   ✅ **Recomendado:** Python **3.10**, **3.11**, **3.12** ou **3.13**.
*   ❌ **Evite:** Python 3.14+ (Causa erro de `typing.ParamSpec`).

---

## 🛠️ Pré-requisitos

### 1. Python
Certifique-se de ter o Python instalado. Verifique a versão no terminal:
```bash
python --version
```

### 2. Graphviz (Opcional/Recomendado)
O **Streamlit** geralmente consegue desenhar os gráficos sem precisar instalar o software Graphviz no sistema (ele faz isso no navegador).
Porém, se os gráficos não aparecerem ou der erro de "ExecutableNotFound", instale o software:

*   **Windows:** [Baixar Instalador](https://graphviz.org/download/)
*   **Linux:** `sudo apt-get install graphviz`

---

## 🚀 Instalação (Passo a Passo)

Siga estes passos para configurar o ambiente no seu computador:

### 1. Criar um Ambiente Virtual (.venv)
Isso isola as bibliotecas do projeto para não bagunçar seu Python global.

**No Windows:**
```powershell
# Abra o terminal na pasta do projeto e rode:
python -m venv .venv
```

**No Linux/Mac:**
```bash
python3 -m venv .venv
```

### 2. Ativar o Ambiente Virtual
Você precisa ativar o ambiente antes de instalar as coisas.

**No Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate
```
*(Se der erro de permissão, rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` antes)*

**No Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**No Linux/Mac:**
```bash
source .venv/bin/activate
```
*Você saberá que funcionou se aparecer um `(.venv)` no começo da linha do terminal.*

### 3. Instalar Dependências
Com o venv ativado, instale as bibliotecas listadas no `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como Rodar

### 1. Interface Visual (Playground e Slides)
Para abrir a aplicação interativa no seu navegador:

```bash
streamlit run src/app.py
```

### 2. Benchmark (Teste de Desempenho)
Para rodar os testes de tempo e gerar o relatório CSV:

```bash
python src/main.py
```

---

## 📂 Estrutura do Projeto

*   `src/`: Código fonte (implementações das árvores e app).
*   `report/`: Onde os resultados dos testes (CSV) são salvos.
*   `requirements.txt`: Lista de bibliotecas necessárias.

---

**Desenvolvido para a disciplina de Estrutura de Dados.**
