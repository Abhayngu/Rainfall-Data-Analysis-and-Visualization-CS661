import pandas as pd 
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import json
import plotly.express as px
from urllib.request import urlopen
import geopandas as gpd 

data = pd.read_csv("india_monthly_rainfall_data.csv")
india_states = json.load(open("india_district.geojson", "r"))
india = json.load(open("india_state_geo.json","r"))

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

data.loc[data['State']=='Chattisgarh','State'] = "Chhattisgarh"
data.loc[data['State']=='Delhi','District'] = "Delhi"
data.loc[data['State']=='Jammu & Kashmir','State'] = 'Jammu and Kashmir'


months={
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'May',
    6: 'Jun',
    7: 'Jul',
    8: 'Aug',
    9: 'Sep',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}

app = Dash(__name__)




app.layout = html.Div([
        html.H1('Rain Fall Data Visualization', style={'color': 'Grey' , 'text-align': 'center' , 'margin-bottom': '10px'}),
        html.Div([
        dcc.Slider(
            id='slider',
            min=1901,
            max=2003,
            step=1,
            marks={
                1901: '1901',
                1920: '1920',
                1940: '1940',
                1960: '1960',
                1980: '1980',
                2003: '2003'
            },
            value = 2000
        ),
    ]),
   
])




    

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)