docker build -t spotify .
docker run -i -t -p 8888:8888 --mount type=bind,source="$(pwd)",target=/app \
    continuumio/miniconda3 /bin/bash \
    -c "/opt/conda/bin/conda install jupyter -y --quiet && mkdir \
    /opt/notebooks && /opt/conda/bin/jupyter notebook \
    --notebook-dir=/opt/notebooks --ip='*' --port=8888 \
    --no-browser --allow-root"





    CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]