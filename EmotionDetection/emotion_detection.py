import requests
import json

def emotion_detector(text_to_analyze):
    # Check for blank input
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }, 400  # HTTP 400: Bad Request
    
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    data = {"raw_document": {"text": text_to_analyze}}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        emotions = response.json()
        
        # Extract emotions from response
        emotion_scores = emotions.get("emotion", {})
        anger = emotion_scores.get("anger", 0)
        disgust = emotion_scores.get("disgust", 0)
        fear = emotion_scores.get("fear", 0)
        joy = emotion_scores.get("joy", 0)
        sadness = emotion_scores.get("sadness", 0)

        # Determine dominant emotion
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        # Return the formatted response
        return {
            'anger': anger,
            'disgust': disgust,
            'fear': fear,
            'joy': joy,
            'sadness': sadness,
            'dominant_emotion': dominant_emotion
        }, 200  # HTTP 200: OK
    
    else:
        return {"error": "Failed to fetch emotions", "status_code": response.status_code}, response.status_code
