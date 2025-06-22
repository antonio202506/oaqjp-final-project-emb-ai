import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = { "raw_document": { "text": text_to_analyze } }
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    response = requests.post(url, json=myobj, headers=header)

    formatted_output = {
        'dominant_emotion': None
    }

    if response.status_code == 200:
        json_response = json.loads(response.text)

        if 'emotionPredictions' in json_response and len(json_response['emotionPredictions']) > 0 and \
            'emotion' in json_response['emotionPredictions'][0]:

            emotions_data = json_response['emotionPredictions'][0]['emotion']

            emotion_scores_for_dominant = {}

            for emotion_name, score in emotions_data.items():
                formatted_output[emotion_name] = score 
                emotion_scores_for_dominant[emotion_name] = score 

            if emotion_scores_for_dominant: # Ensure there are emotions to compare
                dominant_emotion = max(emotion_scores_for_dominant, key=emotion_scores_for_dominant.get)
                formatted_output['dominant_emotion'] = dominant_emotion

    return formatted_output