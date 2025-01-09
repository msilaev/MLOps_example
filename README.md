# Sentiment Analysis Project

## Project Description

This project is a sentiment analysis application that uses machine learning to classify text data into positive or negative sentiments. The project uses Python and leverages various tools and frameworks such as Flask, DVC, MLflow, Docker, and GitHub Actions for CI/CD. Project created with MLOps-Template cookiecutter. For more info: https://mlopsstudygroup.github.io/mlops-guide/. For the DVC remote repository, the AWS S3 bucket is used as a primary option. It can be changed to the local remote for developing purposes.

Besides DVC repository models and artifacts such as tokens vectorizers are registered in MLflow backend. Using the Mlops app different models can be chosen to be used in REST API to analyze user data.




## Project Structure

```
sentiment_analysis/
├── src/
│   ├── preprocess.py
│   ├── train.py
│   ├── tests/
│   │   └── test_sentiment_analysis.py
├── Dockerfile_flask
├── Dockerfile_dvc
├── Dockerfile_mlflow
├──

requirements.txt


├──

docker-compose.yml


└── .github/
    └── workflows/
        └──

ci-cd.yml


```

## Setup Instructions

### Prerequisites

- Python 3.11
- Docker
- Docker Compose
- AWS CLI (for DVC remote storage)

### Installation

1. **Clone the repository:**

```sh
git clone https://github.com/your-username/sentiment_analysis.git
cd sentiment_analysis
```

2. **Set up a virtual environment:**

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

3. **Build and run Docker Compose:**

```sh
docker build -f Dockerfile_base -t base_image:latest .
docker-compose up --build -d
```
### Running Application
1. **Access the Flask application:**

Open your browser and navigate to `http://localhost:5001`. First, it will suggest running the DVC pipeline. 
If this is successful the form for user text sentiment analysis opens. 

2. **Access the MLflow application:**

Open your browser and navigate to `http://localhost:5000`.

### Running Tests

### Linting and Formatting

1. **Run `flake8` linter:**

```sh
docker-compose exec -T flask_app flake8 .
docker-compose exec -T dvc_service flake8 .
```

2. **Run `black` linter:**

```sh
docker-compose exec -T flask_app black . --check
docker-compose exec -T dvc_service black . --check
```

### CI/CD with GitHub Actions

The project uses GitHub Actions for continuous integration and deployment. The CI/CD pipeline is defined in

ci-cd.yml

.

### CI/CD Pipeline

The CI/CD pipeline includes the following steps:

1. **Checkout code:**

```yaml
- name: Checkout code
  uses: actions/checkout@v2
```

2. **Set up Python:**

```yaml
- name: Set up Python
  uses: actions/setup-python@v2
  with:
    python-version: 3.11
```

3. **Install dependencies:**

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install flake8 black
```

4. **Configure DVC remote:**

```yaml
- name: Configure DVC remote
  run: |
    dvc remote add -d myremote s3://example1917/dvc_remote
    dvc remote modify myremote access_key_id $AWS_ACCESS_KEY_ID
    dvc remote modify myremote secret_access_key $AWS_SECRET_ACCESS_KEY
```

5. **Install Docker Compose:**

```yaml
- name: Install Docker Compose
  run: |
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    docker-compose --version
```

6. **Build and run Docker Compose:**

```yaml
- name: Build and run Docker Compose
  run: |
    docker-compose up --build -d
```

7. **Clean up DVC lock files:**

```yaml
- name: Clean up DVC lock files
  run: |
    docker-compose exec -T dvc_service rm -f .dvc/tmp/lock .dvc/tmp/rwlock
```

8. **Run DVC pipeline:**

```yaml
- name: Run DVC pipeline
  run: |
    docker-compose exec -T dvc_service dvc repro
```

9. **Run tests:**

```yaml
- name: Run tests for flask
  run: |
    docker-compose exec -T flask_app pytest src/tests

- name: Run tests for dvc_service
  run: |
    docker-compose exec -T dvc_service pytest src/tests

- name: Run tests for mlflow_server
  run: |
    docker-compose exec -T mlflow_server pytest src/tests
```

10. **Run linters:**

```yaml
- name: Run flake8 linter
  run: |
    docker-compose exec -T flask_app flake8 .

- name: Run black linter
  run: |
    docker-compose exec -T flask_app black . --check
```

11. **Stop Docker Compose:**

```yaml
- name: Stop Docker Compose
  run: |
    docker-compose down
```


## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [DVC](https://dvc.org/)
- [MLflow](https://mlflow.org/)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://github.com/features/actions)
```
