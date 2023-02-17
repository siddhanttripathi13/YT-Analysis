# Import libraries
import dash
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Loading data
channel_df = pd.read_csv('./data/channel_stats.csv')
video_df = pd.read_csv('./data/video_data.csv')

# Set up the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Define app layout
app.layout = dbc.Container([

    dbc.Row([

        dbc.Col(html.H1([html.Img(src="/assets/YouTube_Logo.png")]),
                width={'size': 1, 'offset': 1}),

        dbc.Col(html.H1("YouTube Analytics Dashboard"),
                width={'size': 6, 'offset': 0})

    ], justify='center', align='center'),

    dbc.Row([

        dbc.Col([html.P('Select Channel',
                        style={'textDecoration': 'underline'},
                        className="text-muted"),

                dcc.Dropdown(id="channel-dropdown", multi=False,
                             options=[{"label": "All", "value": "All"}] + [{"label": channel, "value": channel}
                                                                           for channel in channel_df["channelName"].unique()],
                             value='All',
                             clearable=False,
                             className='text-black',
                             style={'width': '60%'}),

                dcc.Graph(id="subscriber-count-graph", figure={})
                 ], width={'size': 5, 'offset': 0}),

        dbc.Col(dcc.Graph(id="view-count-graph", figure={}),
                width={'size': 5, 'offset': 0})

    ], justify='center', align='end'),

    dbc.Row([

        dbc.Col(dcc.Graph(id="view-count-violin", figure={}),
                width={'size': 4, 'offset': 0}),

        dbc.Col(dcc.Graph(id="view-comment-scatter", figure={}),
                width={'size': 4, 'offset': 0}),

        dbc.Col(dcc.Graph(id="view-like-scatter", figure={}),
                width={'size': 4, 'offset': 0})

    ], justify='center', align='end'),

    dbc.Row([

        dbc.Col(dcc.Graph(id="best-performing", figure={}),
                width={'size': 4, 'offset': 0}),

        dbc.Col(dcc.Graph(id="worst-performing", figure={}),
                width={'size': 4, 'offset': 0})

    ], justify='around', align='end')

], fluid=True)

# Define the callbacks for the app
@app.callback(
    [Output("subscriber-count-graph", "figure"),
     Output("view-count-graph", "figure"),
     Output("view-count-violin", "figure"),
     Output("view-comment-scatter", "figure"),
     Output("view-like-scatter", "figure"),
     Output("best-performing", "figure"),
     Output("worst-performing", "figure")],
    [Input("channel-dropdown", "value")]
)
def update_graphs(selected_channel):
    channel_data = channel_df

    # Filtering channel
    if selected_channel == "All":
        video_data = video_df
        title_suffix = "All Channels"
    else:
        video_data = video_df[video_df["channelTitle"] == selected_channel]
        title_suffix = selected_channel

    # Create a bar chart of subscriber count by channel
    subscriber_fig = px.bar(channel_data, x="channelName",
                            y="subscriberCount", title=f"Subscriber Count - {title_suffix}")

    # Create a bar chart of view count by channel
    view_fig = px.bar(channel_data, x="channelName",
                      y="viewCount", title=f"View Count - {title_suffix}")

    # Update bar chart based on selected channel
    if selected_channel != "All":
        subscriber_fig.update_traces(marker_color=[
                                     "red" if name == selected_channel else "grey" for name in channel_data["channelName"]])
        view_fig.update_traces(marker_color=[
                               "red" if name == selected_channel else "grey" for name in channel_data["channelName"]])

    # Create a violin plot of view count by channel
    view_violin = px.violin(video_data, x="channelTitle", y="viewCount",
                            title=f"View Count Distribution - {title_suffix}")

    # Create a scatter plot of view count vs comment count
    view_comment_scatter = px.scatter(
        video_data, x="viewCount", y="commentCount", title=f"Views vs Comments - {title_suffix}")

    # Create a scatter plot of view count vs like count
    view_like_scatter = px.scatter(
        video_data, x="viewCount", y="likeCount", title=f"Views vs Likes - {title_suffix}")

    # Create a bar chart of view count by video titles for top 10 best performing videos
    best_performing = px.bar(video_data.sort_values('viewCount', ascending=False)[0:9],
                             x="title", y="viewCount", title=f"Best performing videos - {title_suffix}")

    # Create a bar chart of view count by video titles for top 10 worst performing videos
    worst_performing = px.bar(video_data.sort_values('viewCount', ascending=True)[0:9],
                              x="title", y="viewCount", title=f"Worst performing videos - {title_suffix}")

    subscriber_fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="#ffffff"
    )

    view_fig.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="#ffffff"
    )

    view_violin.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="#ffffff"
    )

    view_comment_scatter.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="#ffffff"
    )

    view_like_scatter.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="#ffffff"
    )

    best_performing.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="#ffffff"
    )

    worst_performing.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="#ffffff"
    )

    return subscriber_fig, view_fig, view_violin, view_comment_scatter, view_like_scatter, best_performing, worst_performing


if __name__ == "__main__":
    app.run_server(debug=False, port=2000)
