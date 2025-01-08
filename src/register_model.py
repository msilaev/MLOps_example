import os
import sys
import mlflow
import mlflow.sklearn
import joblib
import yaml
import pandas as pd

from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report, accuracy_score
from scipy.sparse import csr_matrix
from mlflow.tracking import MlflowClient

from dotenv import load_dotenv


def register_model(param_yaml_path):
    load_dotenv()

    # Load parameters from YAML
    with open(param_yaml_path) as f:
        params_yaml = yaml.safe_load(f)

    # Set MLflow tracking URI
    mlflow.set_tracking_uri(
        os.getenv("MLFLOW_TRACKING_URI", "http://mlflow_server:5000")
    )

    experiment_name = "Sentiment Analysis Experiment"
    mlflow.set_experiment(experiment_name)

    test_dataset_path = os.path.join(
        params_yaml["train"]["dir"], params_yaml["train"]["test_file"]
    )

    df_test = pd.read_csv(test_dataset_path)
    X_test, Y_test = df_test["feature"], df_test["label"]

    # Define the model and vectorizer paths
    model_path = os.path.join(
        "/app",  # Ensure the base path is correct within the container
        params_yaml["train"]["model_dir"],
        params_yaml["train"]["model_file"],
    )
    vectorizer_path = os.path.join(
        "/app",  # Ensure the base path is correct within the container
        params_yaml["train"]["model_dir"],
        params_yaml["train"]["vectorizer_file"],
    )

    # Load the model and vectorizer
    classifier = joblib.load(model_path)
    cv = joblib.load(vectorizer_path)

    X_test = cv.transform(X_test)
    X_test = csr_matrix(X_test)

    lb = LabelBinarizer()
    Y_test = lb.transform(Y_test).ravel()

    # Start an MLflow run
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_param("loss", "hinge")
        mlflow.log_param("max_iter", 500)
        mlflow.log_param("random_state", 42)

        # Testing
        predicted_test = classifier.predict(X_test)
        accuracy = accuracy_score(Y_test, predicted_test)
        report = classification_report(
            Y_test,
            predicted_test,
            target_names=["Positive", "Negative"],
            output_dict=True,
        )

        # print(report)

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", report["weighted avg"]["precision"])
        mlflow.log_metric("recall", report["weighted avg"]["f1-score"])
        mlflow.log_artifact(vectorizer_path)

        mlflow.sklearn.log_model(
            sk_model=classifier,
            artifact_path="model",
            registered_model_name="SentimentAnalysisModel",
        )

        # Register and transition to Production
        client = MlflowClient()
        model_name = "SentimentAnalysisModel"
        latest_version_info = client.get_latest_versions(model_name, stages=["None"])[0]
        client.transition_model_version_stage(
            name=model_name,
            version=latest_version_info.version,
            stage="Production",
            archive_existing_versions=True,
        )

        # Register the model
        run_id = run.info.run_id
        print(run_id)
        mlflow.register_model(f"runs:/{run_id}/model", "SentimentAnalysisModel")

        # Create a file indicating whether a model is registered
        model_reg_path = os.path.join(
            "/app",  # Ensure the base path is correct within the container
            params_yaml["train"]["model_dir"],
            "model_registered.txt",
        )
        with open(model_reg_path, "w") as f:
            f.write("yes")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Usage: python register_model.py <path to params.yaml>")
        sys.exit(1)

    param_yaml_path = sys.argv[1]

    with open(param_yaml_path) as f:
        params_yaml = yaml.safe_load(f)

    register_model(param_yaml_path)
