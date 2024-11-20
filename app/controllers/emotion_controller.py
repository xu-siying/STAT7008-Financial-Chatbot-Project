# from flask import request, jsonify
# import cv2
# import numpy as np
# from deepface import DeepFace
# import base64

# def analyze_emotion():
#     data = request.get_json()
#     image_data = data.get("image")

#     # Decode the base64 image
#     image_bytes = base64.b64decode(image_data.split(",")[1])
#     np_image = np.frombuffer(image_bytes, np.uint8)
#     frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

#     try:
#         # Detect emotion using DeepFace
#         analysis = DeepFace.analyze(frame, actions=["emotion"])
#         emotion = analysis["dominant_emotion"]
#         return jsonify({"emotion": emotion})
#     except Exception as e:
#         print("Error detecting emotion:", e)
#         return jsonify({"error": "Could not analyze emotion"}), 500
