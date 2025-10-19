# --- database.py ---

# Responsabilidade: Definição da ligação com o banco e dos modelos ORM.

from peewee import *

banco = SqliteDatabase('tarefas_orm.db')


# --- Definição dos Modelos ORM (Tabelas) ---

class BaseModel(Model):
    class Meta:
        database = banco

class Tarefa(BaseModel):
    id = AutoField()
    nome = CharField()
    estado = CharField(default='Pendente')

    def __str__(self):
        return f"[{self.id}] - {self.nome} ({self.estado})"
    

# --- Função de Inicialização ---

def inicializar_banco():
    banco.connect(reuse_if_open=True) # reuse_if_open evita erros
    banco.create_tables([Tarefa])
    print("Base de dados ORM e tabela 'Tarefa' inicializadas.")