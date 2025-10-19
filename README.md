# Gestor de Tarefas com Python e ORM (Peewee)

Este é um projeto simples de um gestor de tarefas ("To-Do List") desenvolvido em Python, com interface de linha de comando (CLI).

O principal objetivo deste projeto é demonstrar o uso de um **ORM (Object-Relational Mapper)**, especificamente a biblioteca `peewee`, para interagir com uma base de dados SQLite. Em vez de escrever comandos SQL manualmente, o ORM permite-nos manipular a base de dados usando apenas classes e objetos Python.

Este projeto faz parte do repositório `learning_database`, focado no aprendizado de diferentes tecnologias de bases de dados.

## ✨ Funcionalidades

O gestor de tarefas permite as seguintes operações básicas (CRUD):

* **Adicionar** novas tarefas (com estado padrão "Pendente").
* **Visualizar** todas as tarefas registadas, ordenadas por estado e ID.
* **Atualizar** o estado de uma tarefa para "Concluída".
* **Deletar** uma tarefa específica da base de dados.
* Interface de menu interativo e robusta, com tratamento de erros de input.

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+** (utiliza a sintaxe `match...case`)
* **Peewee** (usado como o ORM para mapear objetos Python para a base de dados)
* **SQLite** (usada como a base de dados leve, baseada em ficheiro)

## 🧩Etapas do código

* **ETAPA 1 - IMPORTAÇÕES:** Agrupa todas as bibliotecas que o teu programa precisa para funcionar (neste caso, apenas peewee).

* **ETAPA 2 - Configuração da Base de Dados:** Define a variável banco que diz ao Peewee qual o ficheiro de base de dados a utilizar.

* **ETAPA 3 - Definição dos Modelos ORM (Tabelas):** Esta é a "tradução" das tabelas da base de dados para Classes Python. É o coração do ORM.

* **ETAPA 4 - Funções de Gestão de Tarefas (Lógica da Aplicação):** Agrupa todas as tuas funções (def) que efetivamente fazem o trabalho (adicionar, apagar, ver, etc.). É a "lógica de negócio" do programa.

* **ETAPA 5 - Interface do Utilizador (Menu Principal):** Contém a função menu_principal, que é responsável por mostrar as opções ao utilizador e chamar as funções da Etapa 4.

* **ETAPA 6 - Ponto de Entrada da Aplicação:** O if __name__ == "__main__": é o que "liga" o programa, dizendo ao Python para começar por executar a função menu_principal().

## 🚀 Como Utilizar

Para executar este projeto na tua máquina local, segue estes passos:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/brianpventura/learning_database.git](https://github.com/brianpventura/learning_database.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd learning_database
    # (Ou para a sub-pasta específica deste projeto, se houver)
    ```

3.  **Instale as dependências:**
    Este projeto requer apenas a biblioteca `peewee`.
    ```bash
    pip install peewee
    ```

4.  **Execute o script:**
    (Certifica-te de que o teu ficheiro Python tem um nome, por exemplo: `gestor_orm.py`)
    ```bash
    python gestor_orm.py
    ```

5.  **Pronto!** O menu interativo será iniciado. A primeira vez que executares, um ficheiro chamado `tarefas_orm.db` será criado automaticamente no mesmo diretório para armazenar os teus dados.
