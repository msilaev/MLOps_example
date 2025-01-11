# Sentiment Analysis Project

## Project Description

This project is a sentiment analysis application that uses machine learning to classify text data into positive or negative sentiments. The project uses Python and leverages various tools and frameworks such as Flask, DVC, MLflow, Docker, and GitHub Actions for CI/CD. Project created with MLOps-Template cookiecutter. For more info, see the [MLOps Guide](https://mlopsstudygroup.github.io/mlops-guide/).
 For the DVC remote repository, the AWS S3 bucket is used as a primary option. It can be changed to the local remote for developing purposes.

Besides DVC repository models and artifacts such as tokens vectorizers are registered in MLflow backend. Using the Mlops app different models can be chosen to be used in REST API to analyze user data.

Classifier is trained on IMDB Dataset of 50K Movie Reviews from [Kaggle] (https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews)


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

# Sentiment Analysis Project

This project uses a CI/CD pipeline to automate the build, test, and deployment processes using GitHub Actions, Docker, and AWS.

## CI/CD Pipeline

The CI/CD pipeline is defined in `.github/workflows/ci-cd.yml` and includes the following steps:

1. **Set up Python**: Installs Python 3.11.
2. **Install dependencies**: Upgrades pip and installs required packages from `requirements.txt`.
3. **Configure DVC remote**: Sets up DVC remote storage on S3.
4. **Build and push Docker images**: Builds Docker images using `docker-compose` and pushes them to Amazon ECR.
5. **Deploy to EC2**: Deploys the Docker images to an EC2 instance.

## Deployment

The deployment process involves:

1. **Retrieving EC2 Public IP**: Uses AWS CLI to get the public IP of the EC2 instance.
2. **Configuring Security Group**: Ensures the security group allows traffic on necessary ports.
3. **Deploying to EC2**: Uses SSH to connect to the EC2 instance and deploy the Docker images.

## Usage

To trigger the CI/CD pipeline, push changes to the `main` branch or create a pull request targeting the `main` branch.

## Requirements

- AWS credentials with appropriate permissions.
- An EC2 instance with Docker and Docker Compose installed.
- An S3 bucket for DVC remote storage.

## Environment Variables

Ensure the following secrets are set in your GitHub repository:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ARN_OICN_ACCESS`
- `EC2_KEY`
- `EC2_HOST`


## License

This project is licensed under the MIT License.


## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [DVC](https://dvc.org/)
- [MLflow](https://mlflow.org/)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://github.com/features/actions)
```
