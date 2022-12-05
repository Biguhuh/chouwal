# Version 1 - Edouard preprocessing - Logistic Regression
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

def to_df():
    csv_file = pd.read_csv('/Users/bastiengiudicelli/code/Biguhuh/chouwal/chouwal/PMU/data/2022_chouwal.csv')
    df = pd.DataFrame(csv_file)
    print("\nConversion CSV-DataFrame done 🫡")
    return df

def clean_data() -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """
    df = to_df()
    # print(f'df : {df}')

    db = df[df.country != "FR "]
    # print(f'db : {db}')
    db = df.drop(columns = ["id", "comp", "jour","hippo", "heure", "numcourse", "cheval", "commen", "gainsCarriere",
                            "gainsVictoires", "gainsPlace", "gainsAnneeEnCours", "gainsAnneePrecedente", "jumentPleine",
                            "engagement", "handicapDistance", "handicapPoids", "indicateurInedit", "tempstot", "vha", "recordG",
                            "recordGint", "txreclam", "dernierTxreclam", "createdat", "updatedat", "dernierTxreclam", "rangTxVictJock",
                            "rangTxVictCheval", "rangTxVictEnt", "rangTxPlaceJock", "rangTxPlaceCheval", "rangTxPlaceEnt", "rangRecordG",
                            "appetTerrain", "estSupplemente", "devise", "coat", "country", "id", "comp", "jour", "heure", "hippo", "reun",
                            "prix", "prixnom", "partant", "groupe", "autos", "quinte", "arriv", "lice", "url", "updatedAt", "createdAt",
                            "devise","id.1", "comp.1", "jour.1", "hippo.1", "typec.1", "partant.1", "dist.1", "devise.1", "corde.1", "age.1", "cheque.1"
                            ])
    leakage = ['cotedirect', 'coteprob', 'courueentraineurjour','victoireentraineurjour' ]    # print(f'db : {db}')
    db = db.drop(columns = leakage)

    db = db.drop(columns = [ "europ", "natpis", "amat", "courseabc", "pistegp", "temperature", "forceVent", "directionVent", "nebulositeLibelleCourt", "condi", "tempscourse", "ref"])

    # print(f'db : {db}')

    db = db.drop(columns = ["numero","ecurie", "distpoids", "ecar", "redkm", "redkmInt", "corde", "musiquept", "musiqueche", "jockey", "musiquejoc",
                            "montesdujockeyjour", "couruejockeyjour", "victoirejockeyjour", "entraineur", "musiqueent", "dernierhippo", "derniernbpartants",
                            "dernierJoc", "dernierEnt", "dernierProp", "dernierRedKm", "proprietaire", "pere", "mere", "peremere", "meteo", "handi", "reclam",
                            "sex", "sexe", "age", "defoeil", "defoeilPrec", "derniereplace", "oeil", "dernierOeil", "typec"])
    # print(f'db : {db}')

    #db = db.select_dtypes(include=['int64'])
    # print(f'db : {db}')

    db = db.dropna(subset=['cl']) # on vire les lignes dont les résultats ne sont pas connus
    #print(f'db : {db}')

    mask = db['cl'].str.isnumeric()
    db[mask == False] = 999
    db['cl'] = pd.to_numeric(db['cl'] , errors='coerce') # on convertit toutes les valeurs en valeur int

    # Tous les placés (podiums) prennent la valeur 1
    mask1 = db['cl'] < 4
    db[mask1] = 1

    # Tous les hors podium prennent la valeur 0
    mask2 = db['cl'] > 1
    db[mask2] = 0
    print("\ny has been refined 🫡")
    #print(f'{db.info()}')

    return db

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
