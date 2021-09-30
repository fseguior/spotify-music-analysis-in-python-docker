# Análisis de Música de Spotify usando Python, Jupyter Notebooks, Anaconda & Docker

Este proyecto utiliza la Spotify Web API y Python corriendo en un Docker Container, para analizar los audio features de las canciones recientemente escuchadas por un usuario. La librería "spotipy" que es un wrapper sobre esta API se utiliza para obtener los datos.

Referencias adicionales:

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/reference/)
- [Spotipy Python Library](https://spotipy.readthedocs.io/)


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
1. Loguearse a [Spotify Developer Site](https://developer.spotify.com/dashboard/applications) y crear una App
2. En "Edit settings", agregar una entrada bajo ***"Redirect URIs"*** con el valor http://localhost:9000
3. Copiar las keys de ClientID y ClientSecret. Actualizar el archivo del repositorio ***./scripts/credentials.py*** con esos valores

Referencias adicionales:

[Spotify Authorization Guide](https://developer.spotify.com/documentation/general/guides/authorization-guide/)

### Integrar Docker, Anaconda & Jupyter Notebooks
Para hacer que el ambiente sea portable, todo corre en un Docker container basado en la imagen ***continuumio/miniconda3***. Esto permite correr Anaconda en un container para manejar los paquetes.

The configuration of this container is found on the ***dockerfile***. After selecting the conda image, the container reates and then activates a custom environment named ***spotify*** based on the YAML configuration file ***./config/Environment.yml***. This installs all of the needed libraries in the environment.

In order to build and run this environment, the ***docker build*** and ***docker run*** sentences are saved on the file ***./run.sh***. The ***docker run*** command publishes port 8888 on the host to the same port in the container, in order to make the Jupyter notebooks accesible from the host. It also mounts the repo folder as a volume of the container. The ***docker run*** command finally runs on an interactive bash the script ***./config/startnotebook.sh***. This bash script runs the Python script ***./scripts/getData.py*** which uses the Spotipy library to authenticate using the tokens, and then make an API call to get the audio features for the last 50 tracks a user has listened to. The output is saved as a CSV on the ***./data/Data.csv*** file. This CSV is then used by the notebook ***./notebooks/spotify-music-analysis.ipynb*** that does the processing of the data applying K-Means, Self-Organized Maps (Kohonen) and Princpial Components Analysis (PCA) techniques. The reason to run the ***getData.py*** decoupled from the notebook is that API token authentication from the notebook the method would fail, but run ok from the python command line. 

Referencias adicionales:

- [Activating Anaconda in Docker](https://pythonspeed.com/articles/activate-conda-dockerfile/)
- [Docker - Anaconda Documentation](https://docs.anaconda.com/anaconda/user-guide/tasks/docker/)
