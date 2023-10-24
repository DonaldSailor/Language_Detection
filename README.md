# About

The project consists of two components: a server and a client connected through a REST API. The server performs language detection based on the text provided. For prediction, the xlm-roberta-base-language-detection model is used, which achieves a very high precision for 20 languages. ``` https://huggingface.co/papluca/xlm-roberta-base-language-detection ```
## Getting started

To begin, install the required packages using pip

``` pip install requirements.txt```

## Server

The server's API has two endpoints:

1. /detect - A POST method that detects the language of a single text. It accepts a JSON body in the format {text: str} and returns a JSON response {language: str}

2. /detect_batch - A POST method that detects the language for a larger number of texts. It accepts a JSON body in the format {texts: list[str]} and returns a JSON response {language: list[str]}.

The config.json file allows to change the model to own custom one from HF.
To start the server, should execute the following command in server directory:
``` uvicorn main:app --reload ```

## Evaluation script

The repository also provides the app.py script, which allows language detection from multiple texts in a CSV file. The script enables analysis on raw texts as well as on texts cleansed of emojis. The text analysis revealed that the texts contain many special characters, such as emojis. Therefore, it provides an option to clean the texts from emojis.

```
--data_path: path to the CSV file containing texts
--host: path to the prediction script's endpoint
--result_path: path to where the analysis results are saved
--remove_emoji: if to clean text from emojis
--no-remove_emoji: if to keep emojis in the text
```

Example run
``` python app.py --data_path "texts.csv" --host http://127.0.0.1:8000/detect_batch --no-remove_emoji --result_path res_with_emojis.csv ```

## Analysis

The analysis.ipynb file contains a brief analysis of the places where language detection errors occur.
