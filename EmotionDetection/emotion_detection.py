import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = { "raw_document": { "text": text_to_analyze } }
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    response = requests.post(url, json=myobj, headers=header)

    formatted_output = {'anger': None, 'disgust': None, 'fear': None, 'joy': None,
        'sadness': None, 'dominant_emotion': None }

    if response.status_code == 200:
        try:
            json_response = json.loads(response.text)

            if 'emotionPredictions' in json_response and len(json_response['emotionPredictions']) > 0 and \
               'emotion' in json_response['emotionPredictions'][0]:

                emotions_data = json_response['emotionPredictions'][0]['emotion']

                formatted_output['anger'] = emotions_data.get('anger')
                formatted_output['disgust'] = emotions_data.get('disgust')
                formatted_output['fear'] = emotions_data.get('fear')
                formatted_output['joy'] = emotions_data.get('joy')
                formatted_output['sadness'] = emotions_data.get('sadness')

                current_emotion_scores = {
                    'anger': formatted_output['anger'],
                    'disgust': formatted_output['disgust'],
                    'fear': formatted_output['fear'],
                    'joy': formatted_output['joy'],
                    'sadness': formatted_output['sadness']
                }

                valid_emotions = {k: v for k, v in current_emotion_scores.items() if v is not None}
                if valid_emotions:
                    dominant_emotion = max(valid_emotions, key=valid_emotions.get)
                    formatted_output['dominant_emotion'] = dominant_emotion

        except json.JSONDecodeError:
            pass
        except KeyError:
            pass
    # For status_code 400, the initial formatted_output has all None

    return formatted_output
