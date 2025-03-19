from dotenv import load_dotenv
import os
from google.cloud import vision
from openai import OpenAI

class config:
    def __init__(self):
        load_dotenv()

    def get_google_creds(self):
        return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    def get_openai_creds(self):
        return os.getenv("OPENAI_API_KEY")
    
    def set_google_creds(self):
        if not self.get_google_creds():
            print("Google creds not found")
            return

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.get_google_creds()
    
    def set_openai_creds(self):
        if not self.get_openai_creds():
            print("OpenAI creds not found")
            return 
        
        os.environ["OPENAI_API_KEY"] = self.get_openai_creds()


def detect_text(path):
    """Detects text in the file."""
    
    try:
        client = vision.ImageAnnotatorClient()
    except Exception as e:
        print(f"Error creating ImageAnnotatorClient: {e}")
        return (False, "Error creating ImageAnnotatorClient")

    try:
        with open(path, "rb") as image_file:
            content = image_file.read()
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return (False, f"Error reading file {path}")

    image = vision.Image(content=content)

    try:
        response = client.text_detection(image=image)
    except Exception as e:
        print(f"Error during text detection: {e}")
        return (False, "Error during text detection")

    texts = response.text_annotations
    if len(texts) == 0:
        return (False, "No text detected in the image")
    
    full_text = texts[0].description
    
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return (True, full_text)

def extract_question(text):
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "If the text have any questions extract the question else create a question related to it.",
                },
              
                {
                    "role": "user",
                    "content": text,
                }
            ],
        )
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return "Error during OpenAI API call"

    return completion.choices[0].message.content

def search_web(question):
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-search-preview",
            web_search_options={},
            messages=[

                {
                    "role": "system",
                    "content": "Real time search the web for the answer of the question and keep the answers short straight to point.",
                },

                {
                    "role": "user",
                    "content": question,
                }
            ],
        )
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return "Error during OpenAI API call"

    return completion.choices[0].message.content
