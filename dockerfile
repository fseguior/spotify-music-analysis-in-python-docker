FROM continuumio/miniconda3
WORKDIR /app

# Create the environment:
COPY config/environment.yml .
RUN conda env create -f environment.yml

#RUN conda init bash
RUN echo "conda activate spotify" >> ~/.bashrc
