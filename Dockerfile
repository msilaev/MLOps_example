# filepath: /c:/Users/mikes/Documents/STUDY/MLOps/sentiment_analysis/Dockerfile_dvc
# Use the base image
FROM base_image:latest


# Set the working directory in the container
COPY ./ /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Git and DVC
RUN apt-get update && apt-get install -y git
RUN pip install dvc

# Initialize Git repository
RUN git init
RUN dvc init --no-scm --force

# Copy the Git configuration files into the container
COPY .git .git

# Copy the DVC configuration files into the container
COPY .dvc .dvc
COPY dvc.yaml dvc.yaml
COPY params.yaml params.yaml

# Copy the rest of the application code into the container
COPY src src

# Set build arguments for AWS credentials
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

# Set environment variables for AWS credentials
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Set up the DVC remote configuration
RUN dvc remote add -d myremote s3://example1917/dvc_remote --force
RUN dvc remote modify myremote access_key_id ${AWS_ACCESS_KEY_ID}
RUN dvc remote modify myremote secret_access_key ${AWS_SECRET_ACCESS_KEY}

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Expose the port the app runs on
EXPOSE 5000

# Run the DVC pipeline to pull data from the remote storage
#RUN dvc pull
RUN dvc pull -r myremote

#-r myremote

# Set the FLASK_APP environment variable to point to the correct app module
ENV FLASK_APP=src/api/app.py

# Run the application
#CMD ["flask", "run"]
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
