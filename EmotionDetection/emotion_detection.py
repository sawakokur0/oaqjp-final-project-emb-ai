"""Analyze English text with the IBM Watson NLP emotion service."""

import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the dominant emotion for the text."""
    if not text_to_analyze or not text_to_analyze.strip():
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))

    response = requests.post(
        WATSON_URL,
        json={"raw_document": {"text": text_to_analyze}},
        headers=MODEL_HEADERS,
        timeout=15,
    )
    if response.status_code == 400:
        return dict.fromkeys((*EMOTIONS, "dominant_emotion"))

    response.raise_for_status()
    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
