import pandas as pd
import requests
import math
from env import username as user
from env import password as password
from env import hostname as host
import matplotlib.pyplot as plt
import seaborn as sns


def everything_converted_to_csv():
    df = pd.DataFrame()

    for i in range(10):
        response = requests.get(f'https://swapi.dev/api/people/?page={i}')
        data = response.json()
        if len(data.keys()) > 1:
            df = pd.concat([df, pd.DataFrame(data['results'])])
        
    df = df.reset_index()
    df = df.drop(columns = ['index'])
    df.to_csv('people.csv')


    df2 = pd.DataFrame()

    for i in range(5):
        response = requests.get(f'https://swapi.dev/api/starships/?page={i}')
        data = response.json()
        if len(data.keys()) > 1:
            df2 = pd.concat([df2, pd.DataFrame(data['results'])])

    df2 = df2.reset_index()
    df2 = df2.drop(columns = ['index'])
    df2.to_csv('starships.csv')

    df3 = pd.DataFrame()
#60
    for i in range(7):
        response = requests.get(f'https://swapi.dev/api/planets/?page={i}')
        data = response.json()
        if len(data.keys()) > 1:
            df3 = pd.concat([df3, pd.DataFrame(data['results'])])
            
    df3 = df3.reset_index()
    df3 = df3.drop(columns = ['index'])     
    df3.to_csv('planets.csv')

def get_all_data():
    return pd.read_csv('people.csv'), pd.read_csv('starships.csv'), pd.read_csv('planets.csv')

def merging_all_data(df1, df2, df3):
    the_list = list(df1.homeworld)
    the_merge_list = []
    for i in the_list:
        the_merge_list.append(requests.get(i).json()['name'])

    df1['plannet_merge'] = the_merge_list

    the_list = list(df1.homeworld)
    the_merge_list = []
    for i in the_list:
        the_merge_list.append(requests.get(i).json()['name'])

    df1['plannet_merge'] = the_merge_list
    df3['plannet_merge'] = df3.name
    df1.merge(df3, on = 'plannet_merge', how = 'left')
    
    return df1, df2, df3


def get_csv_germany():
    return pd.read_csv('Germany.csv')


def get_db_url(database):
    '''
    Returns a formatted string using credentials stored in env.py that can be passed to a pd.read_sql() function
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{database}'


def get_store_data():
    '''
    Returns a dataframe of all store data in the tsa_item_demand database and saves a local copy as a csv file.
    '''
    query = '''
            SELECT *
            FROM items
            JOIN sales USING(item_id)
            JOIN stores USING(store_id)
            '''

    df = pd.read_sql(query, get_db_url('tsa_item_demand'))
    df.to_csv('tsa_store_data.csv', index=False)
    return df
    

def read_storedata_from_csv():
    return pd.read_csv('tsa_store_data.csv')
    

def get_histplots(df):
    print('item_price')
    plt.hist(df.item_price)
    plt.show()

    print('sale_amount')
    plt.hist(df.sale_amount)
    plt.show()

def convert_to_datetime(df):
    df.sale_date = pd.to_datetime(df.sale_date)
    return df


def salesdate_index(df):
    df = df.set_index('sale_date')
    return df


def add_month_week(df):
    df['month'] = df.index.month
    df['dayofweek'] = df.index.day_name()
    return df


def sales_total_add(df):
    df['sales_total'] = df['sale_amount'] * df['item_price']
    return df

def prep_sales(df):
    df.sale_date = pd.to_datetime(df.sale_date)
    df = df.set_index('sale_date')
    df['month'] = df.index.month
    df['weekday'] = df.index.day_name()
    df['sales_total'] = df['sale_amount'] * df['item_price']
    return df


def germany_prep(df):
    df.Date = pd.to_datetime(df.Date)
    df = df.set_index('Date')
    df['month'] = df.index.month_name()
    df['year'] = df.index.year
    df = df.sort_index()
    df['Wind'].fillna(value=df['Wind'].mean(), inplace=True)
    df['Solar'].fillna(value=df['Solar'].mean(), inplace=True)
    df['Wind+Solar'].fillna(value=0, inplace=True)
    df = df.drop(columns = 'Unnamed: 0')
    return df

def germany_histplots(df):
    plt.figure(figsize=(14,14))

    for i, col in enumerate(df.drop(columns = 'Unnamed: 0')):
        plt.subplot(2,3,i +1)
        sns.histplot(df[col])
        
    plt.show()
