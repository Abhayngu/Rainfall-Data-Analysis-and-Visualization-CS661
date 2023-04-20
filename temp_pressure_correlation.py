import pandas as pd 
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import json
import plotly.express as px
from urllib.request import urlopen
import geopandas as gpd 

pressureData = pd.read_csv("india_monthly_rainfall_data.csv")
temperatureData = pd.read_csv("temp.csv")
# print(temperatureData)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

pressureData.loc[pressureData['State']=='Chattisgarh','State'] = "Chhattisgarh"
pressureData.loc[pressureData['State']=='Delhi','District'] = "Delhi"
pressureData.loc[pressureData['State']=='Jammu & Kashmir','State'] = 'Jammu and Kashmir'


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
        html.H1('Correlation between Temperature and Pressure in India', style={'color': 'Grey' , 'text-align': 'center' , 'margin-bottom': '10px'}),
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
        dcc.Graph(id='temp-pressure-correlation', style={'backgroundColor' : 'red'})
    ]),
   
])



@app.callback(Output('temp-pressure-correlation', 'figure'), Input('slider', 'value'))
def updateCorrelationGraph(sliderVal):
    temp = pressureData[pressureData['Year']==sliderVal]
    # print(temp[0:5])
    dfR = pd.DataFrame({'avgRainfall' : []})
    dfT = pd.DataFrame({'avgTemperature' : []})
    for m in months:
        t1 = temp[months[m]]
        avgRainfall = t1.sum()/len(t1)
        t1 = temperatureData[months[m]]
        avgTemperature = t1.sum()/len(t1)
        dfR.loc[m, 'avgRainfall'] = avgRainfall
        dfT.loc[m, 'avgTemperature'] = avgTemperature
        # print('Average rainfall Overall india in ', months[m], ' : ', avgRainfall)
        # print('Average Temperature Overall india in ', months[m], ' : ', avgTemperature)
       
        # print(type(t1))
        # print(months[m], t1[0:5], sep='\n')
        # print('length ', len(t1))
        # print('type ', type(t1))
        # print(t1[0:5])
    df = pd.DataFrame()
    df['avgRainfall'] = dfR
    df['avgTemperature'] = dfT
    print('----------------------------------------')
    print(df)
    # df = px.data.gapminder().query("continent=='Oceania'")
    fig = px.line(df, x=list(months.values()), y=['avgRainfall', 'avgTemperature'])
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=True, threaded=True)