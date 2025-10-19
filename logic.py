# --- logic.py ---

# Responsabilidade: Lógica de negócio (CRUD - Create, Read, Update, Delete).
# Importa apenas o necessário do módulo 'database'.

from database import Tarefa

# --- Funções de Gestão de Tarefas (Lógica da Aplicação) ---

def adicionar_tarefa(nome_tarefa):
    try:
        Tarefa.create(
            nome=nome_tarefa,
            estado='Pendente'
        )
        print(f'Tarefa {nome_tarefa} adicionada com sucesso!')

    except Exception as e:
        print(f'Erro ao adicionar tarefa: {e}')


def deletar_tarefa(id_tarefa):
    try:
        tarefa_obj = Tarefa.get_or_none(Tarefa.id == id_tarefa)
        
        if tarefa_obj:
            tarefa_obj.delete_instance()
            print(f'Tarefa com id [{id_tarefa}] deletada com sucesso!')
        else:
            print(f'Não foi possível encontrar a tarefa com id [{id_tarefa}]')

    except Exception as e:
        print(f"Erro ao deletar tarefa: {e}")


def visualizar_tarefas():
    tarefas = Tarefa.select().order_by(Tarefa.estado, Tarefa.id)

    if not tarefas.exists():
        print('\nNão há tarefas registradas!')
        return
    
    print('\n--- Lista de Tarefas ---')
    for tarefa in tarefas:
        print(tarefa)
    print('-'*25)


def concluir_tarefa(id_tarefa):
    try:

        tarefa_obj = Tarefa.get_or_none(Tarefa.id == id_tarefa)
        if tarefa_obj and tarefa_obj.estado == 'Pendente':
            tarefa_obj.estado = 'Concluída'
            tarefa_obj.save()
            print(f'Tarefa com id [{id_tarefa}] concluída!')
        elif tarefa_obj:
            print(f'A tarefa com id [{id_tarefa}] já havia sido concluída.')
        else:
            print(f'Tarefa com id [{id_tarefa}] não foi encontrada.')

    except Exception as e:
        print(f'Erro ao concluir tarefa: {e}')