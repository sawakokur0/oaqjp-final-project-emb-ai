"""Serve the Watson emotion detection application with Flask."""

from flask import Flask, render_template, request
from requests import RequestException

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.get("/")
def render_index_page():
    """Display the emotion detection form."""
    return render_template("index.html")


@app.get("/emotionDetector")
def analyze_emotion():
    """Analyze the text from the form and display the emotion scores."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text_to_analyze)
    except RequestException:
        return "The Watson emotion service is unavailable. Please try again later.", 502

    dominant = result["dominant_emotion"]
    if dominant is None:
        return "Invalid text! Please try again!", 400

    scores = ", ".join(
        f"'{emotion}': {score}"
        for emotion, score in result.items()
        if emotion != "dominant_emotion"
    )
    return (
        f"For the given statement, the system response is {scores}. "
        f"The dominant emotion is {dominant}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
