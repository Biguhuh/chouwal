import os
import pandas as pd

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
    # print(f'db : {db}')

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

    print("\nData cleaned 🫡")
    #print(f'{db.info()}')

    return db
