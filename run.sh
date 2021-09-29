docker build -t spotify .
docker run -i -t -p 8888:8888 --mount type=bind,source="$(pwd)",target=/app spotify /bin/bash -c "bash -i ./config/startnotebook.sh"    