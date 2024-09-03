# gui/tkinter_app.py
'''
De Tkinter se importa Tk, que es la clase principal para
crear una ventana de Tkinter. Label, Entry, Button, StringVar
y ttk son widgets y clases que se usan para construir la interfaz gráfica.'''
from tkinter import Tk, Label, Entry, Button, StringVar, ttk, Text, Scrollbar, Frame

'''
La función asksaveasfilename del módulo tkinter.filedialog permite
abrir un cuadro de diálogo para que el usuario seleccione la ruta
y el nombre del archivo donde se guardará la descarga.'''
from tkinter.filedialog import asksaveasfilename 

'''
requests se utiliza para realizar solicitudes HTTP a la
API de FastAPI que se ha implementado.'''
import requests

'''
json se utiliza para formatear los datos JSON que se obtienen de la API.'''
import json

from PIL import Image, ImageTk
from io import BytesIO

def start_tkinter_app(): #Función Principal para Iniciar la Aplicación Tkinter
    
    '''
    Esta función se activa cuando el usuario presiona el botón Fetch Data.'''
    def fetch_data():
        '''
        Se obtienen los valores de los campos de entrada del usuario
        utilizando get() de los objetos StringVar.'''
        name = name_var.get()
        status = status_var.get()
        species = species_var.get()
        
        '''
        Se construye una URL con los parámetros de consulta obtenidos.'''
        url = f"http://127.0.0.1:8000/fetch-data/?name={name}&status={status}&species={species}"# Construir URL para la solicitud GET
        
        
        '''
        * Si hay un error en la solicitud, se captura con una excepción y se muestra un mensaje de error en el campo de resultados.
        * Si la solicitud es exitosa, se convierte la respuesta JSON en un string formateado y se muestra en la GUI.'''
        try:
            '''
            Se utiliza requests.get para enviar la solicitud a la API FastAPI.'''
            response = requests.get(url)
            
            response.raise_for_status()
            data = response.json()
        
            # Mostrar datos en el widget Text
            result_text.delete(1.0, "end")  # Limpiar el widget antes de agregar nuevos datos
            result_text.insert("end", json.dumps(data, indent=2))
            
            # Limpiar el Treeview
            for row in tree.get_children():
                tree.delete(row)
                
            # Insertar datos en el Treeview
            for character in data.get('results', []):
                tree.insert("", "end", values=(character.get("id"), character.get("name"), character.get("status"), character.get("species")))
    
            
        except requests.RequestException as e:
            result.set(f"Error fetching data: {str(e)}")
            
            
    '''
    Similar a fetch_data, pero esta función descarga un archivo ZIP.'''
    def download_data():
        name = name_var.get()
        status = status_var.get()
        species = species_var.get()

        # Construir URL para la solicitud GET de descarga
        url = f"http://127.0.0.1:8000/download-data/?name={name}&status={status}&species={species}"
        
        '''
        * Si la solicitud es exitosa, el contenido de la respuesta (archivo ZIP) se guarda en el archivo data.zip.
        * Se actualiza el campo de resultado con un mensaje de éxito o error.'''
        try:
            response = requests.get(url) #Envía la solicitud para descargar datos desde la API.
            response.raise_for_status()
            
            '''
            Usar un cuadro de diálogo para que el usuario elija la ubicación de guardado'''
            file_path = asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP files", "*.zip")])

            if file_path:  # Verificar si se ha seleccionado una ruta
                '''
                Abrimos manejador de conexto para encapsular la 
                apertura y cierre de archivos de forma segura y automática.'''
                # Guardar archivo ZIP descargado
                with open(file_path, "wb") as f:
                    f.write(response.content)
                result.set(f"Data downloaded successfully as {file_path}")
            else:
                result.set("Download canceled by user.")
            
        except requests.RequestException as e:
            result.set(f"Error downloading data: {str(e)}")

    # Configuración de la ventana principal de Tkinter
    root = Tk()
    root.title("Rick and Morty Data Fetcher")

    # Variables para los campos de entrada
    name_var = StringVar()
    status_var = StringVar()
    species_var = StringVar()
    result = StringVar()
    
    '''
    Frame para los botones y para TEXT'''
    frame = Frame(root)
    frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")


    # Etiquetas y campos de entrada
    Label(frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    Entry(frame, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

    Label(frame, text="Species:").grid(row=1, column=0, padx=5, pady=5)
    Entry(frame, textvariable=species_var).grid(row=1, column=1, padx=5, pady=5)

    Label(frame, text="Status:").grid(row=2, column=0, padx=5, pady=5)
    ttk.Combobox(frame, textvariable=status_var, values=["", "alive", "dead", "unknown"]).grid(row=2, column=1, padx=5, pady=5)

    # Botones de acción
    Button(frame, text="Consultar", command=fetch_data).grid(row=3, column=0, columnspan=1, pady=10)
    Button(frame, text="Descargar", command=download_data).grid(row=3, column=1, columnspan=3, pady=10)

    # Campo de resultado Text
    Label(frame, text=" ").grid(row=0, column=4, padx=5, pady=5)
    Label(frame, text="Respuesta JSON:").grid(row=0, column=5, padx=5, pady=5)
    result_text = Text(frame, wrap="word", height=15, width=50)
    result_text.grid(row=1, column=5, columnspan=1, padx=5, pady=5)
    scrollbar = Scrollbar(frame, command=result_text.yview)
    scrollbar.grid(row=1, column=7, sticky="ns")
    result_text.config(yscrollcommand=scrollbar.set)

    # Campo de resultado Treeview
    Label(root, text="Datos obtenidos:").grid(row=5, column=0, padx=5, pady=5, sticky="nw")
    columns = ("ID", "Name", "Status", "Species")
    tree = ttk.Treeview(root, columns=columns, show='headings')
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Status", text="Status")
    tree.heading("Species", text="Species")
    tree.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
    
    # Dimensiones
    root.grid_rowconfigure(0, weight=1)  # Asegura que la primera fila tenga peso para el redimensionamiento
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_rowconfigure(4, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    frame.grid_rowconfigure(6, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)




    # Iniciar el bucle de la interfaz de usuario
    root.mainloop()
