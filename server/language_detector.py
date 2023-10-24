from transformers import pipeline

class LanguageDetector:
    def __init__(self, model):
        self.detector = pipeline(model)


    def detect(self, texts_list):
        results = self.detector(texts_list)