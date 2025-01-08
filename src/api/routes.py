import sys
import os
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.api.utils.predict import PredictSentiment
from src.api import app

from flask import (
    render_template,
    request,
    url_for,
    jsonify,
    redirect,
    # send_from_directory,
)

print(app.root_path)
param_yaml_path = os.path.join(
    os.path.dirname(os.path.dirname(app.root_path)), app.config["PARAM_YAML_PATH"]
)

classifier = PredictSentiment(param_yaml_path)


@app.route("/report_dvc_pipeline", methods=["GET", "POST"])
def dvc_report():
    return render_template("dvc_pipeline_report.html")


@app.route("/", methods=["GET", "POST"])
def start():
    return render_template("dvc_pipeline.html")


@app.route("/run_dvc_pipeline", methods=["GET", "POST"])
def run_dvc_pipeline():
    dvc_repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    result = subprocess.run(
        ["dvc", "repro"], cwd=dvc_repo_path, capture_output=True, text=True
    )

    if result.returncode == 0:
        return redirect(url_for("dvc_report"))

    return render_template("start.html")


#########################################
@app.route("/upload", methods=["GET", "POST"])
def text_upload():
    print("upload", app.root_path)

    if request.method == "POST":
        text_input = request.form.get("text", "").strip()

        if not text_input:
            return jsonify({"error": "Please enter some text"})

        try:
            upload_folder = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, "user.txt")

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_input)

            return redirect(url_for("predict"))

        except Exception as e:
            return jsonify({"error": str(e)})

    return render_template("upload.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    print(app.root_path)
    try:
        # Define the file path
        file_name = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], "user.txt")

        # Ensure the file exists
        if not os.path.exists(file_name):
            return (
                jsonify({"error": "No uploaded text found. Please upload text first."}),
                400,
            )

        # Read the text from the file
        with open(file_name, "r", encoding="utf-8") as f:
            text = f.read().strip()

        # Validate the content
        if not text:
            return (
                jsonify(
                    {"error": "The uploaded file is empty. Please upload valid text."}
                ),
                400,
            )

        # Make prediction using the classifier
        prediction = classifier.predict(text)
        sentiment = "Positive" if prediction[0] == 1 else "Negative"

        # Render the result in the report.html template
        return render_template("report.html", result=(sentiment, text))

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500


@app.route("/report/<result>")
def report(result):
    return render_template("report.html", result=result)
