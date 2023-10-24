import requests
import json
import argparse
import pandas as pd
import re

def remove_emojis_func(_texts:list[str]) -> list[str]:
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      "]+", re.UNICODE)
    
    return [re.sub(emoj, '', text) for text in _texts]


def run_detection(host_path:str, data_path:str, remove_emoji:bool, result_path:str) -> None:
    texts = pd.read_csv(data_path, header=None, names=['text'])['text'].tolist()

    if remove_emoji:
        texts = remove_emojis_func(texts)

    scores = requests.post(host_path, json={'texts': texts}).json()

    result_table  = pd.DataFrame(scores['language'])

    result_table['text'] = texts

    result_table.to_csv(result_path, index=None)


def main():
    parser = argparse.ArgumentParser(description='Inference arguments')

    parser.add_argument('--data_path', dest='data_path', type=str, required=True)
    parser.add_argument('--host', dest='host_path', type=str, required=True)
    parser.add_argument('--remove_emoji', dest='remove_emoji', type=bool, action=argparse.BooleanOptionalAction)
    parser.add_argument('--result_path', dest='result_path', type=str, required=True)

    args = parser.parse_args()

    run_detection(host_path=args.host_path, data_path=args.data_path, remove_emoji=args.remove_emoji, result_path=args.result_path)
    

if __name__ == '__main__':
    main()