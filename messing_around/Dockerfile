# Start your image with a node base image
FROM jupyter/scipy-notebook


# RUN mkdir my-model
# ENV MODEL_DIR=/home/jovyan/my-model
# ENV MODEL_FILE_LDA=clf_lda.joblib
# ENV MODEL_FILE_NN=clf_nn.joblib

# The /app directory should act as the main application directory
WORKDIR /data

# To maintain some data after deleting/reseting the env
VOLUME /data

# Install any dependencies
RUN pip install joblib

# Copy the train and test data
COPY train.csv ./train.csv
COPY test.csv ./test.csv

# Copy the train and interference python files
COPY train.py ./train.py
COPY interference.py ./interference.py

# Run the train file
RUN python train.py

# To build the Image, run the following in CMD:
    # docker build -t [name] -f Dockerfile

# Then run the interference by:
    # docker run [name] python interference.py