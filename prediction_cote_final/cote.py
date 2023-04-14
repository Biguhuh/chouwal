import pandas as pd
import requests
import time
from datetime import datetime, date, timedelta
import argparse
from os import *



def get_current_date_format():
    today = date.today()
    day = '0' + str(today.day) if today.day < 10 else str(today.day)
    month = '0' + str(today.month) if today.month < 10 else str(today.month)
    year = str(today.year)
    return day + month + year

#recuperer le dictionnaire avec les info sur les cheveaux
def get_response_API_chevaux(R, C):
    today_format = get_current_date_format()
    url = f'https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{today_format}/R{R}/C{C}/participants?specialisation=OFFLINE'
    response = requests.get(url)
    check_response(response)
    return response.json()

#recuperer le dictionnaire avec les info sur la course
def get_response_API_course(R, C):
    today_format = get_current_date_format()
    url = f'https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{today_format}/R{R}/C{C}/'
    response = requests.get(url)
    check_response(response)
    return response.json()

def get_response_API_cheval_internet(R, C):
    today_format = get_current_date_format()
    url = f'https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{today_format}/R{R}/C{C}/participants?specialisation=INTERNET'
    response = requests.get(url)
    check_response(response)
    return response.json()

def check_response(response):
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code}")
                  
                  
def heure(R,C):
    heure_actuelle = datetime.now()
    heure_depart_course = datetime.fromtimestamp(get_response_API_course(R,C)['heureDepart'] / 1000)
    depart_course_moin_5_minutes = heure_depart_course - timedelta(minutes=5)
    heure_course_moin_30_sec = heure_depart_course - timedelta(seconds=30)
    
    return heure_actuelle, depart_course_moin_5_minutes, heure_depart_course, heure_course_moin_30_sec


def calculer_temps_restant(heure_actuelle, heure_depart_course):
    heures, reste = divmod((heure_depart_course - heure_actuelle).total_seconds(), 3600)
    minutes, secondes = divmod(reste, 60)
    temps_restant = f"{int(heures)}h {int(minutes)}m {int(secondes)}s"
    return temps_restant

              
                                
def recuperer_les_cote_course_uniquement_en_ligne(R,C, durée_actualisation_cote):
    
    reponce_course = get_response_API_course(R,C)
    reponce_cheval = get_response_API_cheval_internet(R,C)
    
    if not (reponce_course and reponce_cheval):
        return None
     
    data = {}
    for cheval in reponce_cheval['participants']:
        nom_cheval = cheval['nom']
        data[nom_cheval] = []
        
    heure_actuelle, _ , heure_depart_course, heure_depart_course_moin_30_sec = heure(R,C)
    
    temps_restant_list = []
    heure_liste = []
    
    while heure_actuelle < heure_depart_course_moin_30_sec:
        heure_actuelle = datetime.now()
        reponce_cheval = get_response_API_cheval_internet(R,C)
        for cheval in reponce_cheval['participants']:
            nom_cheval = cheval['nom']
            
            if not cheval['statut'] == 'PARTANT':
                data[nom_cheval].append(None)
            else: 
                cote = cheval['dernierRapportDirect']['rapport']
                data[nom_cheval].append(cote)
                
        temps_restant = calculer_temps_restant(heure_actuelle, heure_depart_course)
        temps_restant_list.append(temps_restant)
        heure_liste.append(heure_actuelle)
        
        print(f"Cotes mises à jour à {heure_actuelle.strftime('%H:%M:%S')}")
        
        # Si la course démarre dans moins de 15 minutes, mettre à jour les cotes toutes les X secondes
        if (heure_depart_course - heure_actuelle).total_seconds() < 15 * 60:
            durée_actualisation_cote = 30
        #dans tout les cas le code s'arrette 5 minutes avant le depart de la course (while heure_actuelle < depart_course_moin_5_minutes:)
        time.sleep(durée_actualisation_cote)
        
    df_cote_en_ligne = pd.DataFrame(data)
    df_cote_en_ligne['temps_restant'] = temps_restant_list
    df_cote_en_ligne['heure'] = heure_liste
    
    return df_cote_en_ligne



def recuperer_les_cote_course_hors_ligne_et_en_ligne(R,C, durée_actualisation_cote):
    
    reponce_course = get_response_API_course(R,C)
    reponce_cheval = get_response_API_chevaux(R,C)
    reponce_cheval_internet = get_response_API_cheval_internet(R,C)
    
    if not (reponce_course and reponce_cheval and reponce_cheval_internet):
        return None
     
    data_hors_ligne = {}
    for cheval in reponce_cheval['participants']:
        nom_cheval = cheval['nom']
        data_hors_ligne[nom_cheval] = []
        
    data_en_ligne = {}
    for cheval in reponce_cheval_internet['participants']:
        nom_cheval = cheval['nom']
        data_en_ligne[nom_cheval] = []
        
    heure_actuelle, depart_course_moin_5_minutes, heure_depart_course, heure_depart_course_moin_30_sec = heure(R,C)
    
    temps_restant_list = []
    heure_liste = []
    
    while heure_actuelle < depart_course_moin_5_minutes:
        heure_actuelle = datetime.now()
        reponce_cheval = get_response_API_chevaux(R,C)
        
        for cheval in reponce_cheval['participants']:
            nom_cheval = cheval['nom']
            
            if not cheval['statut'] == 'PARTANT':
                data_hors_ligne[nom_cheval].append(None)
            else: 
                cote = cheval['dernierRapportDirect']['rapport']
                data_hors_ligne[nom_cheval].append(cote)
        
        for cheval in reponce_cheval_internet['participants']:
            nom_cheval = cheval['nom']
            
            if not cheval['statut'] == 'PARTANT':
                data_en_ligne[nom_cheval].append(None)
            else: 
                cote = cheval['dernierRapportDirect']['rapport']
                data_en_ligne[nom_cheval].append(cote)        
                
        temps_restant = calculer_temps_restant(heure_actuelle, heure_depart_course)
        temps_restant_list.append(temps_restant)
        heure_liste.append(heure_actuelle)
        
        print(f"Cotes mises à jour à {heure_actuelle.strftime('%H:%M:%S')}")
        
        # Si la course démarre dans moins de 15 minutes, mettre à jour les cotes toutes les X secondes
        if (heure_depart_course - heure_actuelle).total_seconds() < 15 * 60:
            durée_actualisation_cote = 30
        #dans tout les cas le code s'arrette 5 minutes avant le depart de la course (while heure_actuelle < depart_course_moin_5_minutes:)
        time.sleep(durée_actualisation_cote)
        
    df_cote_en_ligne = pd.DataFrame(data_en_ligne)
    df_cote_en_ligne['temps_restant'] = temps_restant_list
    df_cote_en_ligne['heure'] = heure_liste
    
    df_cote_hors_ligne = pd.DataFrame(data_hors_ligne)
    df_cote_hors_ligne['temps_restant'] = temps_restant_list
    df_cote_hors_ligne['heure'] = heure_liste
    
    return df_cote_hors_ligne, df_cote_en_ligne


def creer_les_y(R, C):
    reponse_course = get_response_API_course(R, C)
    reponse_cheval = get_response_API_chevaux(R, C)
    reponse_cheval_internet = get_response_API_cheval_internet(R, C)

    if not (reponse_course and reponse_cheval and reponse_cheval_internet):
        return None

    data_hors_ligne = {}
    for cheval in reponse_cheval['participants']:
        nom_cheval = cheval['nom']
        if not cheval['statut'] == 'PARTANT':
            data_hors_ligne[nom_cheval] = None
        else:
            cote = cheval['dernierRapportDirect']['rapport']
            data_hors_ligne[nom_cheval] = cote

    data_en_ligne = {}
    for cheval in reponse_cheval_internet['participants']:
        nom_cheval = cheval['nom']
        if not cheval['statut'] == 'PARTANT':
            data_en_ligne[nom_cheval] = None
        else:
            cote = cheval['dernierRapportDirect']['rapport']
            data_en_ligne[nom_cheval] = cote
            
    df_y_en_ligne = pd.DataFrame(data_en_ligne, index=[0])
    df_y_hors_ligne = pd.DataFrame(data_hors_ligne, index=[0])
    
    if reponse_course['courseExclusiveInternet'] == True:
        return df_y_en_ligne
    else:
        return df_y_hors_ligne, df_y_en_ligne

        
       
if  __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Obtenir les cotes de chaque cheval toutes les X secondes.avant les 10 dernières minutes avant la course.')
    parser.add_argument('R', type=str, help='Le code/numéro de la réunion.')
    parser.add_argument('C', type=str, help='Le code/numéro de la course.')
    parser.add_argument('X', type = int, help='Le nombre de secondes entre chaque actualisation des cotes.')
    args = parser.parse_args()
    
    if not path.exists(f'cote/{datetime.now().strftime("%Y-%m-%d")}'):
        makedirs(f'cote/{datetime.now().strftime("%Y-%m-%d")}')
        
    if not path.exists(f'y/{datetime.now().strftime("%Y-%m-%d")}'):
        makedirs(f'y/{datetime.now().strftime("%Y-%m-%d")}')

    
    # Appeler la fonction avec les arguments de ligne de commande
    if get_response_API_course(args.R,args.C)['courseExclusiveInternet'] == True:
        df_cote_en_ligne = recuperer_les_cote_course_uniquement_en_ligne(args.R, args.C, args.X)
        
        df_cote_en_ligne.to_parquet(f'cote/{datetime.now().strftime("%Y-%m-%d")}/cote_course_uniquement_en_ligne_R{args.R}C{args.C}.parquet')
        
        y_en_ligne = creer_les_y(args.R, args.C)
        
        y_en_ligne.to_parquet(f'y/{datetime.now().strftime("%Y-%m-%d")}/y_uniquement_en_linge_R{args.R}C{args.C}.parquet')
        
        print(df_cote_en_ligne)
        
        
    else:
        df_cote_horsligne, df_cote_en_ligne = recuperer_les_cote_course_hors_ligne_et_en_ligne(args.R, args.C, args.X)
        
        df_cote_en_ligne.to_parquet(f'cote/{datetime.now().strftime("%Y-%m-%d")}/cote_course\"normal\"_en_ligne_R{args.R}C{args.C}.parquet')
        df_cote_horsligne.to_parquet(f'cote/{datetime.now().strftime("%Y-%m-%d")}/cote_course\"normal\"_hors_ligne_R{args.R}C{args.C}.parquet')
        
        y_hors_ligne, y_en_ligne = creer_les_y(args.R, args.C)
        
        y_hors_ligne.to_parquet(f'y/{datetime.now().strftime("%Y-%m-%d")}/y_hors_ligne_R{args.R}C{args.C}.parquet')
        y_en_ligne.to_parquet(f'y/{datetime.now().strftime("%Y-%m-%d")}/y_en_ligne_R{args.R}C{args.C}.parquet')
        
        print(df_cote_en_ligne, df_cote_horsligne)
        

    
    
    
    
    
