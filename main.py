import os
import urllib
import urllib.request, urllib.parse, urllib.error
import urllib.request
import urllib.error
import json

import pretraitement
import requetes



def encode_query(query):
    # URL-encode the query string
    encoded_query = urllib.parse.quote(query, safe='')
    return encoded_query

# Function to convert JSON file to a dictionary
def json_to_dict(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


### Fonction permettant d'effectuer une requete et de recupérer la réponse
def faire_requete(core, req, rows):

    url = f"http://localhost:8983/solr/{core}/select?indent=true&q=_text_:{req}&rows={rows}&fl=DOCNO,score"

    rep = urllib.request.Request(url)

    with urllib.request.urlopen(rep) as reponse:

        data = reponse.read()

        reponse_json = json.loads(data.decode("utf-8"))

        return reponse_json

#### Fonction permettant d'ecrire les resultats dans le format de trec_eval

def requete_debug_et_enregistrement(requete, core, nom_fichier):
    url = f"http://localhost:8983/solr/{core}/select?defType=lucene&fl=DOCNO%2Cscore&indent=true&q.op=OR&q="
    para = "&rows=1000&useParams=&wt=json"  # Paramètre permettant d'extraire les 1000 documents par requête
    url_complet = url + encode_query("TEXT:"+requete) + para
    #print(url_complet)

    try:
        with urllib.request.urlopen(url_complet) as response:
            print(response)
            response_data = response.read().decode()

            try:
                json_data = json.loads(response_data)
                print(json_data)

                # Enregistrement de la réponse JSON formatée dans un fichier
                with open(nom_fichier, 'w', encoding='utf-8') as file:
                    json.dump(json_data, file, indent=4, ensure_ascii=False)

                print(f"Les données ont été enregistrées dans le fichier '{nom_fichier}'.")

            except json.JSONDecodeError:
                print("La réponse n'est pas au format JSON")
                # Enregistre le texte brut si ce n'est pas du JSON
                with open(nom_fichier, 'w', encoding='utf-8') as file:
                    file.write(response_data)
                print(f"La réponse brute a été enregistrée dans le fichier '{nom_fichier}'.")

    except urllib.error.URLError as e:
        print(f'Erreur lors de l’ouverture de l’URL {url_complet}:', e)

### Fonction permettant d'extraire les resultats dans le format de trec_eval sous forme de liste de resultats
def res_req_trec_eval(nom_core, req_ids, chemin, nom_fichier):
    #re_Bm25_b_

    results_for_trec_eval = []
    for req_id in req_ids:
        chemin_complet = chemin + nom_fichier
        #nom_fichier = f"resultats_requetes_courtes/resultats_/re_Bm25_b_"
        chemin_complet = chemin_complet + req_id + ".json"
        print(chemin_complet)
        #json_dict = json_to_dict(nom_fichier)
        try:
            json_dict = json_to_dict(chemin_complet)
            # Suite de votre code
        except FileNotFoundError:
            print(f"Le fichier {chemin_complet} n'a pas été trouvé.")
        print(json_dict)
        for rank, doc in enumerate(json_dict['response']['docs']):
            line = f"{int(req_id)} Q0 {doc['DOCNO'].strip()} {rank} {doc['score']} {nom_core}"
            results_for_trec_eval.append(line)

    return results_for_trec_eval

##### Fonction permettant de transformer une liste de chaines de caractères en fichier text

def liste_chaine_fichier(liste_chaines, chemin_fichier_sortie):
    # Écrire chaque chaîne dans le fichier, chaque chaîne sur une nouvelle ligne
    with open(chemin_fichier_sortie, 'w') as file:
        for ligne in liste_chaines:
            file.write(ligne + "\n")







url_core = f"http://localhost:8983/solr/Bm25_baseline1/select?defType=lucene&fl=DOCNO%2Cscore&indent=true&q.op=OR&q="



#req = "Antitrust Cases Pending"
#rows = 1000
#nom_fichier = "resultats_requetes_courtes/resultats_Bm25_baseline/re_Bm25_1.json"

#requete_debug_et_enregistrement(req, core, nom_fichier)


############################################################################
##### Extraction des résultats Bm25 baseline, requetes courtes ###########
############################################################################
"""
core = "Bm25_baseline"

Liste_req_courtes1_50 = json_to_dict("requetes_courtes/req_courtes1_50.json")
Liste_req_courtes51_100 = json_to_dict("requetes_courtes/req_courtes51_100.json")
Liste_req_courtes101_150 = json_to_dict("requetes_courtes/req_courtes101_150.json")

for id_req, req in Liste_req_courtes1_50.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Bm25_baseline/re_Bm25_b_" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_courtes51_100.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Bm25_baseline/re_Bm25_b_" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_courtes101_150.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Bm25_baseline/re_Bm25_b_" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)




req_ids = list(Liste_req_courtes1_50.keys()) + list(Liste_req_courtes51_100.keys()) + list(Liste_req_courtes101_150.keys())

#print(req_ids)
chemin = "resultats_requetes_courtes/resultats_Bm25_baseline/"
nom_fichier = "re_Bm25_b_"
results_trec = res_req_trec_eval(core, req_ids, chemin, nom_fichier)
# print(results_trec)
print(len(results_trec))

# Reécupération des résultats  sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_courtes/resultats_Bm25_baseline/resultats_Bm25_b_courtes.txt"

liste_chaine_fichier(results_trec, chemin_fichier_sortie)

"""

############################################################################
##### Extraction des résultats Bm25 baseline, requetes longues ###########
############################################################################

core = "Bm25_baseline"

Liste_req_longues1_50 = json_to_dict("requetes_longues/req_longues1_50.json")
Liste_req_longues51_100 = json_to_dict("requetes_longues/req_longues51_100.json")
Liste_req_longues101_150 = json_to_dict("requetes_longues/req_longues101_150.json")

for id_req, req in Liste_req_longues1_50.items():
    nom_fichier = "resultats_requetes_longues/resultats_Bm25_baseline/re_Bm25_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_longues51_100.items():
    nom_fichier = "resultats_requetes_longues/resultats_Bm25_baseline/re_Bm25_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_longues101_150.items():
    nom_fichier = "resultats_requetes_longues/resultats_Bm25_baseline/re_Bm25_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)




req_ids = list(Liste_req_longues1_50.keys()) + list(Liste_req_longues51_100.keys()) + list(Liste_req_longues101_150.keys())

#print(req_ids)
chemin = "resultats_requetes_longues/resultats_Bm25_baseline/"
nom_fichier = "re_Bm25_b_l"
results_trec = res_req_trec_eval(core, req_ids, chemin, nom_fichier)
# print(results_trec)
print(len(results_trec))

# Reécupération des résultats  sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_longues/resultats_Bm25_baseline/resultats_Bm25_b_longues.txt"

liste_chaine_fichier(results_trec, chemin_fichier_sortie)



############################################################################
##### Extraction des résultats Dfr baseline, requetes courtes ###########
############################################################################
"""

core = "Dfr_baseline"

Liste_req_courtes1_50 = json_to_dict("requetes_courtes/req_courtes1_50.json")
Liste_req_courtes51_100 = json_to_dict("requetes_courtes/req_courtes51_100.json")
Liste_req_courtes101_150 = json_to_dict("requetes_courtes/req_courtes101_150.json")

for id_req, req in Liste_req_courtes1_50.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Dfr_baseline/re_Dfr_b_c" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_courtes51_100.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Dfr_baseline/re_Dfr_b_c" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_courtes101_150.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Dfr_baseline/re_Dfr_b_c" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)




req_ids = list(Liste_req_courtes1_50.keys()) + list(Liste_req_courtes51_100.keys()) + list(Liste_req_courtes101_150.keys())

#print(req_ids)
chemin = "resultats_requetes_courtes/resultats_Dfr_baseline/"
nom_fichier = "re_Dfr_b_c"
results_trec = res_req_trec_eval(core, req_ids, chemin, nom_fichier)
# print(results_trec)
print(len(results_trec))

# Reécupération des résultats  sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_courtes/resultats_Dfr_baseline/resultats_Dfr_b_courtes.txt"

liste_chaine_fichier(results_trec, chemin_fichier_sortie)

"""
############################################################################
##### Extraction des résultats Dfr baseline, requetes longues ###########
############################################################################

"""
core = "Dfr_baseline"


Liste_req_longues1_50 = json_to_dict("requetes_longues/req_longues1_50.json")
Liste_req_longues51_100 = json_to_dict("requetes_longues/req_longues51_100.json")
Liste_req_longues101_150 = json_to_dict("requetes_longues/req_longues101_150.json")

for id_req, req in Liste_req_longues1_50.items():
    nom_fichier = "resultats_requetes_longues/resultats_Dfr_baseline/re_Dfr_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_longues51_100.items():
    nom_fichier = "resultats_requetes_longues/resultats_Dfr_baseline/re_Dfr_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_longues101_150.items():
    nom_fichier = "resultats_requetes_longues/resultats_Dfr_baseline/re_Dfr_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)




req_ids = list(Liste_req_longues1_50.keys()) + list(Liste_req_longues51_100.keys()) + list(Liste_req_longues101_150.keys())

#print(req_ids)
chemin = "resultats_requetes_longues/resultats_Dfr_baseline/"
nom_fichier = "re_Dfr_b_l"
results_trec = res_req_trec_eval(core, req_ids, chemin, nom_fichier)
# print(results_trec)
print(len(results_trec))

# Reécupération des résultats  sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_longues/resultats_Dfr_baseline/resultats_Dfr_b_longues.txt"

liste_chaine_fichier(results_trec, chemin_fichier_sortie)

"""



############################################################################
##### Extraction des résultats Ib baseline, requetes courtes ###########
############################################################################

"""

core = "Ib_baseline"
Liste_req_courtes1_50 = json_to_dict("requetes_courtes/req_courtes1_50.json")
Liste_req_courtes51_100 = json_to_dict("requetes_courtes/req_courtes51_100.json")
Liste_req_courtes101_150 = json_to_dict("requetes_courtes/req_courtes101_150.json")

for id_req, req in Liste_req_courtes1_50.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Ib_baseline/re_Ib_b_c" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_courtes51_100.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Ib_baseline/re_Ib_b_c" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_courtes101_150.items():
    nom_fichier = "resultats_requetes_courtes/resultats_Ib_baseline/re_Ib_b_c"+ str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)




req_ids = list(Liste_req_courtes1_50.keys()) + list(Liste_req_courtes51_100.keys()) + list(Liste_req_courtes101_150.keys())

#print(req_ids)
chemin = "resultats_requetes_courtes/resultats_Ib_baseline/"
nom_fichier = "re_Ib_b_c"
results_trec = res_req_trec_eval(core, req_ids, chemin, nom_fichier)
# print(results_trec)
print(len(results_trec))

# Reécupération des résultats  sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_courtes/resultats_Ib_baseline/resultats_Ib_b_courtes.txt"

liste_chaine_fichier(results_trec, chemin_fichier_sortie)
"""

############################################################################
##### Extraction des résultats Ib baseline, requetes longues     ###########
###########################################################################

"""

core = "Ib_baseline"

Liste_req_longues1_50 = json_to_dict("requetes_longues/req_longues1_50.json")
Liste_req_longues51_100 = json_to_dict("requetes_longues/req_longues51_100.json")
Liste_req_longues101_150 = json_to_dict("requetes_longues/req_longues101_150.json")

for id_req, req in Liste_req_longues1_50.items():
    nom_fichier = "resultats_requetes_longues/resultats_Ib_baseline/re_Ib_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_longues51_100.items():
    nom_fichier = "resultats_requetes_longues/resultats_Ib_baseline/re_Ib_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)

for id_req, req in Liste_req_longues101_150.items():
    nom_fichier = "resultats_requetes_longues/resultats_Ib_baseline/re_Ib_b_l" + str(id_req) + ".json"
    requete_debug_et_enregistrement(req, core, nom_fichier)




req_ids = list(Liste_req_longues1_50.keys()) + list(Liste_req_longues51_100.keys()) + list(Liste_req_longues101_150.keys())

#print(req_ids)
chemin = "resultats_requetes_longues/resultats_Ib_baseline/"
nom_fichier = "re_Ib_b_l"
results_trec = res_req_trec_eval(core, req_ids, chemin, nom_fichier)
# print(results_trec)
print(len(results_trec))

# Reécupération des résultats  sous forme d'un fichier text
chemin_fichier_sortie = "resultats_requetes_longues/resultats_Ib_baseline/resultats_Ib_b_longues.txt"

liste_chaine_fichier(results_trec, chemin_fichier_sortie)

"""

##########################################################################################################
##### Creation des requetes prétraitées (lemmatisées)  à partir des requetes non prétraitées   ###########
##########################################################################################################


### Cette fonction permet de prétraiter les valeurs d'un dictionnaire (lemmatisation)

def pret(dic):

    dic_pret = dict()
    for k,v in dic.items():
        dic_pret[k] = pretraitement.pretraiter_chaine_car(v)

    return dic_pret


#### Fonction permettant de transformer un dictionnaire en fichier json

def dic_json(mon_dict, chemin_fichier):

    with open(chemin_fichier, 'w') as fichier:
        json.dump(mon_dict, fichier, indent=4)  # L'indentation est optionnelle mais rend le fichier plus lisible

"""
Liste_req_courtes1_50 = json_to_dict("requetes_courtes/req_courtes1_50.json")
Liste_req_courtes51_100 = json_to_dict("requetes_courtes/req_courtes51_100.json")
Liste_req_courtes101_150 = json_to_dict("requetes_courtes/req_courtes101_150.json")
Liste_req_longues1_50 = json_to_dict("requetes_longues/req_longues1_50.json")
Liste_req_longues51_100 = json_to_dict("requetes_longues/req_longues51_100.json")
Liste_req_longues101_150 = json_to_dict("requetes_longues/req_longues101_150.json")

##### Création des requetes courtes prétraitées et création des fichiers json correspondants

Liste_req_courtes_pret1_50 = pret(Liste_req_courtes1_50)
Liste_req_courtes_pret51_100 = pret(Liste_req_courtes51_100)
Liste_req_courtes_pret101_150 = pret(Liste_req_courtes101_150)

dic_json(Liste_req_courtes_pret1_50, "requetes_courtes_pret/req_courtes_pret1_50.json")
dic_json(Liste_req_courtes_pret1_50, "requetes_courtes_pret/req_courtes_pret51_100.json")
dic_json(Liste_req_courtes_pret1_50, "requetes_courtes_pret/req_courtes_pret101_150.json")

##### Création des requetes longues prétraitées et création des fichiers json correspondants

Liste_req_longues_pret1_50 = pret(Liste_req_longues1_50)
Liste_req_longues_pret51_100 = pret(Liste_req_longues51_100)
Liste_req_longues_pret101_150 = pret(Liste_req_longues101_150)

dic_json(Liste_req_longues_pret1_50, "requetes_longues_pret/req_longues_pret1_50.json")
dic_json(Liste_req_longues_pret51_100, "requetes_longues_pret/req_longues_pret51_100.json")
dic_json(Liste_req_longues_pret101_150, "requetes_longues_pret/req_longues_pret101_150.json")


"""


###########################################################################
##### Extraction des résultats Bm25 preprocess, requetes courtes     ######
###########################################################################








############################################################################
##### Extraction des résultats Bm25 preprocess,, requetes longues     ######
###########################################################################







###########################################################################
##### Extraction des résultats Dfr preprocess, requetes courtes     #######
###########################################################################









##########################################################################
##### Extraction des résultats Dfr preprocess, requetes longues     #######
###########################################################################







##########################################################################
##### Extraction des résultats Ib preprocess, requetes courtes     ########
###########################################################################







##########################################################################
##### Extraction des résultats Ib preprocess, requetes longues     ########
###########################################################################
