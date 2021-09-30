# Spotify Music Analysis using Python, Jupyter Notebooks, Anaconda & Docker
This project uses Spotify Web API and Python running on a Docker Container to analyze the audio features the recently played songs for a given user. The "spotipy" library which is a wrapper over this API is used to get the data.

Further references:

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/reference/)
- [Spotipy Python Library](https://spotipy.readthedocs.io/)


## How to run the notebooks and scripts on this Repository
This Repo are configured to be run in Linux, in my case I used ***WSL2*** with ***Ubuntu 20.004 LTS***

To run the notebooks and scripts follow these steps:

1. Clone the repository
2. Create a Spotify App following the steps described below under **"Setting up a Spotify App to get the Authorization Tokens"**
3. Edit the file named ***"credentials.py"*** under the ***./scripts*** folder, and save the values for ***client_ID*** and ***client_SECRET***. These are empty on this repo as they are private keys to the user, ***credentials.py*** is ignored by the .gitignore file.
4. From a bash command line on the root folder of the repo run ***bash run.sh***. This step will build and run a container, with Anaconda and Jupyter Notebooks installed (details on the config provided on the "***Integrating Docker, Anaconda & Jupyter Notebooks"*** section)
5. When the script finishes running, in the command line you will see the link to open the Jupyter Notebook. The path wil look like http://127.0.0.1:8888/?token=token
6. The Notebook used for the analysis can be found under ***.notebooks/spotify-music-analysis.ipynb***
  
  [Notebook Spotify Music Analysis](https://github.com/fseguior/spotify-music-analysis-in-python-docker/blob/main/notebooks/spotify-music-analysis.ipynb)

  
## Set up and Configuration

### Setting up a Spotify App to get the Authorization Tokens
1. Log into the [Spotify Developer Site](https://developer.spotify.com/dashboard/applications) and create an App
2. After that copy the ClientID and the ClientSecret keys. Update the ***./scripts/credentials.py*** file on this repo with those values
3. Under edit settings, add an entry under ***"Redirect URIs"*** that is set to http://localhost:9000

Further references:

[Spotify Authorization Guide](https://developer.spotify.com/documentation/general/guides/authorization-guide/)

### Integrating Docker, Anaconda & Jupyter Notebooks
In order to make the scripts and notebooks portable, everything runs on a Docker container based on the image ***continuumio/miniconda3***. This allows to run Anaconda in the container to manage packages.

The configuration of this container is found on the ***dockerfile***. After selecting the conda image, the container reates and then activates a custom environment named ***spotify*** based on the YAML configuration file ***./config/Environment.yml***. This installs all of the needed libraries in the environment.

In order to build and run this environment, the ***docker build*** and ***docker run*** sentences are saved on the file ***./run.sh***. The ***docker run*** command publishes port 8888 on the host to the same port in the container, in order to make the Jupyter notebooks accesible from the host. It also mounts the repo folder as a volume of the container. The ***docker run*** command finally runs on an interactive bash the script ***./config/startnotebook.sh***. This bash script runs the Python script ***./scripts/getData.py*** which uses the Spotipy library to authenticate using the tokens, and then make an API call to get the audio features for the last 50 tracks a user has listened to. The output is saved as a CSV on the ***./data/Data.csv*** file. This CSV is then used by the notebook ***./notebooks/spotify-music-analysis.ipynb*** that does the processing of the data applying K-Means, Self-Organized Maps (Kohonen) and Princpial Components Analysis (PCA) techniques. The reason to run the ***getData.py*** decoupled from the notebook is that API token authentication from the notebook the method would fail, but run ok from the python command line. 

Further references:

- [Activating Anaconda in Docker](https://pythonspeed.com/articles/activate-conda-dockerfile/)
- [Docker - Anaconda Documentation](https://docs.anaconda.com/anaconda/user-guide/tasks/docker/)
