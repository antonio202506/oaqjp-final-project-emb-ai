from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector")
def emotion_detector_route():
    text_to_analyze = request.args.get('textToAnalyze')

    response = emotion_detector(text_to_analyze)

    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    anger_score = response.get('anger')
    disgust_score = response.get('disgust')
    fear_score = response.get('fear')
    joy_score = response.get('joy')
    sadness_score = response.get('sadness')
    dominant_emotion = response.get('dominant_emotion')

    formatted_response_string = (
        f"For the given statement, the system response is "
        f"'anger': {anger_score}, "
        f"'disgust': {disgust_score}, "
        f"'fear': {fear_score}, "
        f"'joy': {joy_score}, "
        f"and 'sadness': {sadness_score}. "
        f"The dominant emotion is {dominant_emotion}."
    )

    return formatted_response_string

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)