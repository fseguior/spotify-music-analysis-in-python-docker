FROM continuumio/miniconda3
WORKDIR /app

# Create the environment:
COPY config/environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "spotify", "/bin/bash", "-c"]
