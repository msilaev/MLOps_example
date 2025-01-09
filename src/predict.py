import sys
import os
import yaml
import joblib

# import tweepy

from preprocess_data import preprocess_text
from scipy.sparse import csr_matrix

# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("X_ACCES_KEY_ID")
# API_SECRET_KEY =  os.getenv("X_SECRET_ACCESS_KEY")
# ACCESS_TOKEN =  os.getenv("X_ACCESS_TOKEN")
# ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
# BEARER_TOKEN = os.getenv("X_BERER_TOCKEN")

# Authenticate to Twitter
# auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY,
# ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth)
BEARER_TOKEN = ""


# def fetch_latest_tweets(username, count=1):
#    client = tweepy.Client(bearer_token=BEARER_TOKEN)
#    user = client.get_user(username=username)
#    user_id = user.data.id
#    tweets = client.get_users_tweets(id=user_id, max_results=5)

#    return tweets


# def analyze_tweets(tweets, classifier):
#    results = []
#    for tweet in tweets:
#        prediction = classifier.predict([tweet])
#        sentiment = "Positive" if prediction[0] == 1 else "Negative"
#        results.append({"tweet": tweet, "sentiment": sentiment})
#    return results


class PredictSentiment:
    def __init__(self, param_yaml_path):
        with open(param_yaml_path) as f:
            params_yaml = yaml.safe_load(f)

        # model_path = os.path.join(
        #    params_yaml["train"]["model_dir"], params_yaml["train"]["model_file"]
        # )
        # vectorizer_path = os.path.join(
        #    params_yaml["train"]["model_dir"], params_yaml["train"]["vectorizer_file"]
        # )

        # Define the model path
        model_path = os.path.join(
            "/app",  # Ensure the base path is correct within the container
            params_yaml["train"]["model_dir"],
            params_yaml["train"]["model_file"],
        )

        # Define the model path
        vectorizer_path = os.path.join(
            "/app",  # Ensure the base path is correct within the container
            params_yaml["train"]["model_dir"],
            params_yaml["train"]["vectorizer_file"],
        )

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def preprocess(self, text_data):
        text_data = preprocess_text(text_data)
        print(text_data)

        text_data_list = []
        text_data_list.append(text_data)

        return csr_matrix(self.vectorizer.transform(text_data_list))

    def predict(self, text):
        preprocessed_data = self.preprocess(text)
        # print(preprocessed_data)
        return self.model.predict(preprocessed_data)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Usage: python predict.py <path to params.yaml>")
        sys.exit(1)

    param_yaml_path = sys.argv[1]

    classifier = PredictSentiment(param_yaml_path)

    text = "shit movie is good!"
    prediction = classifier.predict(text)
    sentiment = "Positive" if prediction[0] == 1 else "Negative"
    print(f"Prompt: {text}, Sentiment: {sentiment}")

    text = "This movie is bad!"
    prediction = classifier.predict(text)
    sentiment = "Positive" if prediction[0] == 1 else "Negative"
    print(f"Prompt: {text}, Sentiment: {sentiment}")

    # tweets = fetch_latest_tweets("vonderleyen")
    # results = analyze_tweets(tweets, classifier)

    # for result in results:
    #    print(f"Tweet: {result['tweet']}, Sentiment: {result['sentiment']}")
