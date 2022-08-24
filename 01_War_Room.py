#%%
import numpy as np
from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc    
import plotly.express as px
import pandas as pd       
from matplotlib import pyplot as plt
import datetime as dt
import time
from dash import dash_table
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA
import seaborn as sns
# %%
df = pd.read_csv("D:\Machine_Learning\Hand_Writing_Humphrey\Plotly_Practice\plotly_practice\留言測試_2022_08_15.csv")
df = df.drop("Unnamed: 0",axis=1)

#%%
# Counting The Total Videos
def value_comma(number):
    return ("{:,}".format(number))

df_count_video=df.copy()
df_count_video['Published_date']=pd.to_datetime(df_count_video['Published_date'])
df_card_1_name='影片數量'
df_card_1_name_eng='Published Videos'
df_count_video_ids=df_count_video['Title'].nunique()
df_count_video_ids=value_comma(df_count_video_ids)

# Summary of Video Table
df_vidoe_summary=df_count_video.drop_duplicates(subset='Title',keep='first')
df_vidoe_summary_select=df_vidoe_summary.loc[:,['video_id','Title','Published_date','Views','like_x','comments','duration']]
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
df_count_video_ids_date['year'] = pd.DatetimeIndex(df_count_video_ids_date['Published_date']).year
df_df_count_video_ids_date_datatable=df_count_video_ids_date.loc[:,['year','Published_date','video_id','Title','Views','like_x','comments','duration']]
df_df_count_video_ids_date_datatable.Published_date = pd.DatetimeIndex(df_df_count_video_ids_date_datatable.Published_date).strftime("%Y-%m-%d")
#df_df_count_video_ids_date_datatable.loc[:, 'Views'] =df_df_count_video_ids_date_datatable['Views'].map('{:,.0f}'.format)
#df_df_count_video_ids_date_datatable.loc[:, 'like_x'] =df_df_count_video_ids_date_datatable['like_x'].map('{:,.0f}'.format)
#df_df_count_video_ids_date_datatable.loc[:, 'comments'] =df_df_count_video_ids_date_datatable['comments'].map('{:,.0f}'.format)

# Comment Summary and rank
df_count_video_comment_user_count=df_count_video
df_count_video_comment_user_count=df_count_video_comment_user_count.groupby('Name').count().sort_values('comments',ascending=False)
df_count_video_comment_user_count=df_count_video_comment_user_count.loc[:,['comments']]
df_count_video_comment_detail=df_count_video
df_count_video_comment_summary=df_count_video_comment_detail.merge(df_count_video_comment_user_count,how='inner',on='Name').drop_duplicates(subset='Name',keep='first').sort_values(by='comments_y',ascending=False)

#%%
def drawText(card_name,card_name_eng,value):
    card=dbc.CardBody([
                html.Div([
                    html.H5(card_name),
                    html.H6(card_name_eng),
                    html.H3(value,style={"color":'#FF2D2B'})
                ], style={'textAlign': 'center'}, className='cardbody') 
            ])
    return(card)

def drawText_2(card_name,card_name_eng):
    card=html.Div([
                    html.Span(card_name, style={'align': 'left','font-weight': 'bold','font-size':'18px',"color":'#C0FF6B'},className='cardbody_s3_name'),
                    html.Br(),
                    html.Span(card_name_eng, style={'textAlign': 'left','font-size':'0.83em',"color":'#C0FF6B'},className='cardbody_s3_name_eng')
                ], className='cardbody_s3') 
    return(card)
def drawText_3(value):
    card=html.Div([
                html.Span(value)
                ], className='cardbody_s3_value',style={'textAlign': 'center','margin':'auto'}) 
    return(card)

def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix,unit='s')

#%%
#Build your components 
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
date=dt.datetime.today().strftime("%Y/%m/%d")
Big_Title=html.H3('頻道戰指中心', style={"color": "white",'text-align':'center'})
Small_Title=html.H5('YouTube Combat Information Center', style={"color": "#C0FF6B",'text-align':'center'})
Channel_logo=html.Img(src=app.get_asset_url('press_play_logo.jpeg'),width=100)
YouTube_logo=html.Img(src=app.get_asset_url('YouTube_icon.png'),width=100)
mytitle = dcc.Markdown(children='')
fig_layout = {'title': 'Dash Data Visualization'}
selected_year=df_count_video_ids_date['year'].unique()
views_graph = dcc.Graph(id="views")
likes_graph = dcc.Graph(id="likes")
dropdown = dcc.Dropdown(df_count_video_ids_date.year.unique(),
                        id="dropdown",
                        value=2022,
                        optionHeight=55,
                        clearable=False)
datatable=dash_table.DataTable(
        id='datatable-comment',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
            if i == "video_id"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df_df_count_video_ids_date_datatable.columns],
        data=df_df_count_video_ids_date_datatable.to_dict('records'),  # the contents of the table
        editable=False,              # allow editing of data inside all cells
        filter_action='none',     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable=False,  # allow users to select 'multi' or 'single' columns
        row_selectable=False,     # allow users to select 'multi' or 'single' rows
        row_deletable=False,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=8,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'width': 0
        },
        style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Title']]+[
        {
            'if': {'column_id': b},
            'textAlign': 'center'
        } for b in ['year','Published_date','video_id']
        ],
        
        style_data={
        'color': 'black',
        'backgroundColor': 'white',
        'font_size': '18px'
        },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#93E9BE',
        }
        ],
        style_header={
        'backgroundColor': 'black',
        'color': 'white',
        'font_size': '18px'
        }
    )
datatable_drop_down=dcc.Dropdown(
                    id="datatable_drop_down",
                    options=df_df_count_video_ids_date_datatable.year.unique(),
                    value=2022,
                    clearable=False
    )
datatable_graph = dcc.Graph(id="table_graph")
datatable_check=dcc.Checklist(
                id="table_checklist",
                options=['Views','like_x','comments'],
                value=['Views','like_x','comments'],
                inline=True)

#--------------------
#X = df_df_count_video_ids_date_datatable[['Views', 'like_x', 'comments']]

#pca = PCA(n_components=3)
#components = pca.fit_transform(X)
#total_var = pca.explained_variance_ratio_.sum() * 100
#fig_test_1 = px.scatter_3d(
    #components, x=0, y=1, z=2,
    #title=f'Total Explained Variance: {total_var:.2f}%',
    #labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
#)
#-------------------

#Section_3 KPI
df_card_wait_name='重要指標'
df_card_wait_name_eng='Critical KPI'
df_card_wait_value='Waiting Data'

df_card_s3_1_name='年度發片數量'
df_card_s3_1_name_eng='Published Videos'
df_card_s3_1_value=html.Span(id='s3_1_value',className='cardbody_s3_value')

df_card_s3_2_name='年度觀看次數'
df_card_s3_2_name_eng='Total Views'
df_card_s3_2_value=html.Span(id='s3_2_value',className='cardbody_s3_value')

df_card_s3_3_name='年度按讚次數'
df_card_s3_3_name_eng='Total Likes'
df_card_s3_3_value=html.Span(id='s3_3_value',className='cardbody_s3_value')

df_card_s3_4_name='年度留言次數'
df_card_s3_4_name_eng='Total Comments'
df_card_s3_4_value=html.Span(id='s3_4_value',className='cardbody_s3_value')

df_card_s3_5_name='年度平均片長'
df_card_s3_5_name_eng='Average Duration'
df_card_s3_5_value=html.Span(id='s3_5_value',className='cardbody_s3_value')

df_card_s3_6_name='平均觀看次數'
df_card_s3_6_name_eng='Average Views'
df_card_s3_6_value=html.Span(id='s3_6_value',className='cardbody_s3_value')

df_card_s3_7_name='平均按讚次數'
df_card_s3_7_name_eng='Average Likes'
df_card_s3_7_value=html.Span(id='s3_7_value',className='cardbody_s3_value')

df_card_s3_8_name='平均留言次數'
df_card_s3_8_name_eng='Average Comments'
df_card_s3_8_value=html.Span(id='s3_8_value',className='cardbody_s3_value')


# Section 4
datatable_comment_rank=dash_table.DataTable(
        id='datatable-comment_rank',
        columns=[
            {"name": 'Name', "id": 'Name', "deletable": False, "selectable": True, "hideable": False},
            {"name": 'Comments_Count', "id": 'comments_y', "deletable": False, "selectable": True, "hideable": False}],
        data=df_count_video_comment_summary.to_dict('records'),  # the contents of the table
        editable=False,              # allow editing of data inside all cells
        filter_action='none',     # allow filtering of data by user ('native') or not ('none')
        sort_action="native",       # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",         # sort across 'multi' or 'single' columns
        column_selectable=False,  # allow users to select 'multi' or 'single' columns
        row_selectable=False,     # allow users to select 'multi' or 'single' rows
        row_deletable=False,         # choose if user can delete a row (True) or not (False)
        selected_columns=[],        # ids of columns that user selects
        selected_rows=[],           # indices of rows that user selects
        page_action="native",       # all data is passed to the table up-front or not ('none')
        page_current=0,             # page number that user is on
        page_size=12,                # number of rows visible per page
        style_cell={                # ensure adequate header width when text is shorter than cell's text
            'width': 0
        },
        style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Title']]+[
        {
            'if': {'column_id': b},
            'textAlign': 'center'
        } for b in ['year','Published_date','video_id']
        ],
        
        style_data={
        'color': 'black',
        'backgroundColor': 'white',
        'font_size': '18px'
        },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#93E9BE',
        }
        ],
        style_header={
        'backgroundColor': 'black',
        'color': 'white',
        'font_size': '18px'
        }
    )
# Comments Ranking
df_count_video_comment_summary_top_15=df_count_video_comment_summary.sort_values(by='comments_y',ascending=False).head(15)
comments_ranking = px.bar(df_count_video_comment_summary_top_15, y='comments_y', x='Name', text_auto='.2s',
            title="留言排行榜<br><sup>Comments Ranking</sup>")
comments_ranking=comments_ranking.update_layout(plot_bgcolor='#111111',
                    paper_bgcolor='#111111',
                    title_font_color='#ffffff',
                    font_color='#ffffff')
#Corrlation Analysis
corr=df_vidoe_summary_select.corr()
corr_fig=px.imshow(corr,color_continuous_scale='ylgnbu',text_auto=True)
corr_fig=corr_fig.update_layout(plot_bgcolor='#111111',
                    paper_bgcolor='#111111',
                    title = dict(text = '相關係數<br><sup>Correlation</sup>',x = 0.5),
                    title_font_size=22,
                    title_font_color='#ffffff',
                    font_color='#ffffff')
# Customize your own Layout
app.layout = html.Div([
    html.Div([
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([Channel_logo,YouTube_logo],className='logo'), 
            dbc.Col([Big_Title,Small_Title],className='title'),
            dbc.Col([])
        ])
    ],className='header'),
      
    html.Br(),
    
    html.Div([
        html.H5(
            [html.Span('頻道名稱 (Channel)：',className = 'channel_tw'),
            html.Span('Press Play',className = 'channel_eng')]),
        html.H6(
            [html.Span('當前日期 (Current Date)：',className = 'channel_tw'),
            html.Span(date, className = 'channel_eng'),], style={'text-align':'left'}),
    ]),
    
    html.Div([    
        dbc.Row([
            dbc.Col([dbc.Card(drawText(df_card_1_name,df_card_1_name_eng,df_count_video_ids))]),
            dbc.Col([dbc.Card(drawText(df_card_2_name,df_card_2_name_eng,df_count_total_views))]),
            dbc.Col([dbc.Card(drawText(df_card_3_name,df_card_3_name_eng,df_count_total_likes))]),
            dbc.Col([dbc.Card(drawText(df_card_4_name,df_card_4_name_eng,df_count_total_comments))])
        ]), 
    ]),
    
    html.Br(),
    
    html.Div([
        html.Div([
            dbc.Row([
                html.H6(['查詢年份'],className='dropdown_text'),
                html.H6(['Please select the year:'],className='dropdown_text'),
            dbc.Col([dropdown], className='dropdown', width=3)])
        ],className='dropdown_1'),
        html.Div([
            dbc.Row([
                dbc.Col([views_graph], width=6,className='views_graph'),
                dbc.Col([likes_graph], width=6,className='likes_graph')])
        ],className='chart_1')
    ],className='chart_section_1'),
    
    html.Br(),
    
    html.Div([
        html.Div([
            html.H5([html.Span('紀錄總覽', className='section_title'),
            html.Br(),
            html.Span('Data Table', className='channel_eng'),
            ], style={'text-align':'center'})
        ],className='dropdown_2'),
        
        html.Div([
            dbc.Row([
                html.H6(['查詢年份'],className='dropdown_text'),
                html.H6(['Please select the year:'],className='dropdown_text'),
                dbc.Col([datatable_drop_down],className='dropdown', width=3)]),
            dbc.Row(dbc.Col([datatable],width={"size": 12}))
        ],className='datatable_1')
    ],className='chart_section_2'),
    
    html.Br(),
    
    html.Div([
        html.Div([
            dbc.Row([
                dbc.Col([datatable_graph],className='datatable_graph',width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([dbc.CardBody(drawText_2(df_card_s3_1_name,df_card_s3_1_name_eng))],className='section_3_col'),
                            dbc.Col([dbc.CardBody(df_card_s3_1_value,style={'textAlign':'center'}, className="card-text")],className='section_3_col')
                        ],className='section_3_card_row',style={'margin':'auto'})
                    ],className="section_3_card",style={'width':'400px','height':'100px','margin': 'auto','margin-bottom': '10px'}),
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([dbc.CardBody(drawText_2(df_card_s3_2_name,df_card_s3_2_name_eng))],className='section_3_col'),
                            dbc.Col([dbc.CardBody(df_card_s3_2_value,style={'textAlign':'center'}, className="card-text")],className='section_3_col')
                        ],className='section_3_card_row',style={'margin':'auto'})
                    ],className="section_3_card",style={'width':'400px','height':'100px','margin': 'auto','margin-bottom': '10px'}),
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([dbc.CardBody(drawText_2(df_card_s3_3_name,df_card_s3_3_name_eng))],className='section_3_col'),
                            dbc.Col([dbc.CardBody(df_card_s3_3_value,style={'textAlign':'center'}, className="card-text")],className='section_3_col')
                        ],className='section_3_card_row',style={'margin':'auto'})
                    ],className="section_3_card",style={'width':'400px','height':'100px','margin': 'auto','margin-bottom': '10px'}),
                    dbc.Card([
                       dbc.Row([
                            dbc.Col([dbc.CardBody(drawText_2(df_card_s3_4_name,df_card_s3_4_name_eng))],className='section_3_col'),
                            dbc.Col([dbc.CardBody(df_card_s3_4_value,style={'textAlign':'center'}, className="card-text")],className='section_3_col')
                        ],className='section_3_card_row',style={'margin':'auto'})
                    ],className="section_3_card",style={'width':'400px','height':'100px','margin': 'auto','margin-bottom': '10px'}),
                ],width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([dbc.CardBody(drawText_2(df_card_s3_5_name,df_card_s3_5_name_eng),style={'margin':'auto'})],className='section_3_col'),
                            dbc.Col([dbc.CardBody(drawText_3(df_card_s3_5_value), style={'margin':'auto','textAlign': 'center'}, className="card-text")],className='section_3_col')
                        ],className='section_3_card_row',style={'margin':'auto'})
                    ],className="section_3_card",style={'width':'400px','height':'100px','margin': 'auto','margin-bottom': '10px'}),
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([dbc.CardBody(drawText_2(df_card_s3_6_name,df_card_s3_6_name_eng),style={'margin':'auto'})],className='section_3_col'),
                            dbc.Col([dbc.CardBody(drawText_3(df_card_s3_6_value), style={'margin':'auto','textAlign': 'center'}, className="card-text")],className='section_3_col')
                        ],className='section_3_card_row',style={'margin':'auto'})
                    ],className="section_3_card",style={'width':'400px','height':'100px','margin': 'auto','margin-bottom': '10px'}),
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([dbc.CardBody(drawText_2(df_card_s3_7_name,df_card_s3_7_name_eng),style={'margin':'auto'})],className='section_3_col'),
                            dbc.Col([dbc.CardBody(drawText_3(df_card_s3_7_value), style={'margin':'auto','textAlign': 'center'}, className="card-text")],className='section_3_col')
                        ],className='section_3_card_row',style={'margin':'auto'})
                    ],className="section_3_card",style={'width':'400px','height':'100px','margin': 'auto','margin-bottom': '10px'}),
                    dbc.Card([
                        dbc.Row([
                            dbc.Col([dbc.CardBody(drawText_2(df_card_s3_8_name,df_card_s3_8_name_eng),style={'margin':'auto'})],className='section_3_col'),
                            dbc.Col([dbc.CardBody(drawText_3(df_card_s3_8_value), style={'margin':'auto','textAlign': 'center'}, className="card-text")],className='section_3_col')
                        ],className='section_3_card_row',style={'margin':'auto'})
                    ],className="section_3_card",style={'width':'400px','height':'100px','margin': 'auto','margin-bottom': '10px'}),
                ],width=3)
            ])
        ])
    ]),
    
    html.Br(),
    
    html.Div([
        html.Div([
            html.H5([html.Span('觀眾分析', className='section_title'),
            html.Br(),
            html.Span('Audience Analysis', className='channel_eng'),
            ], style={'text-align':'center'})
        ],className='section_title')
    ],className='section4'),
    
    html.Div([
        dbc.Row([
                dbc.Col([datatable_comment_rank],width=3,className='datatable_2'),
                dbc.Col(dcc.Graph(figure=comments_ranking),width=6,className='comments_ranking'),
                dbc.Col(dcc.Graph(figure=corr_fig),width=3,className='corr_fig')])
    ]),
    

    
    #html.Div([
        #html.Div([
            #dcc.Graph(figure=fig_test_1)
        #])
    #])
])



# Callback allows components to interact
@app.callback(Output(component_id="views",component_property= "figure"),
              [Input(component_id="dropdown", component_property="value")])
def update_chart(value):
    df=df_count_video_ids_date
    df_selected_year=df['year']==value
    df_selected_year=df[df_selected_year]  
    fig_1 = px.line(df_selected_year, 
                    x='Published_date', 
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
    fig_1.update_layout(xaxis_rangeslider_visible=True)
    return fig_1
    
                
@app.callback(Output(component_id="likes",component_property= "figure"),
              [Input(component_id="dropdown", component_property="value")])
def update_chart(value):
    df=df_count_video_ids_date
    df_selected_year=df['year']==value
    df_selected_year=df[df_selected_year]      
    fig_2 = px.bar(df_selected_year,
                   x='Published_date',
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
    fig_2.update_layout(xaxis_rangeslider_visible=True)
    return fig_2

@app.callback(
    Output("datatable-comment", "data"), 
    Input("datatable_drop_down", "value")
)
def display_table(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    return dff_selected_year.to_dict("records")

@app.callback(
    Output("table_graph", "figure"), 
    Input("datatable_drop_down", "value"))
def update_line_chart(value):
    df=df_count_video_ids_date
    df_selected_year=df['year']==value
    df_selected_year=df[df_selected_year]
    
    fig_3 = go.Figure()
    fig_3.add_trace(go.Scatter(x=df_selected_year['Published_date'], 
                               y=df_selected_year['Views'],
                        mode='lines+markers',
                        name='Views')),
    fig_3.add_trace(go.Scatter(x=df_selected_year['Published_date'], 
                               y=df_selected_year['like_x'],
                        mode='lines+markers',
                        name='Like')),
    fig_3.add_trace(go.Scatter(x=df_selected_year['Published_date'], 
                               y=df_selected_year['comments'],
                        mode='lines+markers',
                        name='Comments'))

    fig_3.update_layout(plot_bgcolor='#111111',
                        paper_bgcolor='#111111',
                        title = dict(text = '數據疊加圖<br><sup>Data Table Chart</sup>',x = 0.5),
                        title_font_size=22,
                        title_font_color='#ffffff',
                        font_color='#ffffff',
                        xaxis=dict(showline=True,
                                   showgrid=False,
                                   tickfont=dict(color='#ffffff')),
                        yaxis=dict(tickfont=dict(color='#ffffff')),
                        )
    fig_3.update_layout(xaxis_rangeslider_visible=True)
    return fig_3


@app.callback(
    Output("s3_1_value", "children"), 
    Input("datatable_drop_down", "value")
)
def display_s3_1_value(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    dff_selected_year_video_sum=dff_selected_year['video_id'].count()
    return value_comma(dff_selected_year_video_sum)


@app.callback(
    Output("s3_2_value", "children"), 
    Input("datatable_drop_down", "value")
)
def display_s3_2_value(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    dff_selected_year_video_sum=dff_selected_year['Views'].sum()
    return value_comma(dff_selected_year_video_sum)

@app.callback(
    Output("s3_3_value", "children"), 
    Input("datatable_drop_down", "value")
)
def display_s3_3_value(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    dff_selected_year_video_sum=dff_selected_year['like_x'].sum()
    return value_comma(dff_selected_year_video_sum)

@app.callback(
    Output("s3_4_value", "children"), 
    Input("datatable_drop_down", "value")
)
def display_s3_4_value(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    dff_selected_year_video_sum=dff_selected_year['comments'].sum()
    return value_comma(dff_selected_year_video_sum)

@app.callback(
    Output("s3_5_value", "children"), 
    Input("datatable_drop_down", "value")
)
def display_s3_5_value(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    dff_selected_year['duration'] = pd.to_datetime(dff_selected_year['duration']).dt.time.astype(str)
    tsum = dt.timedelta()
    count = 0
    for single_time in dff_selected_year['duration']:
        t = dt.datetime.strptime(single_time,'%H:%M:%S')
        tdelta = dt.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
        tsum = tsum + tdelta
        count = count + 1
    taverage = tsum / count
    average_time = str(taverage).split(".")[0]
    return average_time

@app.callback(
    Output("s3_6_value", "children"), 
    Input("datatable_drop_down", "value")
)
def display_s3_6_value(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    dff_selected_year_video_mean=dff_selected_year['Views'].mean()
    return value_comma(dff_selected_year_video_mean).split(".")[0]

@app.callback(
    Output("s3_7_value", "children"), 
    Input("datatable_drop_down", "value")
)
def display_s3_7_value(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    dff_selected_year_video_mean=dff_selected_year['like_x'].mean()
    return value_comma(dff_selected_year_video_mean).split(".")[0]

@app.callback(
    Output("s3_8_value", "children"), 
    Input("datatable_drop_down", "value")
)
def display_s3_8_value(value):
    dff = df_df_count_video_ids_date_datatable
    dff_selected_year=dff['year']==value
    dff_selected_year=dff[dff_selected_year]
    dff_selected_year_video_mean=dff_selected_year['comments'].mean()
    return value_comma(dff_selected_year_video_mean).split(".")[0]

# Run app
if __name__=='__main__':
    app.run_server(debug=False)



# %%


# %%
