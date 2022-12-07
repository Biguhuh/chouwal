def affichage(df, y_pred, y_pred_proba):
    df['proba pl'] = y_pred_proba[:,1]
    df['pred'] = y_pred
    df = (df[df['pred'] == 1])
    df = df[['hippo','prixnom','cheval', 'numero', 
             'jour', 'heure', 'proba pl']].sort_values('heure')
    
    return df