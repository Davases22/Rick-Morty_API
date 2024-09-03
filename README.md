# GUI para consultar, filtrar y descargar información de la API pública Rick and Morty
## Preparación para usar
Asegúrese de tener instalado pip e instale las depedencias ubicándose, desde la terminal, en la ubicación del repositorio local y corra el comando ***pip install -r requirements.txt***

## Modo de uso
Una vez instaladas las dependencias, ejecute el archivo ***main.py***, debería arrojarle una ventana de la siguiente manera:
<img src="https://github.com/Davases22/Rick-Morty_API/blob/master/img/img_1.png" width="500"/>

## Modo de interacción
### Consulta
Una vez esté en la GUI, ya puede empezar a jugar con ella. Puede hacer consultas con o sin filtros de personajes de la serie dependiendo de lo que desee. Puede filtrar por nombre de los personajes, su estado (vivo, muerto o desconocido) y su especie también, el botón "consultar" arrojará la información solicitada en formato JSON en la aprte superior derecha y en una tabla en la parte inferior. En el siguiente ejemplo se puede apreciar la consulta que se hizo filtrando los personajes con nombre Rick, que estén vivos y sean de la especia humano:
<img src="https://github.com/Davases22/Rick-Morty_API/blob/master/img/img_2.png" width="500"/>
Se puede apreciar que se obtienen 22 personajes en 2 páginas. Pueden visualizarse en formato JSON o de manera más amigable en la parte inferior en un tabla. Es información también puede ser descargada.

### Descarga
Si la información que está visualizando es la que desea descargar puede hacer click en el botón "Descargar", esto desplegará el explorador de archivos para que pueda elegir el nombre y la ubicación de su descarga, la información se almacenará en formato JSON y estará almacenada en un archivo comprimido ZIP, veamos un ejemplo de cómo se ve la interacción al hacer click en el botón "Descargar"
<img src="https://github.com/Davases22/Rick-Morty_API/blob/master/img/img_3.png" width="500"/>
