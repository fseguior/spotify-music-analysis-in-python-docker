# Spotify Music Analysis using Python, Jupyter Notebooks, Anaconda & Docker
This project uses Spotify Web API and Python running on a Docker Container to analyze the audio features the recently played songs for a given user. The "spotipy" library which is a wrapper over this API is used to get the data.

Further references:

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/reference/)
- [Spotipy Python Library](https://spotipy.readthedocs.io/)


## How to run this repo


## Set up and Configuration

### Setting up a Spotify App to get the Authentication Tokens


### Integrating Docker, Anaconda & Jupyter Notebooks
In order to make the scripts and notebooks portable, everything runs on a Docker container based on the image ***continuumio/miniconda3***. This allows to run Anaconda in the container to manage packages.

The configuration of this container is found on the ***dockerfile***. After selecting the conda image, the container reates and then activates a custom environment named ***spotify*** based on the YAML configuration file ***./config/Environment.yml***. This installs all of the needed libraries in the environment.

In order to build and run this environment, the ***docker build*** and ***docker run*** sentences are saved on the file ***./run.sh***. The ***docker run*** command publishes port 8888 on the host to the same port in the container, in order to make the Jupyter notebooks accesible from the host. The ***docker run*** command also runs on an interactive bash the script ***./config/startnotebook.sh***. This bash script runs the Python script ***./scripts/getData.py*** which uses the Spotipy library to authenticate using the tokens, and then make an API call to get the audio features for the last 50 tracks a user has listened to. The output is saved as a CSV on the ***./data/Data.csv*** file. This CSV is then used by the notebook ***./notebooks/spotify-music-analysis.ipynb*** that does the processing of the data applying K-Means, Self-Organized Maps (Kohonen) and Princpial Components Analysis (PCA) techniques.

Further references:

- [Activating Anaconda in Docker](https://pythonspeed.com/articles/activate-conda-dockerfile/)
- [Docker - Anaconda Documentation](https://docs.anaconda.com/anaconda/user-guide/tasks/docker/)
