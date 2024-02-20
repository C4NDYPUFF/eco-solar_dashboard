import pandas as pd 
import plotly.express as px
import requests


# def load_url_data_to_dataframe(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         data = response.json()
#         dataframe = pd.DataFrame(data)
#         if 'fecharegistro' in dataframe.columns:
#             dataframe.rename(columns={'fecharegistro': 'fecha_registro'}, inplace=True)
#         elif 'fecha_registro' not in dataframe.columns:
#         # Handle case where neither expected column name is present
#          raise ValueError("Expected column 'fecharegistro' or 'fecha_registro' not found in dataframe")

#         return dataframe
#     else:
#         print(f"Failed to retrieve data: Status code {response.status_code}")
#         return None

def load_url_data_to_dataframe(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        dataframe = pd.DataFrame(data)
        return dataframe
    else:
        print(f"Failed to retrieve data: Status code {response.status_code}")
        return None
        
def get_latest_registrarions(df,name):
    if df[name].dtype != 'datetime64[ns]':

        df[name] = pd.to_datetime(df[name])
    
    latest_date = df[name].max()
    df[name] = df[name].dt.date
    latest_num_registrations = df[df[name] == latest_date].shape[0]

    return latest_num_registrations






