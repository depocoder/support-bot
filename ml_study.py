import json
import os
import argparse

from dotenv import load_dotenv
import dialogflow_v2beta1
import dialogflow_v2


def format_json():
    with open("questions.json", "r", encoding='utf-8') as my_file:
        questions = json.load(my_file)
    intents = []
    title_questions = [title for title in questions]
    for title in title_questions:
        intents.append({
            "display_name": title,
            "messages": [{
                'text': {
                    "text": [questions[title]['answer']]},

                }],
            "training_phrases": [{
                "parts": [{"text": question}]} \
                for question in questions[title]['questions']]
        })
    return intents


def add_intents(project_id):
    intents = format_json()
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(project_id)
    for intent in intents:
        client.create_intent(parent, intent)


def train_dialogflow(project_id):
    client = dialogflow_v2beta1.AgentsClient()
    parent = client.project_path(project_id)
    client.train_agent(parent)


def create_argparse():
    parser = argparse.ArgumentParser(
        description='Cкрипт позволяет загрузить свои intent на dialogflow')

    parser.add_argument(
        '--skip_intent', action="store_true",
        help='не загружать intent')

    parser.add_argument(
        '--skip_train', action="store_true",
        help='не обучать dialogflow')

    return parser


def main():
    load_dotenv()
    project_id = os.getenv("PROJECT_ID")
    parser = create_argparse()
    args = parser.parse_args()

    if not args.skip_intent:
        add_intents(project_id)
    if not args.skip_train:
        train_dialogflow(project_id)


if __name__ == "__main__":
    main()
