import pytest
import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from preprocess_data import preprocess_data, tokenize_dataset
from train import train_model_rf
from predict import PredictSentiment

# Example data for testing
data = {
    "text": ["I love this product!", "This is the worst experience ever."],
    "label": [1, 0],
}
df = pd.DataFrame(data)


def test_preprocess_data():
    processed_text = preprocess_data("I love this product!")
    assert processed_text == "i love this product"


def test_tokenize_dataset():
    features, labels = tokenize_dataset(df)
    assert features.shape[0] == 2
    assert labels.shape[0] == 2


def test_train_model_rf(tmpdir):
    # Create a temporary params.yaml file
    params_yaml = """
    train:
      model_dir: {}
      model_file: model.joblib
      vectorizer_file: vectorizer.joblib
    data_source:
      s3_path: s3://your-bucket-name/path/to/data.csv
    split:
      dir: {}
      total_file: total.h5
      train_file: train.h5
      val_file: val.h5
      test_file: test.h5
      trim_step: 10
    """.format(
        tmpdir, tmpdir
    )

    params_path = tmpdir.join("params.yaml")
    with open(params_path, "w") as f:
        f.write(params_yaml)

    # Train the model
    train_model_rf(params_path)

    # Check if the model and vectorizer files are created
    assert tmpdir.join("model.joblib").check()
    assert tmpdir.join("vectorizer.joblib").check()


def test_predict_sentiment(tmpdir):
    # Create a temporary model and vectorizer
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df["text"])
    model = SGDClassifier()
    model.fit(X, df["label"])

    model_path = tmpdir.join("model.joblib")
    vectorizer_path = tmpdir.join("vectorizer.joblib")
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    # Initialize predictor
    predictor = PredictSentiment(model_path, vectorizer_path)

    # Make predictions
    predictions = predictor.predict(["I love this product!"])
    assert predictions[0] == 1


if __name__ == "__main__":
    pytest.main()
