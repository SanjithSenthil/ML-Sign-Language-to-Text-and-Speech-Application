import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
from keras.models import load_model
import numpy as np
from keras.models import load_model
import numpy as np
import time
import os
import sys
from speech import text_to_speech

lang = sys.argv[1]

delay = 4
last_time = time.time()

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
script_directory = os.path.dirname(os.path.abspath(__file__))

# Load the model
model = load_model("Model/keras_Model.h5", compile=False)

# Load the labels
class_names = open("Model/labels.txt", "r").readlines()

detector = HandDetector(maxHands=1)

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

res = ""
result = ""
prev_char = ""

while True:
    current_time = time.time()
    # Grab the webcamera's image for model.
    ret, image = camera.read()
    image = cv2.flip(image,1)
    imageCopy = image.copy()
    hands, _ = detector.findHands(imageCopy)
    imageCopy = cv2.resize(imageCopy, (600, 500))
    
    cv2.putText(imageCopy, "Letter: " + prev_char, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Camera Display", imageCopy)

    if current_time - last_time >= delay:

        if hands:
            
            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            cv2.imshow("Sign Captured", image)

            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalize the image array
            image = (image / 127.5) - 1

            # Predicts the model
            prediction = model.predict(image)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            # Print prediction and confidence score
            print("Class:", class_name[2], end=" ")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            
            prev_char = class_name[2]
            res += class_name[2]
            cv2.putText(imageCopy, "Letter: " + prev_char, (20, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

        else:
            
            # Resize the raw image into (224-height,224-width) pixels
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
            cv2.imshow("Sign Captured", image)
            prev_char = "SPACE"
            res += " "

        last_time = current_time  # Update the last time


    # Exit the loop if 'q', 'j', 'f', 'o', 'r', or spacebar is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('j') or key == ord('f') or key == ord('o') or key == 32:
        break

camera.release()
cv2.destroyAllWindows()

print("Results: " + res)
text_to_speech(res,lang)