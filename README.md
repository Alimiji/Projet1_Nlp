les résultats d’une
étude comparative des map-scores obtenus sur trois schémas de
pondération distincts de mon système RI. Je présenterai leur
performance sur deux ensembles de données de test de TREC : l’un
constitué de données non modifiées, désigné comme ’baseline’, et
l’autre comprenant des données ayant subi un prétraitement, ou
’baseline-preprocess’.



Ce projet a pour objectif de développer un système de recherche d'information sur les documents de TREC, et de 
comparer les différents métriques (BM25, TfIdf, )  de ce système.



METHODOLOGIE:


Installation de cloud Solr et pysolr.

Extraction et formattage des données de Trec en json
Ajout et configuration des schémas de pondération selon
l’approche baseline d’une part et l’approche
baseline-preprocess d’autre part, dans cloud solr.


Indexation des documents selon l’approche baseline d’une part
et l’approche baseline-preprocess d’autre part, dans cloud solr.
Envoie des requêtes et récupération des résultats de requêtes
selon le type de requête (courte et longue) et l’approche
(baseline et baseline-preprocess): On obtient ainsi, 12 résultats
de requêtes.


Évaluation du système RI avec le métrique map, en évaluant
chacune des 12 résultats de requêtes et en utilisant les
jugements de pertinence, avec l’application trec-eval.


https://subscription.packtpub.com/book/data/9781783553150/
1/ch01lvl1sec22/changing-similarity 5/8
