from dash import Dash
# from dash import dcc

# # , dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

dt=pd.read_csv("data/dt1.csv")
zt=pd.read_csv("data/zt.csv")

def color_discrete_map_generator(sub):
    lul = px.colors.sequential.dense
    if sub=="Overall":
        col_map = {
            'None': lul[2], 
            '2 Advanced Courses': lul[8], 
            'Prep Courses': lul[5],
            '1 Advanced Course':lul[6],
            '3 Advanced Courses':lul[10],
            '3 Advanced Courses|Prep Course':lul[11],
            "1 Advanced Course|Prep Course":lul[7],
            "2 Advanced Courses|Prep Course":lul[9]
          }
    else:
        col_map={
            "None":lul[2],
            "Prep Courses":lul[5],
            f"AP {sub}":lul[8],                                
            f"AP {sub}|Honors {sub}|Prep Course":lul[11],
            f"AP {sub}|Prep Courses":lul[9],           
            f"AP {sub}|Honors {sub}":lul[10],
            f"Honors {sub}":lul[6],               
            f"Honors {sub}|Prep Courses":lul[7]
        }
    
    
    return col_map

app = Dash(__name__)

app.layout = html.Div(id="numerical scatter", children=[
                html.H1("libstu", style={'color':"black", 'font':'Sans-serif', 'backgroundColor':'#D3D3D3'}),
                html.Label([
                    "Options:",
                    dcc.RadioItems(
                        id='variables-dropdown',
                        value='ovr', 
                        options=[
                            {'label': 'mth', 'value': 'Math'},
                            {'label': 'eng', 'value': 'English'},
                            {'label': 'sci', 'value': 'Science'},
                            {'label':'ovr', 'value':'Overall'}
                        ]
                        )
                    ]),
                html.Div(children=[
                    dcc.Graph(id='scatter_plot', style={'display': 'inline-block'}),
                    dcc.Graph(id="bar", style={'display': 'inline-block'})
                    ], style={'display': 'inline-block'}, className="container"
                )     
            ],style={'width': '48%', 'display': 'inline-block', 'float':'top'})
@app.callback(
    Output("scatter_plot", "figure"), 
    Output("bar", "figure"),
    Input('variables-dropdown', 'value'))
def scatter(val):
    def sub_plot(sub):
        fig = px.scatter(
            data_frame = dt, 
            x=f"{sub} Avg", 
            y=f"{sub} ACT", 
            color=f"{sub}_color_map", 
            color_discrete_map=color_discrete_map_generator(sub), 
            opacity=0.8, 
            trendline="ols",
            trendline_scope="overall",
            trendline_color_override="red",
            
        )

        fig.update_traces(marker={'size': 12})

        fig.update_layout(
            height=600, 
            width=1000,
            title=f"{sub} Average VS {sub} ACT",
            template="seaborn",
            legend=dict(
            title="Types of Students",
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="#EBECF0",
            bordercolor="Black",
            borderwidth=2,
            font=dict(size=12))
        )
        return fig
    
    def bar_graph(sub):
        temp = dt[f"{sub}_color_map"].value_counts()
        fig = px.bar(temp.values, color=temp.keys(), color_discrete_map=color_discrete_map_generator(sub), text=[f"{round(v*100/dt.shape[0], 1)}%" for v in temp.values])
        fig.update_traces(textposition="outside")
        fig.update_layout(
            title="Count",
            height=450, 
            width=400,
            template='seaborn',
            yaxis={'title':'test', 'visible': True, 'title':None, 'showgrid':True, 'showticklabels':False},
            xaxis={'visible':True, 'title':None, 'showgrid':True, 'showticklabels':False},
            margin=dict(
                l = 10,        # left
                r = 10,        # right
                t = 50,        # top
                b = 10,        # bottom
            ),
            legend=dict(
            title="Types of Students",
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="#EBECF0",
            bordercolor="Black",
            borderwidth=2,
            font=dict(size=13)),
            showlegend=False

        )
        return fig


    if val == "ovr":
        fig = px.scatter(
            data_frame = dt, 
            x="Last GPA", 
            y="Composite ACT", 
            color="Overall_color_map", 
            color_discrete_map=color_discrete_map_generator("Overall"), 
            opacity=0.8, 
            trendline="ols",
            trendline_scope="overall",
            trendline_color_override="red",
            
        )

        fig.update_traces(marker={'size': 12})

        fig.update_layout(
            height=600, 
            width=1000,
            title="GPA VS ACT",
            template="seaborn",
            legend=dict(
            title="Types of Students",
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="#EBECF0",
            bordercolor="Black",
            borderwidth=2,
            font=dict(size=12))
        )
        return fig, bar_graph("Overall")
    elif val=='eng':
        return sub_plot('English'), bar_graph("English")
    elif val=='mth':
        return sub_plot('Math'), bar_graph("Math")
    elif val=='sci':
        return sub_plot('Science'), bar_graph("Science")
        


if __name__ == '__main__':
    app.run_server(debug=True)