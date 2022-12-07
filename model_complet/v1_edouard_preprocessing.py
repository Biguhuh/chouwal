# Version 1 - Edouard preprocessing - Logistic Regression
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

def to_df():
    csv_file = pd.read_csv('/Users/bastiengiudicelli/code/Biguhuh/chouwal/chouwal/PMU/data/2022_chouwal.csv')
    df = pd.DataFrame(csv_file)
    print("\nConversion CSV-DataFrame done 🫡")
    return df

def clean_data(df) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """
    # print(f'df : {df}')
    db = df[df.country != "FR "]
    # print(f'db : {db}')
    db = df.drop(columns = ["id", "comp", "jour","hippo", "heure", "numcourse", "cheval", "commen", "gainsCarriere",
                            "gainsVictoires", "gainsPlace", "gainsAnneeEnCours", "gainsAnneePrecedente", "jumentPleine",
                            "engagement", "handicapDistance", "handicapPoids", "indicateurInedit", "tempstot", "vha", "recordG",
                            "recordGint", "txreclam", "dernierTxreclam", "createdat", "updatedat", "dernierTxreclam", "rangTxVictJock",
                            "rangTxVictCheval", "rangTxVictEnt", "rangTxPlaceJock", "rangTxPlaceCheval", "rangTxPlaceEnt", "rangRecordG",
                            "appetTerrain", "estSupplemente", "devise", "coat", "country", "id", "comp", "jour", "heure", "hippo", "reun",
                            "prix", "prixnom", "partant", "groupe", "autos", "quinte", "arriv", "lice", "url", "createdAt",
                            "devise","id.1", "jour.1", "hippo.1", "typec.1", "dist.1", "devise.1", "corde.1", "age.1", "cheque.1"
                            ])
    
    
    leakage = ['cotedirect', 'coteprob', 'courueentraineurjour','victoireentraineurjour' ]    # print(f'db : {db}')
    db = db.drop(columns = leakage)

    db = db.drop(columns = [ "europ", "natpis", "amat", "courseabc", "pistegp", "temperature", "forceVent", "directionVent", "nebulositeLibelleCourt", "condi", "tempscourse", "ref"])


    db = db.drop(columns = ["numero","ecurie", "distpoids", "ecar", "redkm", "redkmInt", "corde", "musiquept", "musiqueche", "jockey", "musiquejoc",
                            "montesdujockeyjour", "couruejockeyjour", "victoirejockeyjour", "entraineur", "musiqueent", "dernierhippo", "derniernbpartants",
                            "dernierJoc", "dernierEnt", "dernierProp", "dernierRedKm", "proprietaire", "pere", "mere", "peremere", "meteo", "handi", "reclam",
                            "sex", "sexe", "age", "defoeil", "defoeilPrec", "derniereplace", "oeil", "dernierOeil", "typec"])
    if "partant.1" in db.columns:
        db.drop(columns = ["partant.1"], axis = 1, inplace = True)
    if "updatedAt" in db.columns:
        db.drop(columns = ["updatedAt"], axis = 1, inplace = True)
    if "defFirstTime" in db.columns:
        db.drop(columns = ["defFirstTime"], axis = 1, inplace = True)
    if "oeilFirstTime" in db.columns:
        db.drop(columns = ["oeilFirstTime"], axis = 1, inplace = True)
    if "comp.1" in db.columns:
        db.drop(columns = ["comp.1"], axis = 1, inplace = True)
    if "idJockey" in db.columns:
        db.drop(columns = ["idJockey"], axis = 1, inplace = True)
    
    return db

def transphorm_cl_to_y(dd):
    mask_0 = (dd['cl'].isna())
    dd.loc[mask_0, 'cl'] = 998
    mask = (dd['cl'].str.isnumeric())
    dd.loc[mask == False, 'cl'] = 999
    dd.cl = pd.to_numeric(dd.cl, errors='coerce') # on convertit toutes les valeurs en valeur int
    mask_1 = (dd['cl'] <= 4)
    dd.loc[mask_1 == True, 'cl'] = 1 # tous les placés (podiums) prennent la valeur 1
    mask_2 = dd['cl'] >= 3
    dd.loc[mask_2 == True, 'cl'] = 0 # tous les hors podium prennent la valeur 0
    
    return dd



def transform_all_non_numerical_value(df):
    df = df[df.applymap(type) != str]

    return df

'''
def refining_target():
    db = clean_data()
    mask = db['cl'].str.isnumeric()
    db[mask == False] = 999
    db['cl'] = pd.to_numeric(db['cl'] , errors='coerce') # on convertit toutes les valeurs en valeur int

    # Tous les placés (podiums) prennent la valeur 1
    mask1 = db['cl'] < 4
    db[mask1] = 1

    # Tous les hors podium prennent la valeur 0
    mask2 = db['cl'] > 1
    db[mask2] = 0

    return db

def define_features_target():
    db = refining_target()
    X = db.drop(columns = ['cl'])
    y = db.cl
    features = X.columns
    print("\nFeatures and target defined 🫡")
    # print(f'\n Features :\n {X}')
    # print(f'\n Target :\n {y}')

    return X, y, features

def scaling_imputing():
    #print(f'y : \n{y}')
    X, y, features = define_features_target()
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    imputer = SimpleImputer()
    imputer.fit(X)
    X = imputer.transform(X)

    X = pd.DataFrame(X, columns=features)
    print("\nTarget scaled and imputed 🫡")
    return X, y
'''
