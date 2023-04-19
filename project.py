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

indian_states_lat_log = {
    "Andhra Pradesh": (15.9129, 79.7399),
    "Arunachal Pradesh": (28.2180, 94.7278),
    "Assam": (26.2006, 92.9376),
    "Bihar": (25.0961, 85.3131),
    "Chhattisgarh": (21.2787, 81.8661),
    "Goa": (15.2993, 74.1240),
    "Gujarat": (22.2587, 71.1924),
    "Haryana": (29.0588, 76.0856),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Delhi" : (28.7041, 77.1025),
    "Jammu and Kashmir" : (33.2778, 75.3412),
    "Jharkhand": (23.6102, 85.2799),
    "Karnataka": (15.3173, 75.7139),
    "Kerala": (10.8505, 76.2711),
    "Madhya Pradesh": (22.9734, 78.6569),
    "Maharashtra": (19.7515, 75.7139),
    "Manipur": (24.6637, 93.9063),
    "Meghalaya": (25.4670, 91.3662),
    "Mizoram": (23.1645, 92.9376),
    "Nagaland": (26.1584, 94.5624),
    "Orrisa": (20.9517, 85.0985),
    "Punjab": (31.1471, 75.3412),
    "Rajasthan": (27.0238, 74.2179),
    "Sikkim": (27.5330, 88.5122),
    "Tamil Nadu": (11.1271, 78.6569),
    "Telangana": (18.1124, 79.0193),
    "Tripura": (23.9408, 91.9882),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Uttaranchal": (30.0668, 79.0193),
    "West Bengal": (22.9868, 87.8550)
}

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

temp1 = gpd.GeoDataFrame.from_features(india["features"]).rename(columns={'NAME_1':'State'})
temp2 = gpd.GeoDataFrame.from_features(india_states["features"]).rename(columns={'NAME_2':'District'})



app.layout = html.Div([
    html.Div([
        html.H1('Rain Fall Data Visualization', style={'color': 'Grey' , 'text-align': 'center' , 'margin-bottom': '10px'}),
        ], 
        style={'border': '1px solid black', 'padding': '10px'}
    ),
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
        dcc.Slider(
            id='month-slider',
            min=1,
            max=12,
            step=1,
            marks={
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
            },
            value=7
        )
    ]),
    html.Div([
        dcc.Graph(id='india-graph', figure={} , style={'width': '70%', 'height': '500px', 'margin': 'auto' , 'margin-top': '10px'})
    ], style={'display': 'inline-block', 'width': '50%'}),
    html.Div([
        dcc.Graph(id='state-graph',figure={} , style={'width': '100%', 'height': '500px', 'margin': 'auto' , 'margin-top': '10px'})
    ], style={'display': 'inline-block', 'width': '50%'})
])

@app.callback(Output('state-graph', component_property='figure'),
              [Input('india-graph', 'clickData'),Input('slider','value'),Input('month-slider','value')]
)
def update_states(clickData,slider_value,month_value):
    if clickData is not None:
        value = clickData['points'][0]['location']
    else:
        value = "Madhya Pradesh"
#     print(value,slider_value,month_value)
    data_ = data[data['State']==value]
    data_ = data_[data_['Year']==slider_value]
    data_ = data_.loc[:,['District',months[month_value]]]
    global temp2
    
    temp = temp2[temp2['NAME_1']==value]
    merged = temp.merge(data_, on="District").set_index("District")
    merged = merged.loc[:,['geometry',months[month_value]]]
    
    fig = px.choropleth_mapbox(merged,
                               geojson=merged.geometry,
                               locations=merged.index,
                               color=months[month_value],
    #                            range_color=(0, 100),
                               color_continuous_scale='Viridis',
                               mapbox_style='carto-positron',
                               center={'lat': indian_states_lat_log[value][0], 'lon': indian_states_lat_log[value][1]},
                               zoom=5,
                              )
    fig.update_layout(margin={'r':0,'l':0,'b':0,'t':0})
#     fig.show()
    return fig;

@app.callback(
    Output('india-graph', 'figure'),
    [Input('slider', 'value'),Input('month-slider','value')]
)
def update_map(slider_value,month_value):
#     data_ = data.groupby('State')['Jul'].mean().reset_index()
#     print(slider_value,month_value)
    data_ = data[data['Year']==slider_value]
    data_ = data_.groupby('State')[months[month_value]].mean().reset_index()
    global temp1
    temp = temp1
    merged = temp.merge(data_, on="State").set_index("State")
    merged = merged.loc[:,['geometry',months[month_value]]]
                        
    fig = px.choropleth_mapbox(merged, 
                            geojson=merged.geometry,
                           locations=merged.index,
                           color=months[month_value],
#                            range_color=(0, 100),
                           color_continuous_scale='Viridis',
                           mapbox_style='carto-positron',
                           center={'lat': 20.5937, 'lon': 78.9629},
                           zoom=3,
                          )
    fig.update_layout(margin={'r':0,'l':0,'b':0,'t':0})
    return fig


    

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)