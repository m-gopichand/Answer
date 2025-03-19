# ScanQuery

ScanQuery is a tool that captures images from your webcam, detects text within the images, extracts questions, and searches the web for answers.

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/m-gopichand/ScanQuery.git
    cd ScanQuery
    ```

2. **Install required packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Setup the API Keys:**

    Create a file named `.env` in the root directory of the project and add the following lines to it:

    ```env
    GOOGLE_APPLICATION_CREDENTIALS="path/to/yourcredentialsjson"
    OPENAI_API_KEY="yourapikey"
    ```

## Usage

1. **Run the application:**

    ```sh
    python main.py
    ```

2. **Capture images:**

    - Press `Space` to capture an image.
    - Press `Esc` to exit the application.

## Working

1. The application captures images from the webcam.
2. The text is detected from the images using the Google Cloud Vision API.
3. The questions are extracted from the detected text using the OpenAI API.
4. The questions are searched on the web using the gpt-4o-search-preview API.
