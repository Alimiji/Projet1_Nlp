import os
import urllib.request, urllib.parse, urllib.error
import json
import requetes

## Extraction des requetes courtes et longues sous forme de json

"""
# Chemin vers le fichier texte
chemin_fichier1_50 = "TRECAP88-90/Topics-requetes/topics.1-50.txt"
chemin_fichier51_100 = "TRECAP88-90/Topics-requetes/topics.51-100.txt"
chemin_fichier101_150 = "TRECAP88-90/Topics-requetes/topics.101-150.txt"

# Extraction des données d'un fichier


def extraire_donnee(nom_fichier):

    # Ouvrir le fichier en mode lecture

    with open(nom_fichier, 'r') as fichier:
        # Lire chaque ligne du fichier
        donnees = fichier.readlines()

    return " ".join(donnees)

def dictio_json(dictio, chemin_fichier_sortie):

    with open(chemin_fichier_sortie, 'w') as fichier:
        json.dump(dictio, fichier, indent=4)  # L'indentation est pour une meilleure lisibilité du fichier

# Extraction des données requetes de chaque fichier sous forme de chaine de caractères

donnee_req1_50 = extraire_donnee(chemin_fichier1_50)
donnee_req51_100 = extraire_donnee(chemin_fichier51_100)
donnee_req101_150 = extraire_donnee(chemin_fichier101_150)

# Extraction des requetes courtes sous forme de dictionnaire

req_courtes_dictio1_50  = requetes.extraire_requetes_courtes(donnee_req1_50)
#print(req_courtes_dictio1_50)
req_courtes_dictio51_100  = requetes.extraire_requetes_courtes(donnee_req51_100)
req_courtes_dictio101_150  = requetes.extraire_requetes_courtes(donnee_req101_150)

# Enregistrement des requetes courtes sous forme de ficchier json

chemin_fichier_sortie1_50 = "requetes_courtes/req_courtes1_50.json"
chemin_fichier_sortie51_100 = "requetes_courtes/req_courtes51_100.json"
chemin_fichier_sortie101_150 = "requetes_courtes/req_courtes101_150.json"


dictio_json(req_courtes_dictio1_50, chemin_fichier_sortie1_50)
dictio_json(req_courtes_dictio51_100, chemin_fichier_sortie51_100)
dictio_json(req_courtes_dictio101_150, chemin_fichier_sortie101_150)

# Extraction des requetes longues sous forme de dictionnaire

req_longues_dictio1_50  = requetes.extraire_requetes_longues(donnee_req1_50)
req_longues_dictio51_100  = requetes.extraire_requetes_longues(donnee_req51_100)
req_longues_dictio101_150  = requetes.extraire_requetes_longues(donnee_req101_150)

# Enregistrement des requetes longues sous forme de ficchier json

chemin_fichier_sortie1_50 = "requetes_longues/req_longues1_50.json"
chemin_fichier_sortie51_100 = "requetes_longues/req_longues51_100.json"
chemin_fichier_sortie101_150 = "requetes_longues/req_longues101_150.json"

dictio_json(req_longues_dictio1_50, chemin_fichier_sortie1_50)
dictio_json(req_longues_dictio51_100, chemin_fichier_sortie51_100)
dictio_json(req_longues_dictio101_150, chemin_fichier_sortie101_150)


"""


def encode_query(query):
    # URL-encode the query string
    encoded_query = urllib.parse.quote(query, safe='')
    return encoded_query


### Envoie des requetes courtes

nom_json = ["requetes_courtes1_50.json", "requetes_courtes51_100.json", "requetes_courtes101_150.json"]

chemin_fichier = "requetes_courtes/" + nom_json[0]

contenu = dict()

#contenu = json.loads(chemin_fichier,encoding='utf-8')

with open(chemin_fichier, 'r') as fichier:
    contenu = json.load(fichier)

print(contenu)

schema = "Bm25_baseline"

url = "http://localhost:8983/solr/Bm25_baseline1/select?defType=lucene&facet=true&fl=id_doc%2Cscore&indent=true&q.op=OR&q=text%3A%20description%20Document%20discusses%20pending%20antitrust%20case&rows=1000&useParams=&wt=json"
#####  http://localhost:8983/solr/Bm25_baseline1/select?defType=lucene&facet=true&fl=id_doc%2Cscore&indent=true&q.op=OR&text%3Adescription%20Document%20discusses%20pending%20antitrust%20case&rows=1000&useParams=&wt=json


# http://localhost:8983/solr/Bm25_baseline1/select?defType=lucene&facet=true&fl=id_doc%2Cscore&indent=true&q.op=OR&q=text%3A%20description%20Document%20discusses%20pending%20antitrust%20case&rows=1000&useParams=&wt=json
#fhand = urllib.request.urlopen(url_Bm25_baseline + encode_query(q) + para) #"/q=text:"+contenu["1"])

#fhand = urllib.request.urlopen(url)

#print(fhand)

#print(url_Bm25_baseline + encode_query(q) + para)


##### Fonction permettant de convertir un fichier json en dictionnaire

# Function to convert JSON file to a dictionary
def json_to_dict(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


##### Fonction permettant d'envoyer les requetes et de récupérer les 1000 premiers résultats sous
##### la forme d'un fichier json


para = "&rows=1000&useParams=&wt=json"


def requete_resultat(requete, url, file_name):

    url = url + encode_query(requete) + para

    fhand = urllib.request.urlopen(url + encode_query(requete) + para)

    with open(file_name, 'w') as file:
        rank = 0
        for line in fhand:
            decoded_line = line.decode()
            rank += 1
            file.write(decoded_line)

#### Fonction permettant de récupérer tous les résultats de tous les requetes en json

def tous_requetes_resultats(url, dossier_res, Liste_files, nom_core, type_req):

    for f in Liste_files:

        d = json_to_dict(f)
        # Récuperation des résultats pour chaque requête

        for q_id, q in d.items():
            file_name = dossier_res + "/res_" + nom_core + "_" + q_id + "_" + type_req + ".json"
            requete_resultat(q, url, file_name)



# Chemin vers le dossier contenant les fichiers resultats JSON pour les requêtes courtes

json_folder_req_courtes = 'requetes_courtes'

# Fonction pour parcourir tous les fichiers JSON dans un dossier et les convertir en dictionnaires
def process_json_files(json_folder):
    json_dicts = []
    for file_name in os.listdir(json_folder):
        if file_name.endswith('.json'):
            file_path = os.path.join(json_folder, file_name)
            with open(file_path, 'r') as file:
                json_dicts.append(json.load(file))
    return json_dicts


##### Fonction permettant de déterminer l'ensemble de tous les résultats dans le format de trec_eval

def res_req_trec_eval(json_dicts, nom_core):

    results_for_trec_eval = []
    query_id = 0
    for data in json_dicts:
        query_id += 1
        for rank, doc in enumerate(data['response']['docs']):
            line = f"{query_id} Q0 {doc['id_doc'][0]} {rank} {doc['score']} {nom_core}"
            results_for_trec_eval.append(line)

    return results_for_trec_eval

##### Fonction permettant de transformer une liste de chaines de caractères en fichier text

def liste_chaine_fichier(liste_chaines, chemin_fichier_sortie):
    # Écrire chaque chaîne dans le fichier, chaque chaîne sur une nouvelle ligne
    with open(chemin_fichier_sortie, 'w') as file:
        for ligne in liste_chaines:
            file.write(ligne + "\n")




### Détermination et récupération des résultats Bm25_baseline pour les requetes courtes

url_Bm25_baseline = "http://localhost:8983/solr/Bm25_baseline1/select?defType=lucene&facet=true&fl=id_doc%2Cscore&indent=true&q.op=OR&q="

url = url_Bm25_baseline + "text:"
dossier_res = "resultats_requetes_courtes/resultats_Bm25_baseline"
Liste_files = ["requetes_courtes/requetes_courtes1_50.json", "requetes_courtes/requetes_courtes51_100.json", "requetes_courtes/requetes_courtes101_150.json"]
nom_core = "Bm25_baseline"
type_req = "courte"

tous_requetes_resultats(url, dossier_res, Liste_files, nom_core, type_req)

# Récupération des résultats de tous les requetes courtes sous forme d'un dictionnaire
json_folder = "resultats_requetes_courtes/resultats_Bm25_baseline"

json_dicts = process_json_files(json_folder)

#print(json_dicts)

# Récupération des résultats sous la forme de trec_eval en liste de chaines de caractères

resultat_trec_eval = res_req_trec_eval(json_dicts, nom_core)

#print(resultat_trec_eval)

# Reécupération des résultats sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_courtes/resultats_Bm25_baseline/resultats_Bm25_baseline_courtes.txt"

liste_chaine_fichier(resultat_trec_eval, chemin_fichier_sortie)


##### Requetes longues Bm5_baseline    #####


### Détermination et récupération des résultats Bm25_baseline pour les requetes longues

"""
# The encoded query string
encoded_query = "Airbus%20Subsidies%20Description%20Document%20will%20discuss%20government%20assistance%20to%20Airbus%20Industrie%2C%20or%20mention%20a%20trade%20dispute%20between%20Airbus%20and%20a%20U%20S%20aircraft%20producer%20over%20the%20issue%20of%20subsidies"

# Decoding the query string
decoded_query = urllib.parse.unquote(encoded_query)
decoded_query
"""

url_Bm25_baseline = "http://localhost:8983/solr/Bm25_baseline1/select?defType=lucene&facet=true&fl=id_doc%2Cscore&indent=true&q.op=OR&q="

url = url_Bm25_baseline + "text:"
dossier_res = "resultats_requetes_longues/resultats_Bm25_baseline"
Liste_files = ["requetes_longues/req_longues1_50.json", "requetes_longues/req_longues51_100.json", "requetes_longues/req_longues101_150.json"]
#Liste_files = ["requetes_longues/requetes_longues1_150.json"]
nom_core = "Bm25_baseline"
type_req = "longue"

tous_requetes_resultats(url, dossier_res, Liste_files, nom_core, type_req)

# Récupération des résultats de tous les requetes courtes sous forme d'un dictionnaire
json_folder = "resultats_requetes_longues/resultats_Bm25_baseline"

json_dicts = process_json_files(json_folder)

#print(json_dicts)

# Récupération des résultats sous la forme de trec_eval en liste de chaines de caractères

resultat_trec_eval = res_req_trec_eval(json_dicts, nom_core)

#print(resultat_trec_eval)

# Reécupération des résultats sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_longues/resultats_Bm25_baseline/resultats_Bm25_baseline_longues.txt"

liste_chaine_fichier(resultat_trec_eval, chemin_fichier_sortie)

##### Détermination et récupération des résultats Bm25_preprocess pour les requetes courtes et longues


url_Bm25_preprocess = "http://localhost:8983/solr/Bm25_preprocess1/select?defType=lucene&facet=true&fl=id_doc%2Cscore&indent=true&q.op=OR&q="

url = url_Bm25_preprocess + "text:"
dossier_res = "resultats_requetes_courtes/resultats_Bm25_preprocess"
Liste_files = ["requetes_courtes/requetes_courtes1_50.json", "requetes_courtes/requetes_courtes51_100.json", "requetes_courtes/requetes_courtes101_150.json"]
nom_core = "Bm25_preprocess"
type_req = "courte"

tous_requetes_resultats(url, dossier_res, Liste_files, nom_core, type_req)

# Récupération des résultats de tous les requetes courtes sous forme d'un dictionnaire
json_folder = "resultats_requetes_courtes/resultats_Bm25_preprocess"

json_dicts = process_json_files(json_folder)

#print(json_dicts)

# Récupération des résultats sous la forme de trec_eval en liste de chaines de caractères

resultat_trec_eval = res_req_trec_eval(json_dicts, nom_core)

#print(resultat_trec_eval)

# Reécupération des résultats sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_courtes/resultats_Bm25_preprocess/resultats_Bm25_preprocess_courtes.txt"

liste_chaine_fichier(resultat_trec_eval, chemin_fichier_sortie)


##### Requetes longues Bm5_preprocess    #####


### Détermination et récupération des résultats Bm25_baseline pour les requetes longues

"""
# The encoded query string
encoded_query = "Airbus%20Subsidies%20Description%20Document%20will%20discuss%20government%20assistance%20to%20Airbus%20Industrie%2C%20or%20mention%20a%20trade%20dispute%20between%20Airbus%20and%20a%20U%20S%20aircraft%20producer%20over%20the%20issue%20of%20subsidies"

# Decoding the query string
decoded_query = urllib.parse.unquote(encoded_query)
decoded_query
"""

url_Bm25_preprocess = "http://localhost:8983/solr/Bm25_preprocess1/select?defType=lucene&facet=true&fl=id_doc%2Cscore&indent=true&q.op=OR&q="

url = url_Bm25_preprocess  + "text:"
dossier_res = "resultats_requetes_longues/resultats_Bm25_preprocess"
Liste_files = ["requetes_longues/req_longues1_50.json", "requetes_longues/req_longues51_100.json", "requetes_longues/req_longues101_150.json"]
#Liste_files = ["requetes_longues/requetes_longues1_150.json"]
nom_core = "Bm25_preprocess"
type_req = "longue"

tous_requetes_resultats(url, dossier_res, Liste_files, nom_core, type_req)

# Récupération des résultats de tous les requetes courtes sous forme d'un dictionnaire
json_folder = "resultats_requetes_longues/resultats_Bm25_preprocess"

json_dicts = process_json_files(json_folder)

#print(json_dicts)

# Récupération des résultats sous la forme de trec_eval en liste de chaines de caractères

resultat_trec_eval = res_req_trec_eval(json_dicts, nom_core)

#print(resultat_trec_eval)

# Reécupération des résultats sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_longues/resultats_Bm25_preprocess/resultats_Bm25_preprocess_longues.txt"

liste_chaine_fichier(resultat_trec_eval, chemin_fichier_sortie)


