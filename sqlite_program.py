import sqlite3
import os # Módulo para verificar se o ficheiro existe (opcional, mas útil)

# --- Documentação e Etapa 1: Conexão com a Base de Dados ---

def conectar_db(nome_db="tarefas.db"):
    """
    Estabelece a conexão com a base de dados SQLite. 
    Se o ficheiro da base de dados não existir, ele é criado.
    
    Parâmetros:
    - nome_db (str): O nome do ficheiro da base de dados (padrão: 'tarefas.db').
    
    Retorna:
    - sqlite3.Connection: O objeto de conexão ou None se houver um erro.
    """
    try:
        # A função connect() cria a base de dados se não existir.
        conn = sqlite3.connect(nome_db)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar à base de dados: {e}")
        return None

# --- Documentação e Etapa 2: Criação da Tabela ---

def criar_tabela(conn):
    """
    Cria a tabela 'tarefas' na base de dados se esta não existir.
    
    Parâmetros:
    - conn (sqlite3.Connection): O objeto de conexão com a base de dados.
    """
    sql_criar_tabela = """
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        estado TEXT NOT NULL
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_criar_tabela)
        # Não precisamos de conn.commit() para CREATE TABLE, mas é boa prática.
        conn.commit() 
        print("Tabela 'tarefas' verificada/criada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")

# --- Documentação e Etapa 3: Adicionar Tarefa (CREATE) ---

def adicionar_tarefa(conn, nome_tarefa):
    """
    Insere uma nova tarefa na base de dados com o estado inicial 'Pendente'.
    
    Parâmetros:
    - conn (sqlite3.Connection): O objeto de conexão.
    - nome_tarefa (str): A descrição da tarefa a ser adicionada.
    """
    sql_inserir = """
    INSERT INTO tarefas (nome, estado) 
    VALUES (?, 'Pendente');
    """
    try:
        cursor = conn.cursor()
        # O '?' é um placeholder seguro para evitar ataques de injeção SQL.
        cursor.execute(sql_inserir, (nome_tarefa,))
        conn.commit() # Confirma a transação, guardando os dados de forma permanente.
        print(f"Tarefa '{nome_tarefa}' adicionada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao adicionar tarefa: {e}")

# --- Documentação e Etapa 4: Deletar Tarefas (DELETE) ---

def deletar_tarefa(conn, id_tarefa):

    sql_deletar = """
    DELETE FROM tarefas
    WHERE id = ?;
    """

    try: 
        cursor = conn.cursor()
        cursor.execute(sql_deletar, (id_tarefa,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Tarefa de id {id_tarefa} deletada com sucesso!")
        else:
            print(f"Tarefa com id {id_tarefa} não encontrada!")

    except sqlite3.Error as e:
        print(f"Erro ao deletar tarefa: {e}")
        
# --- Documentação e Etapa 5: Visualizar Tarefas (READ) ---

def ver_tarefas(conn):
    """
    Seleciona e exibe todas as tarefas da base de dados.
    
    Parâmetros:
    - conn (sqlite3.Connection): O objeto de conexão.
    """
    sql_selecionar = "SELECT id, nome, estado FROM tarefas ORDER BY estado, id;"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_selecionar)
        tarefas = cursor.fetchall() # Obtém todos os resultados da query.
        
        if not tarefas:
            print("\nNão há tarefas registadas.")
            return

        print("\n--- Lista de Tarefas ---")
        for tarefa in tarefas:
            id_t, nome_t, estado_t = tarefa
            # Formatação para melhor visualização
            print(f"[{id_t}] - {nome_t} ({estado_t})")
        print("------------------------")

    except sqlite3.Error as e:
        print(f"Erro ao visualizar tarefas: {e}")

# --- Documentação e Etapa 6: Concluir Tarefa (UPDATE) ---

def concluir_tarefa(conn, id_tarefa):
    """
    Atualiza o estado de uma tarefa específica para 'Concluída'.
    
    Parâmetros:
    - conn (sqlite3.Connection): O objeto de conexão.
    - id_tarefa (int): O ID da tarefa a ser atualizada.
    """
    sql_atualizar = """
    UPDATE tarefas
    SET estado = 'Concluída'
    WHERE id = ? AND estado = 'Pendente';
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_atualizar, (id_tarefa,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Tarefa com ID {id_tarefa} marcada como Concluída!")
        else:
            print(f"Tarefa com ID {id_tarefa} não encontrada ou já estava Concluída.")

    except sqlite3.Error as e:
        print(f"Erro ao concluir tarefa: {e}")


# --- Documentação e Etapa 7: Menu Principal (Interface) ---

def menu_principal():
    """
    Apresenta o menu ao utilizador e gere a lógica da aplicação.
    """
    # 1. Conexão e Inicialização
    conn = conectar_db()
    if conn is None:
        return # Sai se não conseguir conectar
    
    # 2. Criação da Tabela
    criar_tabela(conn)

    while True:
        print("\n=== GESTÃO DE TAREFAS (SQLite) ===")
        print("1. Adicionar nova tarefa")
        print("2. Excluir Tarefa")
        print("3. Ver todas as tarefas")
        print("4. Concluir uma tarefa")
        print("5. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            nome = input("Descrição da nova tarefa: ")
            if nome:
                adicionar_tarefa(conn, nome)
            else:
                print("A descrição não pode ser vazia.")
                
        elif escolha == '2':
            ver_tarefas(conn)

            try:
                id_t = int(input("Digite o id da tarefa que irá deletar: "))
                deletar_tarefa(conn, id_t)
            except ValueError:
                print("ID inválido. Digite um número válido.")

        elif escolha == '3':
            ver_tarefas(conn)
            
        elif escolha == '4':
            ver_tarefas(conn) # Mostrar IDs antes de pedir
            try:
                id_t = int(input("Digite o ID da tarefa a concluir: "))
                concluir_tarefa(conn, id_t)
            except ValueError:
                print("ID inválido. Por favor, digite um número válido.")
                
        elif escolha == '5':
            print("A fechar a aplicação e a guardar alterações. Até logo!")

            conn.close() # Fecha a conexão com a base de dados
            break
            
        else:
            print("Opção inválida. Tente novamente.")

# Execução do Programa
if __name__ == "__main__": # __main__ funciona como um construtor
    menu_principal()