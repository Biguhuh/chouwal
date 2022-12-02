from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_selector, ColumnTransformer, make_column_transformer
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd

def read_raw_data():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    # path = os.pathjoin('/Users/bastiengiudicelli/code/Biguhuh/chouwal/chouwal/PMU/data/2022_chouwal.csv')
    df  = pd.read_csv('/Users/bastiengiudicelli/code/Biguhuh/chouwal/chouwal/PMU/data/2022_chouwal.csv')

    # Proportion of non_raced races
    non_raced_prop = df['cl'].isna().sum()/len(df['cl']) * 100
    print(f'\nThere are {non_raced_prop} % races that are still not raced')
    return df

# What is the proportion of nans still present ?
def columns_percentage_nan():
    df = read_raw_data()
    lst_col = df.columns[:]
    for i in lst_col:
        print(f'{i} : {df[i].isna().sum()/len(df[i]) * 100} % of NaNs')

def create_y():
    df = read_raw_data()
    # Delete non-numerical values
    for i in range(len(df['cl'])):
        if not str(df['cl'][i]).isnumeric():
            df['cl'][i] = 0

    # tous les placés prennent la valeur 1
    for i in range(len(df['cl'])):
        if int(df['cl'][i]) < 4:
            df['cl'][i] = 1

    # tous les hors podium prennent la valeur 0
    for i in range(len(df['cl'])):
        if int(df['cl'][i]) > 1:
            df['cl'][i] = 0
    print('Encoding podium position done 🫡')
    return df

def raced_races():
    df = read_raw_data()
    #creation d'un dataframe avec toute les course jouer
    df_raced_races = df.copy()
    df_raced_races.dropna(subset=['cl'], inplace=True)
    df_raced_races.reset_index(inplace = True)

    print(f'\nRaced races shape : {df_raced_races.shape}')
    return df_raced_races

def non_raced_races():
    df = read_raw_data()
    # For comparing nos prediction quand on auras les resltas de la course
    df_non_raced_races = df.copy()

    # Keep df where df['cl'] = NaN
    df_non_raced_races = df_non_raced_races[df_non_raced_races['cl'].isna()]
    df_non_raced_races.reset_index(inplace = True)

    print(f'\nNon raced races shape : {df_non_raced_races.shape}')
    return df_non_raced_races

def compare_raced_nonraced_size():
    df_raced_races = raced_races()
    df_non_raced_races = non_raced_races()
    # mettre les data frame a la meme taille
    df_raced_races = df_raced_races[:len(df_non_raced_races)]
    # on compare les pourcentage de nan
    lst_col = df_raced_races.columns[:]
    print('\n Raced / Non Raced\n')
    for i in lst_col:
        print(f'{i} : {df_raced_races[i].isna().sum()/len(df_raced_races[i]) * 100} / {df_non_raced_races[i].isna().sum()/len(df_non_raced_races[i]) * 100}')

def drop_percentage_nan(percentage=90):
    df = read_raw_data()
    # Drop columns with too many NaNs (> 90%)
    # lst_futur_colums = []   #retirer les # pour imprimer les colonnes suprimer
    for i in df.columns:
        if df[i].isna().sum()/len(df[i]) * 100 > percentage:
            # lst_futur_colums.append(i)
            df.drop(i, axis=1, inplace=True)
    # print(f'les colonnes supprimées sont : {lst_futur_colums}')
    return df

def columns_with_nans():
    df = drop_percentage_nan()
    # Which columns still have NaNs ?
    lst_col = df.columns[:]
    for i in lst_col:
        if df[i].isna().sum()/len(df[i]) * 100 != 0:
            print(f'{i} : {df[i].isna().sum()/len(df[i]) * 100} : {df[i].dtype}')
    return df

def not_numeric():
    df_raced_races = raced_races()
    # Drop all non-numerical values
    df_raced_races.drop(['cheval', 'musiqueche', 'musiquept','musiquejoc',
                    'musiqueent','hippo','dernierhippo','dernierJoc',
                    'dernierEnt','dernierProp','proprietaire','createdat',
                    'updatedat','devise','coat','id.1','age.1','jour.1',
                    'comp.1','typec.1','hippo.1','dist.1','devise.1',
                    'url','createdAt','condi','arriv','heure','pere',
                    'mere','derniereplace','jour','prixnom','sex'], axis=1, inplace=True)

    # Transformer les lignes ou forcevent = NaN
    for i in range(len(df_raced_races['forceVent'])):
        if str(df_raced_races.forceVent[i]).isalpha():
            df_raced_races.forceVent[i] = mean

def preprocess():
    columns_percentage_nan()
    not_numeric()
    num_imputer = ColumnTransformer(
                [('poidmont_trans', SimpleImputer(strategy='mean'), ['poidmont']),
                ('oeuil_trans',SimpleImputer(strategy='most_frequent'), ['oeilFirstTime'])],
                remainder='passthrough')

    num_scaler = RobustScaler()

    num_preprocessing = make_pipeline(num_imputer, num_scaler)


    obj_col = make_column_selector(dtype_exclude= ['float64', 'int64'])
    obj_transphormer = OneHotEncoder()

    obj_preprocessing = make_column_transformer((obj_col, obj_transphormer))

    preproc_full = make_union(num_imputer, obj_preprocessing)
    print('Data preprocessed 🫡')
    return preproc_full
