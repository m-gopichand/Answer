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
    
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
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

    return completion.choices[0].message.content

def search_web(question):
    client = OpenAI()
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

    return completion.choices[0].message.content

