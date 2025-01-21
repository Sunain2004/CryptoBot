import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
import pytz

# Path to the CSV file
csv_file = "processed_crypto_data.csv"

# Timezone settings
source_timezone = pytz.UTC  # Assuming your timestamps are in UTC
target_timezone = pytz.timezone('Etc/GMT-5')  # Replace with your desired timezone

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Crypto Price Chart"

# Load and convert data
def load_data():
    # Load the data
    data = pd.read_csv(csv_file)
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # Localize to source timezone (if not already) and convert to target timezone
    data['timestamp'] = data['timestamp'].dt.tz_localize(source_timezone).dt.tz_convert(target_timezone)
    return data

# Define app layout
app.layout = html.Div(style={'backgroundColor': '#1e1e1e', 'padding': '20px'}, children=[
    html.H1('BTC/USDT', style={'color': 'white', 'textAlign': 'center'}),

    # Store for user layout settings
    dcc.Store(id='user-layout', data=None),

    dcc.Interval(
        id='interval-component',
        interval=5000,  # Update every 5 seconds
        n_intervals=0
    ),
    dcc.Graph(
        id='candlestick-chart',
        style={'height': '800px','backgroundColor': '#1e1e1e'},
        config={
            'displayModeBar': True,
            'scrollZoom': True,
            'displaylogo': False  # Remove Plotly logo from mode bar
        },
        figure={
            'layout': {
                'title': {
                    'text': 'Crypto Price Chart',
                    'font': {'size': 24},
                    'x': 0.5  # Center align the title
                },
                'xaxis': {
                    'title': {'text': 'Time', 'font': {'size': 14}},
                    'rangeslider': {'visible': False},
                    'showgrid': True,
                    'gridcolor': 'gray'
                },
                'yaxis': {
                    'title': {'text': 'Price', 'font': {'size': 14}},
                    'showgrid': True,
                    'gridcolor': 'gray'
                },
                'template': 'plotly_dark',  # Keep dark theme
                'plot_bgcolor': '#1e1e1e',  # Set the plot background to match app
                'paper_bgcolor': '#1e1e1e',  # Set the paper (outer) background
                'legend': {
                    'orientation': "h",
                    'yanchor': "bottom",
                    'y': 1.02,
                    'xanchor': "right",
                    'x': 1
                }
            }
        }

    )
])

# Update chart dynamically
@app.callback(
    Output('candlestick-chart', 'figure'),
    [Input('interval-component', 'n_intervals')],
    [State('candlestick-chart', 'relayoutData'), State('user-layout', 'data')]
)
def update_chart(n, relayout_data, user_layout):
    # Reload data
    data = load_data()

    # Calculate dynamic y-axis range
    y_min = data['low'].min()
    y_max = data['high'].max()
    y_padding = (y_max - y_min) * 0.10

    # Highlight current price
    latest_data = data.iloc[-1]
    current_price = latest_data['close']

    # Determine default x-axis range for the last 24 hours
    last_24h = pd.Timestamp.now() - pd.Timedelta(hours=24)
    auto_zoom_min = last_24h
    auto_zoom_max = data['timestamp'].max()

    # Default x-axis range
    x_range = [auto_zoom_min, auto_zoom_max]

    # Restore user layout if available
    if relayout_data and 'xaxis.range[0]' in relayout_data and 'xaxis.range[1]' in relayout_data:
        x_range = [
            pd.to_datetime(relayout_data['xaxis.range[0]']),
            pd.to_datetime(relayout_data['xaxis.range[1]'])
        ]
    elif user_layout:
        x_range = user_layout.get('xaxis.range', x_range)

    # Build the chart
    fig = go.Figure()

    # Add candlestick data
    fig.add_trace(go.Candlestick(
        x=data['timestamp'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        name='Candlestick'
    ))

    # Add SMA(20)
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['SMA_20'],
        mode='lines',
        line=dict(color='orange', width=1),
        name='SMA(20)'
    ))

    # Add SMA(50)
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['SMA_50'],
        mode='lines',
        line=dict(color='purple', width=1),
        name='SMA(50)'
    ))

    # Add EMA(20)
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['EMA_20'],
        mode='lines',
        line=dict(color='blue', width=1),
        name='EMA(20)'
    ))

    # Add EMA(50)
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['EMA_50'],
        mode='lines',
        line=dict(color='green', width=1),
        name='EMA(50)'
    ))

    # Highlight the current price
    fig.add_trace(go.Scatter(
        x=[latest_data['timestamp']],
        y=[current_price],
        mode='markers+text',
        marker=dict(size=10, color='red'),
        text=[f'Current: {current_price:.2f}'],
        textposition="top left",
        name='Current Price'
    ))

    # Update figure layout dynamically
    # fig.update_layout(user_layout.get())

    return fig

# Store user layout settings
@app.callback(
    Output('user-layout', 'data'),
    [Input('candlestick-chart', 'relayoutData')],
)
def save_user_layout(relayout_data):
    if relayout_data:
        return {'xaxis.range': [
            relayout_data.get('xaxis.range[0]'),
            relayout_data.get('xaxis.range[1]')
        ]}
    return dash.no_update

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
