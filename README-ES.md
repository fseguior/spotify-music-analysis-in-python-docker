# Análisis de Música de Spotify usando Python, Jupyter Notebooks, Anaconda & Docker

Este proyecto utiliza la Spotify Web API y Python corriendo en un Docker Container, para analizar los audio features de las canciones recientemente escuchadas por un usuario. La librería "spotipy" que es un wrapper sobre esta API se utiliza para obtener los datos.

Referencias adicionales:

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/reference/)
- [Spotipy Librería Python](https://spotipy.readthedocs.io/)


## Como correr los notebooks y scripts de este repositorio
Este repositorio esta configurados para ser corrido en Linux, en mi caso use ***WSL2*** con ***Ubuntu 20.004 LTS***

Para correr los notebooks y scripts, seguir los siguientes pasos:

1. Clonar el repositorio
2. Crear una Spotify App siguiendo los pasos descriptos en la sección **"Configurar una Spotify App para obtener Authorization Tokens"**
3. Editar el archivo ***"credentials.py"*** en la carpeta ***./scripts***, y guardar los valores ***client_ID*** y ***client_SECRET***. Estos valores están vacíos en el repo ya que son keys privadas del usuario, ***credentials.py*** es ignorado por el archivo .gitignore.
4. Desde una línea de comando bash en la carpeta raíz del repositorio correr ***bash run.sh***. Este paso va a buildear y correr un Docker container con Anaconda y Jupyter Notebooks instalado (para detalles de la configuración ver la sección ***"Integrar Docker, Anaconda & Jupyter Notebooks"***)
5. Cuando el script termine de correr en la línea de comando se va a ver un link para abrir el Jupyter Notebook. The path va a ser algo similar a http://127.0.0.1:8888/?token=token
6. El Notebook utilizado para el análisis puede ser encontrado en ***.notebooks/spotify-music-analysis.ipynb***
  
  [Notebook Spotify Music Analysis](https://github.com/fseguior/spotify-music-analysis-in-python-docker/blob/main/notebooks/spotify-music-analysis.ipynb)

  
## Set Up y Configuración

### Configurar una Spotify App para obtener Authorization Tokens
1. Loguearse a [Sitio Spotify Developer](https://developer.spotify.com/dashboard/applications) y crear una App
2. En "Edit settings", agregar una entrada bajo ***"Redirect URIs"*** con el valor http://localhost:9000
3. Copiar las keys de ClientID y ClientSecret. Actualizar el archivo del repositorio ***./scripts/credentials.py*** con esos valores

Referencias adicionales:

[Guía Autorización Spotify](https://developer.spotify.com/documentation/general/guides/authorization-guide/)

### Integrar Docker, Anaconda & Jupyter Notebooks
Para hacer que el ambiente sea portable, todo corre en un Docker container basado en la imagen ***continuumio/miniconda3***. Esto permite correr Anaconda en un container para manejar los paquetes.

La configuración de este container se encuentra en el ***dockerfile***. Después de seleccionar la imagen de conda, el container crea y luego activa el ambiente customizado llamado ***spotify*** basado en el archivo de configuración YAML ***./config/Environment.yml***. Esto instala todos los paquetes necesarios en el ambiente.

Para buildear y correr el ambiente, las sentencias ***docker build*** y ***docker run*** se guardan en el archivo ***./run.sh***. El comando ***docker run*** publica el puerto 8888 en el host con el mismo puerto en el container, de forma tal que hace accesible el Jupyter notebook desde el host. También monta la carpeta del repo como un volumen del container. El comando ***docker run*** finalmente corre de forma interactiva el script bash ***./config/startnotebook.sh***. Este script bash corre el script Python ***./scripts/getData.py*** que utiliza la librería Spotipy para autenticarse usando tokens, y después hacer una llamada a la API para obtener los audio features de las últimas 50 canciones que el usuario escuchó. El output se guarda como un CSV en el archivo ***./data/Data.csv***. Este CSV es usado luego por el notebook ***./notebooks/spotify-music-analysis.ipynb*** que hace el procesamiento de los datos aplicando técnicas de K-Means, Mapas autoorganizados (Kohonen) y Análisis de Componentes Principales (PCA). La razón de correr ***getData.py*** separado del notebook es que el método de autorización de la API mediante las tokens falla en el notebook, pero corre ok desde una línea de comando de Python. Para esta autorización la librería crea un web server en el puerto especificado, y en el notebook dentro del container falla.

Referencias adicionales:

- [Activar Anaconda en Docker](https://pythonspeed.com/articles/activate-conda-dockerfile/)
- [Documentación Docker - Anaconda](https://docs.anaconda.com/anaconda/user-guide/tasks/docker/)
