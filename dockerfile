FROM continuumio/miniconda3
WORKDIR /app

# Create the environment:
COPY config/environment.yml .
RUN conda env create -f environment.yml

# Activate environment
RUN echo "conda activate spotify && /opt/conda/bin/conda install jupyter -y --quiet" >> ~/.bashrc