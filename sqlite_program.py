# --- ETAPA 1 - importações ---

from peewee import *

# --- ETAPA 2 - Configuração da Base de Dados ---

banco = SqliteDatabase('tarefas_orm.db')

# --- ETAPA 3 - Definição dos Modelos ORM (Tabelas) ---

class BaseModel(Model):
    class Meta:
        database = banco

class Tarefa(BaseModel):
    id = AutoField()
    nome = CharField()
    estado = CharField(default='Pendente')

    def __str__(self):
        return f"[{self.id}] - {self.nome} ({self.estado})"

# --- ETAPA 4 - Funções de Gestão de Tarefas (Lógica da Aplicação) ---

def inicializar_banco():
    banco.connect()
    banco.create_tables([Tarefa])

    print("Base de dados ORM e tabela 'Tarefa' inicializadas.")


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

# --- ETAPA 5 - Interface do Utilizador (Menu Principal) ---

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
                id_t = int(input('Digite o id da tarefa a concluir: '))
                try:
                    concluir_tarefa(id_t)
                except ValueError:
                    print('Id inválido. Por favor, digite um número!')
            
            case 4:
                visualizar_tarefas()
                id_t = int(input('Digite o id da tarefa a deletar: '))
                try:
                    deletar_tarefa(id_t)

                except ValueError:
                    print('Id inválido. Por favor, digite um número!')

            case 5:
                print('Fechando a aplicação... Até logo ;)')
                banco.close()
                break

            case _:
                print('Opção inválida! Tente novamente.')

# --- ETAPA 6 - Ponto de Entrada da Aplicação ---

if __name__ == "__main__":
    menu_principal()