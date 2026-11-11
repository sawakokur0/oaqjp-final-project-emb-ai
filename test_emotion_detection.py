"""Test Watson response formatting and Flask routing with controlled responses."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector
from server import app

EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")
CASES = (
    ("I am really mad about this", "anger"),
    ("I am disgusted just hearing about this", "disgust"),
    ("I am really afraid that this will happen", "fear"),
    ("I am glad this happened", "joy"),
    ("I feel sad about this", "sadness"),
)


def watson_response(dominant):
    """Create a test fixture in the Watson API response format."""
    scores = {emotion: 0.05 for emotion in EMOTIONS}
    scores[dominant] = 0.8
    response = Mock(status_code=200)
    response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}
    return response


class TestEmotionDetector(unittest.TestCase):
    """Verify the detector and the application routes."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_each_dominant_emotion(self, post):
        for text, emotion in CASES:
            with self.subTest(emotion=emotion):
                post.return_value = watson_response(emotion)
                result = emotion_detector(text)
                self.assertEqual(result["dominant_emotion"], emotion)
                self.assertEqual(set(result), {*EMOTIONS, "dominant_emotion"})
                self.assertEqual(post.call_args.kwargs["json"]["raw_document"]["text"], text)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_blank_input(self, post):
        self.assertEqual(emotion_detector(" "), dict.fromkeys((*EMOTIONS, "dominant_emotion")))
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_watson_bad_request(self, post):
        post.return_value = Mock(status_code=400)
        self.assertEqual(emotion_detector("!"), dict.fromkeys((*EMOTIONS, "dominant_emotion")))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_flask_prediction(self, post):
        post.return_value = watson_response("joy")
        response = app.test_client().get(
            "/emotionDetector", query_string={"textToAnalyze": "I am glad this happened"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("The dominant emotion is joy.", response.get_data(as_text=True))

    def test_flask_blank_input(self):
        response = app.test_client().get("/emotionDetector")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid text", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
