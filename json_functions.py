import json
from difflib import get_close_matches

def load(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def load_name(settings_file):
    try:
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            return settings.get('name', 'You')
    except FileNotFoundError:
        return 'You'