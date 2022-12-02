import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_selector, make_column_transformer
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.impute import SimpleImputer


def get_data():
    df = pd.read_csv('data/2022_chouwal.csv')
    return df



def drop_the_non_frensh_races(df):
    # df['country'].apply(strip, axis=1) peut etre utile un jour
    df = df[df.country == "FR "]
    return df


def drop_the_leackage(df): # permet de supprimer les colonnes qui donne des info qu'on est pas senser avoir avant la course
    pass

def retirer_les_coat(df):
    df.applymap(lambda x: str(x)[1:-1] if str(x)[0] == "'" and str(x)[-1] == "'" else x)
    return df

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


def transform_defoeil_to_changementFer(df) : 
    mask = df.defoeil != df.defoeilPrec
    df['changementFer'] = mask.astype(int)
    df.drop(['defoeilPrec','defoeil'], axis=1, inplace=True)


 
#foction pour drop (encore) un certain nombre de colone qui contienne beaucoup de nan, de valeur compliqué a gerer...
def drop_maybe_usefull_columns(df): #on les drop pour ce simplifier la vie et faire un model rapidement mais elle seront peut etre a recuperer dans le futur
    
    df = df.drop(['ecar','redkm','meteo','handi','corde.1','autos',
                'quinte','natpis','courseabc','directionVent',
                'nebulositeLibelleCourt','tempscourse','redkm',
                'dernierRedkm','recordG'], #drop pour linstant mais je suis entrain de les numérisé
                 axis=1, inplace=True)
    
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



class custom_imputer:
    def __init__(self):
        self

    def fit(self, X, y=None):
        self.X = X
        self.imputer_mean = SimpleImputer(strategy='mean')
        self.imputer_mf = SimpleImputer(strategy='most_frequent')
        self.imputer_mean.fit(self.X[['poidmont']])
        self.imputer_mf.fit(self.X[['groupe', 'oeilFirstTime']])
        
        
        return self

    def transform(self, X, y=None):
        self.X[['poidmont']] = self.imputer_mean.transform(self.X[['poidmont']])
        self.X[['groupe', 'oeilFirstTime']] = self.imputer_mf.transform(self.X[['groupe', 'oeilFirstTime']])
        
        return self.X

    def fit_transform(self, X, y=None):
        self.X = X
        self.fit(self.X)
        return self.transform(self.X)

def proprocesse_pipeline():
    
    custom_imput = custom_imputer()

    num_col = make_column_selector(dtype_include= ['float64', 'int64'])
    num_scaler = RobustScaler()
    num_prerpocessing = make_column_transformer((num_scaler, num_col))

    obj_col = make_column_selector(dtype_exclude= ['float64', 'int64'])
    obj_transphormer = OneHotEncoder()
    obj_preprocessing = make_column_transformer((obj_transphormer, obj_col))

    unions = make_union(num_prerpocessing, obj_preprocessing)
    preproc_full = make_pipeline(custom_imput, unions)
    
    return preproc_full



def final_preprocessing(df):
    
    df = drop_the_non_frensh_races(df)
    df = retirer_les_coat(df)
    df = drop_percentage_nan(df)
    df = drop_useless_obj_columns(df)
    df = created_y(df)
    
    X, y = X_y(df)
    X_train, X_test, y_train, y_test = split_train_test(X, y)
    
    preproc_full = proprocesse_pipeline()
    preproc_full.fit_transform(X_train)
    
    return df, X_train, X_test, y_train, y_test