from database import inicializar_banco
from gui import AppGestorTarefas

# --- Ponto de Entrada da Aplicação ---


if __name__ == "__main__":
    
    inicializar_banco()
    
    app = AppGestorTarefas()
    app.protocol("WM_DELETE_WINDOW", app.fechar_app)
    app.mainloop()