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



def drop_percentage_nan(df, percertage=90):
    # lst_futur_colums = []   #retirer les # pour imprimer les colonnes suprimer
    for i in df.columns:
        if df[i].isna().sum()/len(df[i]) * 100 > percertage:
            # lst_futur_colums.append(i)
            df.drop(i, axis=1, inplace=True)
    # print(f'les colonnes supprimées sont : {lst_futur_colums}')
    return df



def created_y(df):
    df = df.dropna(subset=['cl'], inplace=True)
    
    # on convertit toutes les valeurs en valeur int
    mask = df['cl'].str.isnumeric()
    df['cl'][mask == False] = 0
    df['cl'] = pd.to_numeric(df['cl'], errors='coerce') 
    
    # tous les placés (podiums) prennent la valeur 1
    mask1 = df['cl'] < 4
    df['cl'][mask1 == True] = 1 
    
    # tous les hors podium prennent la valeur 0
    mask2 = df['cl'] > 1
    df['cl'][mask2 == True] = 0
    
    return df


def drop_useless_obj_columns(df):
    
    df = df.drop(['cheval', 'musiqueche', 'musiquept','musiquejoc',
                  'musiqueent','hippo','dernierhippo','dernierJoc',
                  'dernierEnt','dernierProp','proprietaire','createdat',
                  'updatedat','devise','coat','id.1','age.1','jour.1',
                  'comp.1','typec.1','hippo.1','dist.1','devise.1',
                  'url','createdAt','condi','arriv','heure','pere',
                  'mere','derniereplace','jour','prixnom','sex'], axis=1, inplace=True)
    
    return df

def X_y(df):
    y = df['cl']
    X = df.drop('cl', axis=1, inplace=True)
    return X, y

def split_train_test(X, y ,test_size=0.3, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, 
                                                        random_state=random_state)
    
    return X_train, X_test, y_train, y_test


def pipeline_preprocessing(df):
    