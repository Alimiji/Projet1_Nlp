import pandas as pd
import spacy
import json

# Utilisation une stop liste et d' une lemmatisation (approche nommée Baseline-pre-process).
##### Cette fonction permet de prétraiter un texte:lemmatisation et élimination des stop-word
nlp = spacy.load('en_core_web_sm')
def pretraiter_chaine_car(texte):
    # Charger le modèle anglais

    # Traiter le texte
    doc = nlp(texte)
    # Élimination des stop words et lemmatisation
    cleaned_text = " ".join([token.lemma_ for token in doc if not token.is_stop])

    return cleaned_text
