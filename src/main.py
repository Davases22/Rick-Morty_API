# main.py
import threading
from api.endpoints import app
from gui.tkinter_app import start_tkinter_app

'''
Hilo para ejecutar la aplicación FastAPI'''
def run_fastapi():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    '''
    Ejecutar FastAPI en un hilo separado'''
    threading.Thread(target=run_fastapi).start()
    
    '''
    Ejecutar la interfaz gráfica de Tkinter'''
    start_tkinter_app()
