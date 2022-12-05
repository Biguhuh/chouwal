import zlib
import requests
from requests.auth import HTTPBasicAuth
from datetime import date, timedelta
import pandas as pd
import os


def create_str_date_values():
    date_today = date.today()
    date_yesterday = date.today() - timedelta(days=1)
    return date_today, date_yesterday



#downloading the database, returning a text file to convert. This text file contains 2 tables: cachedate and caractrap
def download_data(date):
    user = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
    url = f'http://195.15.226.172/share/pturfDay{date}.sql.gz'
    res = requests.get(url, auth=HTTPBasicAuth(user, password), timeout=10)
    data = zlib.decompress(res.content, zlib.MAX_WBITS|32)
    return data

# saving the database as sql files : is it really usefull ? Nope, not after developpement
def save_today_for_pred_sql(data_t, date_t):
    with open(f'{date_t}_for_pred.sql', 'w') as file:
      file.write(str(data_t))
    file.close()
    
def save_yesterday_for_val_sql(data_y, date_y):
    with open(f'{date_y}_for_val.sql', 'w') as file:
      file.write(str(data_y))
    file.close()


# TABLE 1

# convert and save cachedate as csv
def save_cachedate_csv(data, date, status):
    _data_ = str(data.decode()).replace('\\t', ',').replace('\\n', '\n').replace('),(','\n')
    start_1=int(_data_.find('cachedate` VALUES (') + len('cachedate` VALUES ('))
    stop_1=_data_.find('/*!40000 ALTER TABLE `cachedate` ENABLE KEYS */') - len(";\n'")
    print(_data_[start_1: stop_1] + '\n',
    file=open(f'{date}_cachedate_{status}.csv', 'w'))
    

# create cachedate as proper dataframe    
def df_cachedate(data, date, status):
    headers_1= features[0:133].tolist() + [n for n in range(0,10)]
    save_cachedate_csv(data, date, status)

    _df_ = pd.read_csv(f'{date}_cachedate_{status}.csv',
                    index_col=None,
                    sep=',',
                    skiprows=0, names = headers_1)

    dcachedate = _df_.drop(columns = [0,1,2,3,4,5,6,7,8,9])
    return dcachedate


# TABLE 2

# convert and save caractrap as csv    
def save_caractrap_csv(data, date, status):
    _data_ = str(data.decode()).replace('\\t', ',').replace('\\n', '\n').replace('),(','\n')
    start_2=int(_data_.find('INSERT INTO `caractrap` VALUES (') + len('INSERT INTO `caractrap` VALUES ('))
    stop_2=_data_.find('/*!40000 ALTER TABLE `caractrap` ENABLE KEYS */') - len(";\n'")
    print(_data_[start_2: stop_2] + '\n',
    file=open(f'{date}_caractrap_{status}.csv', 'w'))


# create caractrap as proper dataframe    
def df_caractrap(data, date, status):
    headers_2= features[133:].tolist() + [n for n in range(0,10)]

    save_caractrap_csv(data, date, status)

    _dg_ = pd.read_csv(f'{date}_caractrap_{status}.csv',
                    index_col=None,
                    sep=',',
                    skiprows=0, names = headers_2)

    dcaractrap = _dg_.drop(columns = [0,1,2,3,4,5,6,7,8,9])
    return dcaractrap    

# create the final dataframe
def save_final_dataframe(data, date, status):
    # loading the 2 tables od database
    d_cachedate = df_cachedate(data, date, status)
    d_caractrap = df_caractrap(data, date, status)

    # rename column which is a mess
    d_caractrap.rename(columns={'comp.1':'comp'},inplace=True)

    # merging of both dataframes to create proper final dataframe. Ready to use !
    final_df=d_cachedate.merge(d_caractrap,how='left',on='comp')
    
    final_df = final_df.applymap(lambda x: str(x)[1:-1] if str(x)[0] == "'" and str(x)[-1] == "'" else x)
    final_df.to_csv(f'{date}_df_{status}.csv', index=False)
    return final_df



# main function
def get_daily_db():
    date_today, date_yesterday = create_str_date_values()
    data_today = download_data(date_today)
    data_yesterday = download_data(date_yesterday)
    #save_today_for_pred_sql(data_today, date_today)
    #save_yesterday_for_val_sql(data_yesterday, date_yesterday)
    today_df = save_final_dataframe(data_today, date_today, 'pred')
    yesterday_df = save_final_dataframe(data_yesterday, date_yesterday, 'val')
    return today_df, yesterday_df
    