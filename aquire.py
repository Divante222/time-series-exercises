import pandas as pd
import requests
import math

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

    
