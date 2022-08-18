#%%
from turtle import left
from click import style
import numpy as np
from ctypes import alignment
from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc    
import plotly.express as px
import pandas as pd       
from matplotlib import pyplot as plt
from sqlalchemy import false
from yaml import ValueToken
import datetime as dt

# %%
df = pd.read_csv("/Users/humphreyshen/Desktop/Plotly_Practice/plotly_practice/留言測試_2.csv")

#%%
def value_comma(number):
    return ("{:,}".format(number))

def drawText(card_name,card_name_eng,value):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H5(card_name),
                    html.H6(card_name_eng),
                    html.H3(value)
                ], style={'textAlign': 'center'}) 
            ])
        ),
    ])



#%%
# Counting The Total Videos
df_count_video=df.copy()
df_card_1_name='影片數量'
df_card_1_name_eng='Published Videos'
df_count_video_ids=df_count_video['Title'].nunique()
df_count_video_ids=value_comma(df_count_video_ids)

# Count Total Views
df_card_2_name='總觀看次數'
df_card_2_name_eng='Total Views'
df_count_total_views=df_count_video.drop_duplicates(subset='Title',keep='first')
df_count_total_views=df_count_total_views['Views'].sum()
df_count_total_views=value_comma(df_count_total_views)

# Count Total Likes
df_card_3_name='總按讚次數'
df_card_3_name_eng='Total Views'
df_count_total_likes=df_count_video.drop_duplicates(subset='Title',keep='first')
df_count_total_likes=df_count_total_likes['like_x'].sum()
df_count_total_likes=value_comma(df_count_total_likes)

# Count Total Comments
df_card_4_name='總留言次數'
df_card_4_name_eng='Total Comments'
df_count_total_comments=df_count_video.drop_duplicates(subset='Title',keep='first')
df_count_total_comments=df_count_total_comments['comments'].sum()
df_count_total_comments=value_comma(df_count_total_comments)

# Show Original Table
df_count_video_ids_date=df_count_video.drop_duplicates(subset='Title',keep='first')

#%%
# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
date=dt.datetime.today().strftime("%Y/%m/%d")
Big_Title=html.H3('頻道戰指中心', style={"color": "white",'text-align':'center'})
Small_Title=html.H5('YouTube Combat Information Center', style={"color": "#127cc1",'text-align':'center'})
Channel_logo=html.Img(src=app.get_asset_url('press_play_logo.jpeg'),width=100)
YouTube_logo=html.Img(src=app.get_asset_url('YouTube_icon.png'),width=100)
mytitle = dcc.Markdown(children='')
colors = {
    'background': '#111111',
    'text': '#7FDBFF'}
fig_layout = {'title': 'Dash Data Visualization'}
views_graph = dcc.Graph(id="views")
likes_graph = dcc.Graph(id="likes")
dropdown = dcc.Dropdown(id="dropdown",
                        options=df_count_video_ids_date['channel'],
                        value='Press_Play',
                        clearable=False)

# Customize your own Layout
app.layout = html.Div([
                html.Br(),
                dbc.Row([
                    dbc.Col([Channel_logo,YouTube_logo]), 
                    dbc.Col([Big_Title,Small_Title]),
                    dbc.Col([])
                    ]),  
                html.Br(),
                html.H4([html.Span(' 頻道名稱：', style={"color": "white"}),
                        html.Span('Press Play', style={"color": "yellow"}),
                        ], style={'text-align':'left'}),
                html.H6([html.Span('當前日期：', style={"color": "white"}),
                        html.Span(date, style={"color": "yellow"}),
                        ], style={'text-align':'left'}),
                dbc.Row([
                    dbc.Col([dropdown], width=3)], justify='left'),
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([drawText(df_card_1_name,df_card_1_name_eng,df_count_video_ids)], width=3),
                            dbc.Col([drawText(df_card_2_name,df_card_2_name_eng,df_count_total_views)], width=3),
                            dbc.Col([drawText(df_card_3_name,df_card_3_name_eng,df_count_total_likes)], width=3),
                            dbc.Col([drawText(df_card_4_name,df_card_4_name_eng,df_count_total_comments)], width=3)], align='center')])), 
                html.Br(),
                dbc.Row([
                    dbc.Col([views_graph], width=6),
                    dbc.Col([likes_graph], width=6)]),
            ])

# Callback allows components to interact
@app.callback(Output(component_id="views",component_property= "figure"),
              Input(component_id="dropdown", component_property="value"))
def update_chart(df):
    df=df_count_video_ids_date
    fig_1 = px.line(df, x="Published_date", 
                    y="Views")
    fig_1.update_layout(plot_bgcolor='#111111',
                        paper_bgcolor='#111111',
                        title = dict(text = '觀看次數時序圖<br><sup>Views With Time Seqence</sup>',x = 0.5),
                        title_font_size=22,
                        title_font_color='#ffffff',
                        font_color='#ffffff',
                        xaxis=dict(showline=True,
                                   showgrid=False,
                                   tickfont=dict(color='#ffffff')),
                        yaxis=dict(tickfont=dict(color='#ffffff')),
                        )

    return fig_1
    
                
@app.callback(Output(component_id="likes",component_property= "figure"),
              Input(component_id="dropdown", component_property="value"))
def update_chart(df):
    df=df_count_video_ids_date
    fig_2 = px.bar(df,
                   x="Published_date", 
                   y="like_x", 
                   color='like_x')
    fig_2.update_layout(plot_bgcolor='#111111',
                        paper_bgcolor='#111111',
                        title = dict(text = '按讚時序圖<br><sup>Likes With Time Seqence</sup>',x = 0.5),
                        title_font_size=22,
                        title_font_color='#ffffff',
                        font_color='#ffffff',
                        xaxis=dict(showline=True,
                                   showgrid=False,
                                   tickfont=dict(color='#ffffff')),
                        yaxis=dict(tickfont=dict(color='#ffffff')),
                        )
    return fig_2

# Run app
if __name__=='__main__':
    app.run_server(debug=False)

# %%
help(html.Img)

def update_graph(column_name):  # function arguments come from the component property of the Input

    print(column_name)
    print(type(column_name))
    fig = px.bar(data_frame=df_count_video_ids_date,
                x='Published_date',
                y='Views')

    return fig, '#### '+column_name  # returned objects are assigned to the component property of the Output

# %%
df_count_video_ids_date
# %%
