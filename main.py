# --- main.py ---

# Responsabilidade: Ponto de entrada da aplicação e interface do utilizador (menu).

# Importa as funções de inicialização e a variável 'banco' (para fechar)

from database import inicializar_banco, banco


# Importação das funções de lógica de negócio

from logic import (
    adicionar_tarefa, 
    deletar_tarefa, 
    visualizar_tarefas, 
    concluir_tarefa
)


# --- Interface do Utilizador (Menu Principal) ---

def menu_principal():
    inicializar_banco()

    while True:
        print("\n=== GESTÃO DE TAREFAS ===")
        print("1. Adicionar nova tarefa")
        print("2. Ver todas as tarefas")
        print("3. Concluir uma tarefa")
        print("4. Deletar uma tarefa")
        print("5. Sair")

        try: 
            escolha = int(input('Escolha uma opção: '))

        except ValueError:
            print('Opção inválida. Digite um número!')
            continue
        
        match escolha:
            case 1:
                desc_tarefa = str(input('Escreva a descrição da tarefa: '))
                if desc_tarefa:
                    adicionar_tarefa(desc_tarefa)
                else:
                    print("A descrição não pode ser vazia.")

            case 2:
                visualizar_tarefas()
            
            case 3:
                visualizar_tarefas()
                try:
                    id_t = int(input('Digite o id da tarefa a concluir: '))
                    concluir_tarefa(id_t)
                except ValueError:
                    print('Id inválido. Por favor, digite um número!')
                    continue

            case 4:
                visualizar_tarefas()
                try:
                    id_t = int(input('Digite o id da tarefa a deletar: '))
                    deletar_tarefa(id_t)

                except ValueError:
                    print('Id inválido. Por favor, digite um número!')
                    continue

            case 5:
                print('Fechando a aplicação... Até logo ;)')
                banco.close()
                break

            case _:
                print('Opção inválida! Tente novamente.')


# --- Ponto de Entrada da Aplicação ---

if __name__ == "__main__":
    menu_principal()