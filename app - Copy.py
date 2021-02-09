#importing libraries 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os 
import pandas as pd
import calculation  #The file which contains the calculations 
import plotly.graph_objects as go
import dash_table as dt
import geo_calculation


#Get  data
today_info = calculation.latest_info
total_confirmed = calculation.total_confirmed
total_today_str = " +"+ str(int(calculation.total_today))
n_deaths=calculation.n_deaths
possibly_cases= calculation.possibly_cases
last_updated="Last updated:" + str(calculation.last_updated)
df_merged=calculation.df_merged
df_merged_copy = calculation.df_merged_copy
sw_delay = calculation.sw_delay
geo_merged = geo_calculation.geo_merged
geo_merged_json = geo_calculation.geo_merged_json
confirmed_deaths_today_str = " +"+ str(int(calculation.confirmed_deaths_today))
discharged_cases = calculation.discharged_cases
df_world = calculation.df_world
df_details = calculation.df_details
df_age = calculation.df_age

#Case classification graph 
fig_1 = px.bar(df_merged, x=df_merged.index, y=["Local link (+)","Local link (-)","Imported link (+)","Imported link (-)"],barmode="stack", title="Epidemic Curve according to four different case types",
                labels={"value": "Cases", "variable": "Case type"},hover_data=["Total"],template="plotly_dark")
fig_1.update_layout(paper_bgcolor="#363431")
fig_1.update_layout(title={'xanchor': 'center','x':0.5,},margin=dict(l=30, r=10, t=45, b=20))
fig_1.update_layout(legend=dict(orientation="h",yanchor="bottom",y=0.97,xanchor="right",x=1))
# fig_1.update_layout(plot_bgcolor="black")

#Sliding window total cases
fig_2 = px.scatter(df_merged, x=df_merged.index, y="Total" , title="Daily Cases", labels={"value": " Total Cases", "variable": "Daily total cases"}, template="plotly_dark" )
fig_2.add_trace(go.Scatter(name="Sliding window (7 days)",x =df_merged_copy.index,y=df_merged_copy["Total"] ))
fig_2.update_layout(paper_bgcolor="#363431")
fig_2.update_layout(title={'xanchor': 'center','x':0.5,},margin=dict(l=30, r=10, t=30, b=20))
fig_2.update_layout(legend=dict(yanchor="bottom",y=0.9 ,xanchor="right",x=1))
fig_2['data'][0]['showlegend']=True
fig_2['data'][0]['name']='Total reported cases'

#Delay Sliding window
fig_3 = px.line(sw_delay, x=sw_delay.index, y=["Local link (+)","Local link (-)"] , title="Average Delay : Sliding window (7 days)", labels={"value": " Average Delay", "variable": "Case Type"}, template="plotly_dark" )
fig_3.update_layout(paper_bgcolor="#363431")
fig_3.update_layout(title={'xanchor': 'center','x':0.5,},margin=dict(l=30, r=10, t=30, b=20))
fig_3.update_layout(legend=dict(yanchor="top",y=1.02,xanchor="right",x=1))

#Building clusters
MAPBOX_ACCESSTOKEN = 'pk.eyJ1Ijoic2hvdW5hazIiLCJhIjoiY2trMWRqbGp2MDAwODJ3bnVnemwzOXU2OSJ9.nya5Aq9vI6HC2dfnnzs8IA'

zmin = geo_merged['Building name'].min()
zmax = geo_merged['Building name'].max()

# Set the data for the map
data = go.Choroplethmapbox(
        geojson = geo_merged_json,             #this is your GeoJSON
        locations = geo_merged.index,    #the index of this dataframe should align with the 'id' element in your geojson
        z = geo_merged["Building name"], #sets the color value
#        colorbar=dict(thickness=20, ticklen=3, tickformat='%',outlinewidth=0), adjusts the format of the colorbar
        marker_line_width=1, marker_opacity=0.7, colorscale="Viridis", #adjust format of the plot
        zmin=zmin, zmax=zmax, hovertext=["District"])           #sets min and max of the colorbar
#         hovertemplate = "<b>%{text}</b><br>" +
#                     "%{z:.0%}<br>" +
#                     "<extra></extra>")  # sets the format of the text shown when you hover over each shape

# Set the layout for the map
layout = go.Layout(
    title = {'text': f"Cases related to clusters in Buildings (classified by District)"},
            # 'font': {'size':24}},       #format the plot title
    mapbox1 = dict(
        domain = {'x': [0, 1],'y': [0, 1]}, 
         center = dict(lat=22.2800 , lon=114.1588),
        accesstoken = MAPBOX_ACCESSTOKEN, 
        zoom = 9),                      
    autosize=True, margin=dict(l=0, r=0, t=40, b=0))
    # height=650,)
#     )
fig_4=go.Figure(data=data, layout=layout)
fig_4.update_layout(mapbox_style="dark")
fig_4.update_layout(paper_bgcolor="#363431")
fig_4.update_layout(font={"color":"white"},title={'xanchor': 'center','x':0.5,})


#Fig 5 Mode of testing
df_testing = calculation.df_testing
fig_5 = px.pie(df_testing, values='Number of cases', names='Category name', title='Mode of testing',template="plotly_dark",height=300)
fig_5.update_layout(margin=dict(l=30, r=10, t=30, b=20))
fig_5.update_layout(showlegend=False)
fig_5.update_layout(paper_bgcolor="#363431")
fig_5.update_layout(title={'xanchor': 'center','x':0.5,})

#Fig 6 Age
fig_6 = px.bar(df_age, x = df_age.index, y = ["Local with Epi-link","Local without Epi-link","Local"],labels={"value": " Percentage of cases with delay", "variable": "Case type"},barmode='group',template="plotly_dark")
fig_6.update_layout(title="Confirmation delay for local cases, classified by age")
fig_6.update_layout(paper_bgcolor="#363431")
fig_6.update_layout(title={'xanchor': 'center','x':0.5,})

#Tab styles
tabs_styles = {
    'height': '10px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    "backgroundColor":"#363431",
    "color":"white",
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '2px'
}

app=dash.Dash(__name__)
#server = app.server


app.layout=html.Div(style={"backgroundColor":"black"},children=[

    

    ##################    Header
    html.Div(className="page_header",children=[
        html.H1("COVID 19 Dashboard for Hong Kong"),
        ]),

    ##################     Main contents begin here
    
    #Left Column
    html.Div(children=[
        html.Div(style={"border":"2px black solid","margin":"0"},children=[
            html.P("Confirmed Cases"),
            html.H2(children=[total_confirmed,
                html.Span(style={"color":"red"},children=[total_today_str])]),
        ]),

        html.Div(style={"border":"2px black solid"},children=[
            html.P("Confirmed Deaths"),
            html.H2(children=[n_deaths,
                html.Span(style={"color":"red"},children=[confirmed_deaths_today_str])]),
        ]),
        
        html.Div(style={"border":"2px black solid"},children=[
            html.P("Discharged Cases"),
            html.H2(discharged_cases),
        ]),

        html.Div(style={"border":"2px black solid"},children=[
            html.P("Possible Cases"),
            html.H2(possibly_cases), #replace with actual data
        ]),

        dt.DataTable(
            id="Case details",
            columns=[{'id': c, 'name': c} for c in df_details.columns],
            data=df_details.to_dict('records'),
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white',
                'whiteSpace': 'normal',
                'height': 'auto',
                "textAlign":"left",
            },
            style_table={'height': '150px','overflowY': 'auto','textAlign': 'left'},
        ),

        
        

    ],className="two columns left_column"),

    #Middle Column
    html.Div(style={"backgroundColor":"#363431"},children=[
    
        dcc.Tabs(style={'height': '1'},
            id="tabs-with-classes",
            value='tab-1',            
            children=[

                dcc.Tab(label="Building clusters",value="tab-1",style=tab_style, selected_style=tab_selected_style,children=[
                    dcc.Graph(
                        id='geo_data',
                        figure=fig_4,
                            
                
                    )
                ]),


                dcc.Tab(label="Case Classification",value="tab-2",style=tab_style, selected_style=tab_selected_style,children=[
                    dcc.Graph(
                        id='case_classification',
                        figure=fig_1,
                            
                
                    )
                ]),
                

                dcc.Tab(label="Total Cases",value="tab-3",style=tab_style, selected_style=tab_selected_style,children=[
                    dcc.Graph(
                        id='sliding_window_total',
                        figure=fig_2,
                            
                
                    )
                ]),

                dcc.Tab(label="Delay",value="tab-4",style=tab_style, selected_style=tab_selected_style,children=[
                    dcc.Graph(
                        id='sliding_window_delay',
                        figure=fig_3,
                            
                
                    )
                ]),

                 dcc.Tab(label="Age structured delay",value="tab-5",style=tab_style, selected_style=tab_selected_style,children=[
                     dcc.Graph(
                         id="age_delay",
                         figure=fig_6,
                     )
                 ]),


        ]),

        html.Div(style={"border":"5px black solid","textAlign":"center"},children=[
            html.P("Data Source : CHP. For detailed information, click here. For source code, click here"),
        ]),




    ],className="six-half columns"),

    #Right Column
    html.Div(children=[
        dcc.Graph(
                    id='testing_data',
                    figure=fig_5,     
            
                ),

        html.Div(children=[
            html.H3(style={"border":"2px black solid"},children="Global Cases"),

        ],className="left_column"),

        dt.DataTable(
            id="World_covid_cases",
            columns=[{'id': c, 'name': c} for c in df_world.columns],
            data=df_world.to_dict('records'),
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white',
                'whiteSpace': 'normal',
                'height': 'auto',
                "textAlign":"left",
            },
            style_table={'height': '150px','overflowY': 'auto','textAlign': 'left'},
        ),

        html.Div(style={"border":"5px black solid"},children=[
            html.P(last_updated), #replace with actual data
        ],className="left_column"),


    ],className="four columns"),

])


# app.css.append_css({
#     "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
# })

if __name__=="__main__":
    app.run_server(debug=True)