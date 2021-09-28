docker build -t spotify .
docker run -i -t -p 8888:8888 --mount type=bind,source="$(pwd)",target=/app \
    spotify /bin/bash \
    -c "/opt/conda/bin/conda install jupyter -y --quiet && mkdir \
    /opt/notebooks && /opt/conda/bin/jupyter notebook \
    --notebook-dir=/opt/notebooks --ip='*' --port=8888 \
    --no-browser --allow-root"
    
  echo 'Your TOKEN for Jupyter Notebook is:'
  SERVER=$(docker exec -it jupyter jupyter notebook list)
  echo "${SERVER}" | grep '/notebook' | sed -E 's/^.*=([a-z0-9]+).*$/\1/'