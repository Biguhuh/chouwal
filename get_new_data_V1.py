import pandas as pd
import numpy as np
import requests
from datetime import date
import zlib
from requests.auth import HTTPBasicAuth

# credentials to place in git ignore
user = 'XX'
password = 'XXX'


def fetch_new_data():
    date = date.today()
    Base_url ='http://195.15.226.172/share/pturfDay'
    url= f'{Base_url}{date}.sql.gz'
    response = requests.get(url,auth=HTTPBasicAuth(user, password), timeout=10)
    data = zlib.decompress(response.content, zlib.MAX_WBITS|32)

    # 1.Convert my bytes file into string
    byte_file=data
    data_file = byte_file.decode()
    print(data_file)


    # 2. convert string to csv
    data_file = data_file.replace('\\t', ',').replace('\\n', '\n').replace('),(','\n')

    # 3. write csv to file
    print(data_file[950:-1], file=open('my_file_20223011.csv', 'w'))
    pd.read_csv('my_file_20223011.csv')

    #pseudo code for tmw
    #when finding the following content:

    '''
    /*!40000 ALTER TABLE `cachedate` ENABLE KEYS */
    --
    -- Dumping data for table `caractrap`
    --
    -- WHERE:  jour='2022-11-30'
    LOCK TABLES `caractrap` WRITE

    /*!40000 ALTER TABLE `caractrap` DISABLE KEYS */
    INSERT INTO `caractrap` VALUES (
    '''
    #Action 1 => delete those strings
    #Action 2 => Create a second csv / find the matching key to concatenate this data with the upper part of the csv

    return ###
