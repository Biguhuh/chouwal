import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def get_data():
    df = pd.read_csv('data/2022_chouwal.csv')
    return df



def drop_the_non_frensh_races(df):
    # df['country'].apply(strip, axis=1) peut etre utile un jour
    df = df[df.country == "FR "]
    return df


def drop_the_leackage(df): # permet de supprimer les colonnes qui donne des info qu'on est pas senser avoir avant la course
    pass



################################les 3 foction suivante serve a gerer les nan des colone numérique###############################################

def search_percentage_nan_egla_to_cl(df, percertage=11): #permet de supprimer les colonnes qui ont un pourcentage de nan cimilaire a cl
    lst_futur_colums = []
    for i in df.columns:
        if df[i].isna().sum()/len(df[i]) * 100 <= percertage and df[i].isna().sum()/len(df[i]) * 100 != 0:
            lst_futur_colums.append(i)
    return lst_futur_colums


def drop_percentage_nan(df, percertage=90): # permet de supprimer les colonnes qui ont plus de 90% de valeurs manquantes
    # lst_futur_colums = []   #retirer les # pour imprimer les colonnes suprimer
    for i in df.columns:
        if df[i].isna().sum()/len(df[i]) * 100 > percertage:
            # lst_futur_colums.append(i)
            df.drop(i, axis=1, inplace=True)
    # print(f'les colonnes supprimées sont : {lst_futur_colums}')
    return df

def colums_percentage_nan_dif_0(df): # permet de voir les colonnes qui ont encore des NAN
    lst_col = df.columns[:]
    for i in lst_col:
        if df[i].isna().sum()/len(df[i]) * 100 != 0:
            print(f'{i} : {df[i].isna().sum()/len(df[i]) * 100}')

###############################################################################################################################################

def created_y(df):
    # on suprime les non numerique
    for i in range(len(df['cl'])):
        if not str(df['cl'][i]).isnumeric():
            df['cl'][i] = 0
    
    # tous les placés (podiums) prennent la valeur 1
    for i in range(len(df['cl'])):
        if int(df['cl'][i]) < 4:
            df['cl'][i] = 1
    
    # tous les hors podium prennent la valeur 0
    for i in range(len(df['cl'])):
        if int(df['cl'][i]) > 1:
            df['cl'][i] = 0
    
    return df

###################################################Gestion des colonnes non numérique#####################################################

def drop_useless_obj_columns(df):
    
    df = df.drop(['cheval', 'musiqueche', 'musiquept','musiquejoc',
                  'musiqueent','hippo','dernierhippo','dernierJoc',
                  'dernierEnt','dernierProp','proprietaire','createdat',
                  'updatedat','devise','coat','id.1','age.1','jour.1',
                  'comp.1','typec.1','hippo.1','dist.1','devise.1',
                  'url','createdAt','condi','arriv','heure','pere',
                  'mere','derniereplace','jour','prixnom','sex'], axis=1, inplace=True) 
    
    return df


###########################################################################################################################################


def X_y(df):
    y = df['cl']
    X = df.drop('cl', axis=1, inplace=True)
    return X, y

def split_train_test(X, y ,test_size=0.3, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, 
                                                        random_state=random_state)
    
    return X_train, X_test, y_train, y_test


def pipeline_preprocessing(df):
    pass



def final_preprocessing(df):
    
    df = drop_the_non_frensh_races(df)
    df = drop_the_leackage(df)
    df = drop_percentage_nan(df)
    df = drop_useless_obj_columns(df)
    df = created_y(df)
    
    X, y = X_y(df)
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    
    pipeline_preprocessing(df)
    
    return df, X_train, X_test, y_train, y_test