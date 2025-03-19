import cv2 
import os
import shutil
from openai import OpenAI
from utils import config, detect_text, search_web, extract_question


## Configuring the environment variables
config = config()
config.set_google_creds()
config.set_openai_creds()
os.makedirs("cache", exist_ok=True)


camera = cv2.VideoCapture(0)
if not camera.isOpened():
     print("Error opening the camera")

image_counter = 0

while True:
    res, frame = camera.read()
    if not res: print("Failed to read the frame")

    cv2.imshow("test", frame)
    k = cv2.waitKey(1)
    

    if k % 256 == 27:  # Escape 
        print("Escape pressed clearing cache and closing")
        shutil.rmtree("cache")                                                                                                                                                                           
        print("Bye!!")
        break

    if k % 256 == 32:  # Space 
        image_name = "frame_{}.png".format(image_counter)
        cv2.imwrite(os.path.join("cache", image_name),  frame)
        have_text, question = detect_text(os.path.join("cache", image_name))
        if have_text:
            process_ques = extract_question(question)
            print("Question:{}".format(process_ques))
            print("Answer:{}".format(search_web(process_ques)))
        image_counter += 1

camera.release()
cv2.destroyAllWindows()