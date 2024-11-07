from deepface import DeepFace

def detect_emotion(image_frame):
    """Detects emotion from a given video frame or image."""
    try:
        analysis = DeepFace.analyze(image_frame, actions=["emotion"])
        return analysis["dominant_emotion"]
    except Exception as e:
        print("Error detecting emotion:", e)
        return "Error"
