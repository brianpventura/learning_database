# --- gui.py ---
# Responsabilidade: Ponto de entrada e Interface Gráfica (GUI)

import customtkinter as ctk
from database import banco
from logic import (
    adicionar_tarefa, 
    deletar_tarefa, 
    visualizar_tarefas, 
    concluir_tarefa
)

class AppGestorTarefas(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        # --- 1. Configuração da Janela Principal ---
        self.title("Gestor de Tarefas")
        self.geometry("900x600") # Um pouco maior para o novo layout
        ctk.set_appearance_mode("system")
        
        # --- 2. Configuração do Layout (Grid) ---
        # 2 colunas: 
        # Coluna 0 (esquerda) para botões. Peso 1.
        # Coluna 1 (direita) para conteúdo. Peso 3 (mais larga).
        self.grid_columnconfigure(0, weight=1, minsize=180) # Coluna dos botões
        self.grid_columnconfigure(1, weight=3) # Coluna principal
        # 1 linha que ocupa todo o espaço
        self.grid_rowconfigure(0, weight=1)

        # --- 3. Frame da Esquerda (Ações) ---
        
        # O fg_color cria a cor de fundo (azul na tua foto, aqui um cinza escuro)
        self.frame_botoes = ctk.CTkFrame(self, fg_color=("#F0F0F0", "#212325"), corner_radius=0)
        self.frame_botoes.grid(row=0, column=0, sticky="nsew") # Ocupa toda a coluna 0

        # Configura o grid *dentro* do frame de botões (para centrá-los)
        self.frame_botoes.grid_rowconfigure((0, 3), weight=1) # Espaçadores (em cima e em baixo)
        self.frame_botoes.grid_rowconfigure((1, 2), weight=0) # Linhas dos botões
        self.frame_botoes.grid_columnconfigure(0, weight=1)  # Coluna única

        self.btn_deletar = ctk.CTkButton(
            self.frame_botoes,
            text="Deletar",
            fg_color="#E74C3C", # Vermelho (como na foto)
            hover_color="#C0392B",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            command=self.on_deletar
        )
        self.btn_deletar.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_concluir = ctk.CTkButton(
            self.frame_botoes,
            text="Concluir",
            fg_color="#2ECC71", # Verde (como na foto)
            hover_color="#27AE60",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            command=self.on_concluir
        )
        self.btn_concluir.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # --- 4. Frame da Direita (Conteúdo Principal) ---
        
        self.frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_principal.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Configura o grid *dentro* do frame principal
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(2, weight=1) # Linha da lista (ocupa mais espaço)

        # --- 4.1. Título "Olá" ---
        self.label_ola = ctk.CTkLabel(
            self.frame_principal, 
            text="Olá!",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.label_ola.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="w")

        # --- 4.2. Título "Lista de tarefas" ---
        self.label_lista_titulo = ctk.CTkLabel(
            self.frame_principal, 
            text="Lista de tarefas:",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label_lista_titulo.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # --- 4.3. Lista de Tarefas (Scrollable + RadioButtons) ---
        
        # Variável para guardar o ID da tarefa selecionada
        self.var_tarefa_selecionada = ctk.IntVar(value=0)
        
        self.scroll_frame_tarefas = ctk.CTkScrollableFrame(self.frame_principal, height=250)
        self.scroll_frame_tarefas.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        # --- 4.4. Input de Adicionar Tarefa ---
        
        # Frame para agrupar o 'Adicionar' (entry + botão)
        self.frame_adicionar = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_adicionar.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_adicionar.grid_columnconfigure(0, weight=1)

        self.entry_nova_tarefa = ctk.CTkEntry(
            self.frame_adicionar,
            placeholder_text="escreva o texto aqui..."
        )
        self.entry_nova_tarefa.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.btn_adicionar = ctk.CTkButton(
            self.frame_adicionar,
            text="Adicionar",
            fg_color="#16A085", # Tom de ciano/verde
            hover_color="#117A65",
            width=100,
            command=self.on_adicionar
        )
        self.btn_adicionar.grid(row=0, column=1, sticky="e")
        
        # --- 4.5. Label de Status ---
        self.label_status = ctk.CTkLabel(self.frame_principal, text="Bem-vindo!", text_color="gray")
        self.label_status.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # --- 5. Inicialização ---
        self.atualizar_lista_tarefas()

    # --- Funções "Handler" (O que os botões fazem) ---

    def atualizar_lista_tarefas(self):
        """Busca as tarefas no 'logic' e atualiza o ScrollableFrame."""
        
        # 1. Limpa todos os widgets antigos (botões) da lista
        for widget in self.scroll_frame_tarefas.winfo_children():
            widget.destroy()
            
        # 2. Busca as novas tarefas
        tarefas = visualizar_tarefas()
        
        # 3. Cria e insere os novos RadioButtons
        if not tarefas:
            label_vazia = ctk.CTkLabel(self.scroll_frame_tarefas, text="Nenhuma tarefa registrada.")
            label_vazia.pack(anchor="w")
        else:
            for tarefa in tarefas:
                # O texto do botão será o __str__ do nosso modelo
                # Ex: [1] - Comprar pão (Pendente)
                texto_tarefa = str(tarefa)
                
                radio_btn = ctk.CTkRadioButton(
                    self.scroll_frame_tarefas,
                    text=texto_tarefa,
                    variable=self.var_tarefa_selecionada, # Variável de controle
                    value=tarefa.id, # O valor que o botão representa
                    font=ctk.CTkFont(size=14)
                )
                radio_btn.pack(anchor="w", padx=10, pady=5)

    def on_adicionar(self):
        """Chamado pelo botão Adicionar."""
        desc_tarefa = self.entry_nova_tarefa.get()
        
        mensagem_status = adicionar_tarefa(desc_tarefa)
        
        self.label_status.configure(text=mensagem_status)
        self.entry_nova_tarefa.delete(0, "end")
        self.atualizar_lista_tarefas() # Atualiza a lista visual
        self.var_tarefa_selecionada.set(0) # Limpa a seleção

    def on_concluir(self):
        """Chamado pelo botão Concluir."""
        id_t = self.var_tarefa_selecionada.get()
        
        if id_t == 0: # 0 é o valor padrão (nada selecionado)
            mensagem_status = "Por favor, selecione uma tarefa da lista."
        else:
            mensagem_status = concluir_tarefa(id_t)
        
        self.label_status.configure(text=mensagem_status)
        self.atualizar_lista_tarefas() # Atualiza a lista visual
        self.var_tarefa_selecionada.set(0) # Limpa a seleção

    def on_deletar(self):
        """Chamado pelo botão Deletar."""
        id_t = self.var_tarefa_selecionada.get()
        
        if id_t == 0:
            mensagem_status = "Por favor, selecione uma tarefa da lista."
        else:
            mensagem_status = deletar_tarefa(id_t)

        self.label_status.configure(text=mensagem_status)
        self.atualizar_lista_tarefas() # Atualiza a lista visual
        self.var_tarefa_selecionada.set(0) # Limpa a seleção

    def fechar_app(self):
        """Fecha a conexão com o banco antes de fechar a janela."""
        banco.close()
        print("Conexão com o banco fechada. Até logo!")
        self.destroy()