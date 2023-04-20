import pandas as pd 
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import json
import plotly.express as px
from urllib.request import urlopen
import geopandas as gpd 

rainfallData = pd.read_csv("india_monthly_rainfall_data.csv")
temperatureData = pd.read_csv("temperatures.csv")
# print(temperatureData)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

rainfallData.loc[rainfallData['State']=='Chattisgarh','State'] = "Chhattisgarh"
rainfallData.loc[rainfallData['State']=='Delhi','District'] = "Delhi"
rainfallData.loc[rainfallData['State']=='Jammu & Kashmir','State'] = 'Jammu and Kashmir'


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

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])




app.layout = html.Div([
        html.Div([
        html.H1('Change in Average rainfall and average temperature', style={'color': 'Grey' , 'textAlign': 'center'}),
        
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
            tooltip={"placement": "bottom", "always_visible": True},
            value = 2000,
            className='year-slider'
        ),
        html.Div(children = [ dcc.Graph(id='rainfall-correlation', style={'backgroundColor' : 'red'}),
        dcc.Graph(id='temp-correlation', style={'backgroundColor' : 'red'}),], style={'display' : 'flex', 'justifyContent' : 'space-between'})
       
        # dcc.Graph(id='rainfall-temp-correlation', style={'backgroundColor' : 'red'})
    ]),
   
])



@app.callback(Output('rainfall-correlation', 'figure'), Input('slider', 'value'))
def updateRainfall(sliderVal):
    print('changing rainfall')
    temp = rainfallData[rainfallData['Year']==sliderVal]
    # print(temp[0:5])
    dfR = pd.DataFrame({'avgRainfall' : []})
    # dfT = pd.DataFrame({'avgTemperature' : []})
    for m in months:
        t1 = temp[months[m]]
        avgRainfall = t1.sum()/len(t1)
        dfR.loc[m, 'avgRainfall'] = avgRainfall
        # t1 = temperatureData[months[m]]
        # avgTemperature = t1.sum()/len(t1)
        # dfT.loc[m, 'avgTemperature'] = avgTemperature
        # print('Average rainfall Overall india in ', months[m], ' : ', avgRainfall)
        # print('Average Temperature Overall india in ', months[m], ' : ', avgTemperature)
       
        # print(type(t1))
        # print(months[m], t1[0:5], sep='\n')
        # print('length ', len(t1))
        # print('type ', type(t1))
        # print(t1[0:5])
    df = pd.DataFrame()
    df['avgRainfall'] = dfR
    # df['avgTemperature'] = dfT
    fig = px.line(df, x=list(months.values()), y=['avgRainfall'])
    return fig

@app.callback(Output('temp-correlation', 'figure'), Input('slider', 'value'))
def updateTemperature(sliderVal):
    print('changing temp')
    temp = temperatureData[temperatureData['Year']==sliderVal]
    # print(temp[0:5])
    # dfR = pd.DataFrame({'avgRainfall' : []})
    dfT = pd.DataFrame({'avgTemperature' : []})
    for m in months:
        # t1 = temp[months[m]]
        # avgRainfall = t1.sum()/len(t1)
        t1 = temp[months[m]]
        avgTemperature = t1.sum()/len(t1)
        # dfR.loc[m, 'avgRainfall'] = avgRainfall
        dfT.loc[m, 'avgTemperature'] = avgTemperature
        # print('Average rainfall Overall india in ', months[m], ' : ', avgRainfall)
        # print('Average Temperature Overall india in ', months[m], ' : ', avgTemperature)
       
        # print(type(t1))
        # print(months[m], t1[0:5], sep='\n')
        # print('length ', len(t1))
        # print('type ', type(t1))
        # print(t1[0:5])
    df = pd.DataFrame()
    # df['avgRainfall'] = dfR
    df['avgTemperature'] = dfT
    fig = px.line(df, x=list(months.values()), y=['avgTemperature'], color_discrete_sequence=['red'])
    return fig

# @app.callback(Output('rainfall-temp-correlation', 'figure'), Input('slider', 'value'))
# def updateCorrelation(sliderVal):
#     temp = rainfallData[rainfallData['Year']==sliderVal]
#     # print(temp[0:5])
#     dfR = pd.DataFrame({'avgRainfall' : []})
#     dfT = pd.DataFrame({'avgTemperature' : []})
#     for m in months:
#         t1 = temp[months[m]]
#         avgRainfall = t1.sum()/len(t1)
#         t1 = temperatureData[months[m]]
#         avgTemperature = t1.sum()/len(t1)
#         dfR.loc[m, 'avgRainfall'] = avgRainfall
#         dfT.loc[m, 'avgTemperature'] = avgTemperature
#         # print('Average rainfall Overall india in ', months[m], ' : ', avgRainfall)
#         # print('Average Temperature Overall india in ', months[m], ' : ', avgTemperature)
       
#         # print(type(t1))
#         # print(months[m], t1[0:5], sep='\n')
#         # print('length ', len(t1))
#         # print('type ', type(t1))
#         # print(t1[0:5])
#     df = pd.DataFrame()
#     df['avgRainfall'] = dfR
#     df['avgTemperature'] = dfT
    
#     fig = px.line(df, x='avgTemperature', y='avgRainfall', color_discrete_sequence=['red'])

#     return fig

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=True, threaded=True)