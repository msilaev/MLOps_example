import sys
import os
import yaml
import joblib
import math
import json
import pandas as pd

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import (
    average_precision_score,
    roc_auc_score,
    precision_recall_curve,
)
from scipy.sparse import csr_matrix
from dvclive import Live


def evaluate(param_yaml_path, data_category, live):
    # Load parameters from YAML
    with open(param_yaml_path) as f:
        params_yaml = yaml.safe_load(f)

    model_path = os.path.join(
        params_yaml["train"]["model_dir"], params_yaml["train"]["model_file"]
    )
    vectorizer_path = os.path.join(
        params_yaml["train"]["model_dir"], params_yaml["train"]["vectorizer_file"]
    )

    # Load classifier and vectorizer
    classifier = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    # Load test dataset
    test_dataset_path = os.path.join(
        params_yaml["train"]["dir"], params_yaml["train"]["test_file"]
    )
    df_test = pd.read_csv(test_dataset_path)
    X_test, Y_test = df_test["feature"], df_test["label"]

    # Preprocessing
    X_test = vectorizer.transform(X_test)
    X_test = csr_matrix(X_test)
    lb = LabelBinarizer()
    Y_test = lb.fit_transform(Y_test).ravel()

    # Testing
    predictions_by_class = classifier.predict_proba(X_test)
    predicted_test = classifier.predict(X_test)
    avg_prec = average_precision_score(Y_test, predicted_test)
    roc_auc = roc_auc_score(Y_test, predicted_test)

    if not live.summary:
        live.summary = {"avg_prec": {}, "roc_auc": {}}
    live.summary["avg_prec"][data_category] = avg_prec
    live.summary["roc_auc"][data_category] = roc_auc

    # ROC Curve
    live.log_sklearn_plot("roc", Y_test, predicted_test, name=f"roc/{data_category}")

    # Precision-Recall Curve
    precision, recall, prc_thresholds = precision_recall_curve(
        Y_test, predictions_by_class[:, 1]
    )
    nth_point = max(1, math.ceil(len(prc_thresholds) / 1000))
    prc_points = list(zip(precision, recall, prc_thresholds))[::nth_point]
    prc_dir = os.path.join("eval", "prc")
    os.makedirs(prc_dir, exist_ok=True)
    prc_file = os.path.join(prc_dir, f"{data_category}.json")
    with open(prc_file, "w") as fd:
        json.dump(
            {
                "prc": [
                    {"precision": p, "recall": r, "threshold": t}
                    for p, r, t in prc_points
                ]
            },
            fd,
            indent=4,
        )

    # Confusion Matrix
    live.log_sklearn_plot(
        "confusion_matrix",
        Y_test.squeeze(),
        predictions_by_class.argmax(-1),
        name=f"cm/{data_category}",
    )


if __name__ == "__main__":
    param_yaml_path = sys.argv[1]

    with open(param_yaml_path) as f:
        params_yaml = yaml.safe_load(f)

    model_path = os.path.join(
        params_yaml["train"]["model_dir"], params_yaml["train"]["model_file"]
    )
    vectorizer_path = os.path.join(
        params_yaml["train"]["model_dir"], params_yaml["train"]["vectorizer_file"]
    )

    # Load classifier and vectorizer
    classifier = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    # Load test dataset
    test_dataset_path = os.path.join(
        params_yaml["train"]["dir"], params_yaml["train"]["test_file"]
    )
    df_test = pd.read_csv(test_dataset_path)
    X_test, Y_test = df_test["feature"], df_test["label"]

    # Initialize DVCLive
    EVAL_PATH = "eval"
    live = Live(os.path.join(EVAL_PATH, "live"), dvcyaml=False)
    evaluate(param_yaml_path, "test", live)
    live.make_summary()
